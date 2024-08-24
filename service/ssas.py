import datetime
import json
import os
import sys

import clr
import pandas as pd
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



def list_running_instances():
    """
    Retrieves a list of running Power BI Desktop SSAS instances, along with associated .pbix or .pbip files and the localhost port.

    Returns:
        list of dict: A list where each dictionary contains information about a running SSAS instance:
            - 'instance' (str): The local host and port number where the SSAS instance is running (e.g., 'localhost:12345').
            - 'file_name' (str): The name of the associated .pbix or .pbip file being used by the instance. If no such file is found, defaults to 'Semantic Model'.
            - 'start_time' (str): The start time of the process in 'YYYY-MM-DD HH:MM:SS' format.

    Example:
        [
            {
                'instance': 'localhost:12345',
                'file_name': 'Example.pbix',
                'start_time': '2024-08-23 14:15:30'
            },
            ...
        ]

    Notes:
        - This function relies on the `psutil` module to iterate over running processes and identify Power BI Desktop instances (`PBIDesktop.exe`).
        - It checks the command-line arguments of each process to find associated .pbix or .pbip files.
        - The function identifies the port by examining established network connections.
        - If multiple Power BI Desktop instances are running, each instance is returned as a separate entry in the list.
    """
    instances = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline', 'create_time']):

        if proc.info['name'] == 'PBIDesktop.exe':

            port = None
            name = 'Semantic Model'
            start_time = datetime.datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')

            for conn in proc.connections():
                if conn.status == psutil.CONN_ESTABLISHED:
                    port = conn.raddr.port
                    break

            for arg in proc.info['cmdline']:
                if arg.endswith('.pbix') or arg.endswith('.pbip'):
                    name = os.path.basename(arg)
                    break

            instances.append({
                'instance': f'localhost:{port}',
                'file_name': name,
                'start_time': start_time
            })

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