import sys

import pandas as pd

sys.path.append('./service')
from pyadomd import Pyadomd


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
    result = con.cursor().execute(dax_query)
    return pd.DataFrame(result.fetchall())
