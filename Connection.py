import pandas as pd
import os
import pyodbc, struct

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel



import os
import pyodbc, struct
from azure.identity import DefaultAzureCredential
from query import query


connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

def get_all(query):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = cursor.description
    return result, columns

def get_conn():
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

