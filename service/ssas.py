import datetime
import json
import os
import sys

import clr
import pandas as pd
import psutil
from debugpy.launcher.debuggee import process

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

def get_ssas_ports(tcp_connections):
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


def add_power_bi_details(port):
    """
    Retrieves details about a Power BI Desktop instance for a given port number.
    :param port: The port number of the ssas instance.
    :return: A dictionary containing details about the Power BI instance in the format:
        {
            'instance': 'localhost:port',
            'file_name': 'Semantic Model' or 'file_name.pbix',
            'start_time': 'YYYY-MM-DD HH:MM:SS'
        }
    """
    processes = get_power_bi_processes()

    instance_json = {
        'instance': f'localhost:{port}',
        'file_name': 'Semantic Model',
        'start_time': None
    }

    for proc in processes:

        process_connections_ports = [port.raddr.port for port in proc.connections() if
                                     port.status == psutil.CONN_ESTABLISHED]
        if port in process_connections_ports:

            for arg in proc.info['cmdline']:
                if arg.endswith('.pbix') or arg.endswith('.pbip'):
                    instance_json['file_name'] = os.path.basename(arg)
                    break

            instance_json['start_time'] = datetime.datetime.fromtimestamp(proc.info['create_time']).strftime(
                '%Y-%m-%d %H:%M:%S')
            return instance_json

    return instance_json

def get_power_bi_processes():
    """
    Retrieves a list of running Power BI Desktop processes.
    :return: A list of psutil.Process objects representing running Power BI Desktop processes.
    """
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline', 'create_time']):
        if proc.info['name'] == 'PBIDesktop.exe':
            processes.append(proc)
    return processes


def list_running_instances():
    """
    Lists active instances of Power BI Desktop, providing details about each.
    :return: a list of dictionaries, each containing details about a Power BI instance. example:
    [
        {
            'instance': 'localhost:port',
            'file_name': 'Semantic Model' or 'file_name.pbix',
            'start_time': 'YYYY-MM-DD HH:MM:SS'
        },
        ...
    ]
    """
    ssas_ports = get_ssas_ports(get_tcp_connections())
    instances = []

    for ssas_port in ssas_ports:
        instance = add_power_bi_details(ssas_port)
        instances.append(instance)

    return instances


def list_formatted_instances():
    """
    Retrieves a list of running Power BI Desktop SSAS instances, along with associated .pbix or .pbip files and the localhost port.
    :return: list of formatted instances in the format 'instance - file_name'. Example: localhost:666 - Data Model.pbix
    """
    instances = list_running_instances()
    formatted_instances = []
    for instance in instances:
        formated_instance = format_instance_and_filename(instance)
        formatted_instances.append(formated_instance)
    return formatted_instances

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