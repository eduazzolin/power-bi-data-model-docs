import json
import sys

import clr
import pandas as pd
import os

sys.path.append('./service')
from pyadomd import Pyadomd

dll_name = "Microsoft.AnalysisServices.Tabular.DLL"

try:
    clr.AddReference(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dll_name))
except:
    clr.AddReference(os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name))

import Microsoft.AnalysisServices.Tabular as Tabular


def list_running_ssas():
    """
    Search for running SSAS instances and return a list of instances.
    :return: list of string like 'localhost:port_number'
    """
    import psutil
    instances = []
    tcp_connections = psutil.net_connections(kind='tcp')
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == 'msmdsrv.exe':
            for conn in tcp_connections:
                if conn.pid == proc.info['pid'] and conn.status == psutil.CONN_LISTEN:
                    port = conn.laddr.port
                    instances.append('localhost:' + str(port))
                    break
    return instances


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
