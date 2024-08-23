import json
import sys
import model.data_model as dm

import clr
import pandas as pd
import os
import psutil

sys.path.append('./service')
from pyadomd import Pyadomd

dll_name = "Microsoft.AnalysisServices.Tabular.DLL"

try:
    clr.AddReference(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dll_name))
except:
    clr.AddReference(os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name))

import Microsoft.AnalysisServices.Tabular as Tabular

def format_instance_and_filename(data):
    """
    Formats the string by concatenating the instance name and file name.
    :param data: Dictionary containing the keys 'instance' and 'file_name'.
    :return: Formatted string in the format 'instance - file_name'. Example: localhost:666 - Data Model.pbix
    """
    instance = data.get('instance', '')
    file_name = data.get('file_name', '')

    return f'{instance} - {file_name}'

def get_tcp_connections():
    """
    Retrieves all TCP connections.
    :return: list of tcp connections
    """
    return psutil.net_connections(kind='tcp')

def find_ssas_ports(tcp_connections):
    """
    Finds all localhost ports used by SSAS (msmdsrv.exe) instances.
    :param tcp_connections: list of TCP connections
    :return: list of SSAS ports
    """
    ssas_ports = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == 'msmdsrv.exe':
            for conn in tcp_connections:
                if conn.pid == proc.info['pid'] and conn.status == psutil.CONN_LISTEN:
                    ssas_ports.append(conn.laddr.port)
                    break
    return ssas_ports

def find_pbi_files():
    """
    Finds all running Power BI Desktop instances and retrieves the open .pbix file names.
    :return: list of Power BI .pbix files
    """
    pbi_files = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'PBIDesktop.exe':
            for arg in proc.info['cmdline']:
                if arg.endswith('.pbix'):
                    pbi_files.append(os.path.basename(arg))
                    break
    return pbi_files

def list_running_ssas():
    """
    Returns a list of SSAS instances with associated .pbix files and localhost:port.
    :return: list of dictionaries with 'instance' (localhost:port) and 'file_name' (.pbix file)
    """
    tcp_connections = get_tcp_connections()
    ssas_ports = find_ssas_ports(tcp_connections)
    pbi_files = find_pbi_files()

    instances = []
    
    # Zip the SSAS ports and PBI files together, assuming they were started together
    for port, pbix_file in zip(ssas_ports, pbi_files):
        instances.append({
            'instance': f'localhost:{port}',
            'file_name': pbix_file
        })

    return instances

def list_running_valid_ssas():
    """
    Search for running SSAS instances and return a list of instances that can be connected,
    excluding reports without a data model.
    :return: list of string like 'localhost:port_number'
    """
    instances = list_running_ssas()
    valid_instances = []
    for instance in instances:
        try:
            dm.DataModel(instance['instance'], skip_loading=True)
            formated_instance = format_instance_and_filename(instance)
            valid_instances.append(formated_instance)
        except:
            pass
    return valid_instances

def connect_ssas(port_number):
    """
    Connect to a SSAS instance using the port number
    :param port_number: like 'localhost:port_number'
    :return: connection object
    """
    connection_string = f'Provider=MSOLAP;Data Source={port_number};'
    con = Pyadomd(connection_string)
    con.open()
    return con


def close_connection(con):
    """
    Close the connection to the SSAS instance
    :param con: connection object
    """
    con.close()


def run_query(con, dax_query):
    """
    Run a DAX query and return the result as a DataFrame
    :param con: connection object
    :param dax_query: string with the DAX query
    :return: Pandas DataFrame
    """
    cursor = con.cursor().execute(dax_query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[column[0] for column in cursor.description])
    cursor.close()
    return df


def get_model_bim(port_number):
    """
    Get the model.bim file from a SSAS instance
    https://learn.microsoft.com/pt-br/dotnet/api/microsoft.analysisservices.tabular.database?view=analysisservices-dotnet
    https://learn.microsoft.com/pt-br/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet
    :param port_number: like 'localhost:port_number'
    :return: json string with the model.bim file
    """
    server = Tabular.Server()
    server.Connect(port_number)
    database = server.Databases[0]
    script = Tabular.JsonScripter.ScriptCreate(database)
    json_file = json.loads(script)
    edited = json_file['create']['database']
    raw_json = json.dumps(edited, indent=2)
    return raw_json