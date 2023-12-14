import pandas as pd
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from query import query as selectquery
from Connection import get_all
from personalitat_holland import solve_Holland
from User import User
from Degree import Degree
        

#Let's test the code by creating a user and calling the function get_degrees
user = User(["I","S"])
user.get_degrees()

#Now we save the degrees in a file called degrees.txt and if the file exists just erase it and create a new one
with open("degrees.txt", "w", encoding='utf-8') as file:
    file.write("")
for i in range(len(user._degrees)):
    with open("degrees.txt", "a", encoding='utf-8') as file:
        file.write(str(user._degrees[i]))
        file.write("\n")

