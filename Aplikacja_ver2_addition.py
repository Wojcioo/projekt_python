import numpy as np
import pandas as pd
from matplotlib import pyplot
import os

filename = os.path.dirname(os.path.realpath(__file__)) + '/Dane.csv'
data_frame = pd.read_csv(filename) 

user_value = [29, 3, 11, 10, 5, 0, 1, 3388, 2]


slownik = {}
for row in data_frame.itertuples():
    number_of_matches = 0
    
    for indeks, idx in enumerate([1,7,24,29,32,34,21,19,15]):
        if list(row)[idx] == user_value[indeks]:
            number_of_matches += 1

    slownik[list(row)[0]] = number_of_matches

new_slownik = {}
count_match = 0
for key, value in slownik.items():
    if value == max(slownik.values()):
        count_match +=1
        new_slownik[key] = value
        number_of_match = new_slownik[key]

print(new_slownik)
count_departure = 0
for key in new_slownik.keys():
    if data_frame['Attrition'][key] == 'Yes':
        count_departure +=1
        
probability = (count_departure/count_match) * 100
        
print(f'Znaleziono {count_match} dopasowań łącznie {number_of_match} parametrów, z których prawdopodobienstwo odejscia wynosi {probability}')