#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 20:21:47 2023

@author: ninalanzarivera
"""

import pandas as pd

def solve_Holland(file: str, top = 2):
    '''
    Parameters
    ----------
    file : str
        Archivo txt con las soluciones a cada pregunta del TH, donde cada pregunta se almacenará en una linea distinta.
            Formato de las respuestas según la pregunta
                A) Lista numérica de los índices de los atributos seleccionados.
            	B & C ) Lista numérica de los índices de las respuestas iguales a 'A'
            	D ) Lista de los caracteres seleccionados como respuestas.
                	* Los valores de cada lista deben estar separados por coma

    top : int, optional
        Número de Tipos de Vocación que deseamos como solución. The default is 2.

    Returns
    -------
    solution : list
        Lista de caracteres (inicial de los distintos Tipos de Vocación según el TH.
            Options:
                'R': REALISTA
                'I': INVESTIGADORA
                'S': SOCIAL
                'C': CONVENCIONAL
                'E': EMPRENDEDORA
                'A': ARTÍSTICA

    '''
    assert type(file) == str
    assert type(top) == int
    assert top <= 6
    
    inputs = []
    
    with open(file, 'r') as archivo:    
        for line in archivo.readlines():
            input_line = line.split(',')
            try:
                input_line.remove('\n')
            except:
                pass
            try:
                input_line = [int(valor) for valor in input_line]
            except:
                pass
            inputs.append(input_line)
    
    sol_A = pd.DataFrame({'R': [3,11,18,21,24,27,35,44],
                   'I': [8,19,29,31,33,36,37,43],
                   'S': [4,14,15,16,17,22, 0, 0],
                   'C': [5,6,7,9,10,26,28,42],
                   'E': [2,12,23,32,38,39,40,41],
                   'A': [1,13,20,25,30,34,45, 0]
                   })

    sol_B = pd.DataFrame({'R': [1,10,16],
                      'I': [9,13,14],
                      'S': [5,8,17],
                      'C': [3,4,18],
                      'E': [7,12,15],
                      'A': [2,6,11]
                      })

    sol_C = pd.DataFrame({'R': [2,5,12],
                      'I': [4,9,10],
                      'S': [3,14,18],
                      'C': [1,8,13],
                      'E': [6,7,17],
                      'A': [11,15,16]
                      })

    sol_D = pd.DataFrame({'R': ['E', 'F', 'C', 'B', 'D'],
                      'I': ['A', 'C', 'E', 'F', 'C'],
                      'S': ['D', 'E', 'A', 'E', 'F'],
                      'C': ['B', 'A', 'F', 'D', 'B'],
                      'E': ['C', 'D', 'B', 'A', 'E'],
                      'A': ['F', 'B', 'D', 'C', 'A']
                      })
    
    result = pd.DataFrame(columns = ['PA', 'PB', 'PC', 'PD'])
    result['PA'] = sol_A.isin(inputs[0]).sum()
    result['PB'] = sol_B.isin(inputs[1]).sum()
    result['PC'] = sol_C.isin(inputs[2]).sum()
    
    cols = ['R', 'I', 'S', 'C', 'E', 'A']
    input_D_transform = pd.DataFrame(columns = cols)

    for i in cols:
        input_D_transform[i] = inputs[3]
    result['PD'] = (sol_D == input_D_transform).sum()
    result['TOTAL'] = result[['PA', 'PB', 'PC', 'PD']].sum(axis=1)
    
    solution = result.sort_values('TOTAL', ascending=False).head(top).index.to_list()
    
    return solution

