#!/usr/bin/env python3

import cgi
import cgitb
from string import Template
import pymysql
import json
import sys
from datetime import datetime
import pandas as pd
from io import BytesIO
import numpy as np

# Enable CGI traceback for debugging
cgitb.enable()

# Print the HTTP header
print("Content-Type: application/json\n")

# Parse form data
#form = cgi.FieldStorage()

def sanitize_input(input_str):
    sanitized_str = ""
    for char in input_str:
        if char:
            if char.isalnum():
                sanitized_str += char
            else:
                sanitized_str += "_"
        else:
            char = None
    return sanitized_str
    
def delete_data(mouse_str, table_name):
  for mouseid in mouse_str:
    if table_name == "BreedingLog":
        delete_query = f"DELETE FROM {table_name} WHERE Stud/M = (%s)"
        cursor.execute(delete_query, mouseid)
        print("Testing:", delete_query, mouseid)
        
        delete_query = f"DELETE FROM {table_name} WHERE Dam/F = (%s)"
        cursor.execute(delete_query, mouseid)
        print("Testing:", delete_query, mouseid)
        
    elif table_name:
        delete_query = f"DELETE FROM {table_name} WHERE mouseID = (%s)"
        cursor.execute(delete_query, mouseid)
        print("Testing:", delete_query, mouseid)

try:
    connection = pymysql.connect(
        host='bioed.bu.edu', 
        user='mchang15',
        password='bmms12s091', 
        db='mchang15',
        port=4253
    ) 
except pymysql.Error as e: 
        print(str(e))
        
# Create a cursor object
cursor = connection.cursor()

# Read form data from standard input
try:
    form_data = sys.stdin.read()
    if not form_data:
        raise ValueError("No data received")
    form = json.loads(form_data)
except json.JSONDecodeError as e:
    print(json.dumps({'error': 'Invalid JSON data: ' + str(e)}))
    sys.exit(1)
except Exception as e:
    print(json.dumps({'error': str(e)}))
    sys.exit(1)
    
try:
    if 'mouseIDs' in form:
        # Get the filteredData from the form
        mouse_ids_str = form.get('mouseIDs')
        print(mouse_ids_str)
        table_name = form.get('strainName')
        print(table_name)
        if mouse_ids_str:
            delete_data(mouse_ids_str, table_name)
            
        connection.commit()
        cursor.close()
        connection.close()
      
except pymysql.Error as e:
      print(str(e))
