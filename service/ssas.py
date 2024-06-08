import json
import sys

import clr
import pandas as pd

sys.path.append('./service')
from pyadomd import Pyadomd
import os

dll_name = "Microsoft.AnalysisServices.Tabular.DLL"

try:
    clr.AddReference(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dll_name))
except:
    clr.AddReference(os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name))

import Microsoft.AnalysisServices.Tabular as Tabular


def list_running_ssas():
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
    connection_string = f'Provider=MSOLAP;Data Source={port_number};'
    con = Pyadomd(connection_string)
    con.open()
    return con


def close_connection(con):
    con.close()


def run_query(con, dax_query):
    cursor = con.cursor().execute(dax_query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[column[0] for column in cursor.description])
    cursor.close()
    return df


def get_model_bim(port_number):
    server = Tabular.Server()
    server.Connect(port_number)
    database = server.Databases[0]
    script = Tabular.JsonScripter.ScriptCreate(database)
    json_file = json.loads(script)
    edited = json_file['create']['database']
    raw_json = json.dumps(edited, indent=2)
    return raw_json
