import pandas as pd
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential
from query import query as selectquery
from Connection import get_all
from personalitat_holland import solve_Holland
from Degree import Degree

class User():

    def __init__(self, tuple) -> None:
        self._tuple = tuple
        self._degrees = []
        self._P1 = ""
        self._P2 = ""
        self._P3 = ""
        self._P4 = ""
        self._academic_branch = []
        self._degrees = []
    
    def get_CL_CODES(self):
        print("Retrieving CL_CODES")
        query = selectquery("SELECT ISNULL(P1,'Z') as P1, ISNULL(P2,'Z') AS P2, ISNULL(P3,'Z') AS P3, ISNULL(P4,'Z') AS P4 FROM TiposVocacionales WHERE TipoVocacional_ID = '" + self._tuple[0] +"-" +self._tuple[1] + "'")
        result, columns = get_all(query)
        df = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
        self._P1 = df['P1'][0]
        self._P2 = df['P2'][0]
        self._P3 = df['P3'][0]
        self._P4 = df['P4'][0]

    def get_academic_branches(self):
        self.get_CL_CODES()
        print("Retrieving academic branches")
        query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_1 = '" + self._P1 + "'")
        result, columns = get_all(query)
        df_combined = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
        if len(df_combined) < 10:
            query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_2 = '" + self._P1 + "'")
            result, columns = get_all(query)
            df2 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
            df_combined = pd.concat([df_combined, df2], ignore_index=True)
            if len(df_combined) < 10:
                query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_1 = '" + self._P2 + "'")
                result, columns = get_all(query)
                df3 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                df_combined = pd.concat([df_combined, df3], ignore_index=True)
                if len(df_combined) < 10:
                    query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_2 = '" + self._P2 + "'")
                    result, columns = get_all(query)
                    df4 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                    df_combined = pd.concat([df_combined, df4], ignore_index=True)
                    if len(df_combined) < 10:
                        query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_1 = '" + self._P3 + "'")
                        result, columns = get_all(query)
                        df5 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                        df_combined = pd.concat([df_combined, df5], ignore_index=True)
                        if len(df_combined) < 10:
                            query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_2 = '" + self._P3 + "'")
                            result, columns = get_all(query)
                            df6 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                            df_combined = pd.concat([df_combined, df6], ignore_index=True)
                            if len(df_combined) < 10:
                                query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_1 = '" + self._P4 + "'")
                                result, columns = get_all(query)
                                df7 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                                df_combined = pd.concat([df_combined, df7], ignore_index=True)
                                if len(df_combined) < 10:
                                    query = selectquery("SELECT  distinct RamaAcademica_ID FROM RamasAcademicas WHERE CL_2 = '" + self._P4 + "'")
                                    result, columns = get_all(query)
                                    df8 = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
                                    df_combined = pd.concat([df_combined, df8], ignore_index=True)

        for i in range(len(df_combined)):
            self._academic_branch.append(df_combined['RamaAcademica_ID'][i])

    def get_degrees_list(self):
        self.get_academic_branches()
        print("Retrieving degrees list")
        for i in range(len(self._academic_branch)):
            query = selectquery("SELECT Grado_ID,Grado, Universidad, COD_UNI, Precio_anyo, Duracion,rama_academica_1 FROM dbo.MasterGrados1 WHERE rama_academica = '" + self._academic_branch[i] + "'")
            result, columns = get_all(query)
            df = pd.DataFrame.from_records(result, columns=[x[0] for x in columns])
            for j in range(len(df)):
                degree = Degree(df['Grado_ID'][j],df['Grado'][j],df['Universidad'][j],df['COD_UNI'][j],df['Precio_anyo'][j],df['Duracion'][j],df['rama_academica_1'][j])
                if degree not in self._degrees:
                    self._degrees.append(degree)
                    self._priority = i +  1
        for i in range(len(self._degrees)):
            if self._degrees[i]._rama_academica_1 in self._academic_branch:
                self._degrees[i]._priority = self._degrees[i]._priority - 1
        self._degrees.sort(key=lambda x: (x._priority, x._Precio_anyo))
        #Now crop the list of degrees to the top 6
        self._degrees = self._degrees[:6]

    def get_degrees(self):
        self.get_degrees_list()
        print("Top 6 degrees most relevant saved in degrees.txt")
        return self._degrees[:6]

