### The application predicts the departure of an employee from your company based on the input data. 
### It also provides recommendations that can prevent this from happening.

import numpy as np
import pandas as pd
from matplotlib import pyplot
import math
import copy
import statistics as st
import re


## Data store
def store_data(filename):
    data_frame = pd.read_csv(filename)
    data_list = [['age', 18, 60],
                 ['education degree from 1 to 5: \n 1:Below College \n 2: College \n 3: Bachelor \n 4: Master \n 5: Doctor\n', 1, 5], 
                 ['percent Salary Hike from 11 to 25', 11, 25],
                 ['total_working years', 0, 40],
                 ['working years at company', 0, 40],
                 ['number years since last promotion', 0, 15],
                 ['number companies worked', 1, 9],
                 ['monthly income in USD', 1009, 19999],
                 ['job level from 1 to 5', 1, 5]]
    
    column_name = ['Age', 'Education', 'PercentSalaryHike', 'TotalWorkingYears', 'YearsAtCompany', 'YearsSinceLastPromotion',
             'NumCompaniesWorked', 'MonthlyIncome', 'JobLevel']
    return data_frame, data_list, column_name


##

def specify_list_of_probabilities(data_frame, data_list, column_name):
    probability_list = []
    probability_dictionary = {}    
    
    for indeks, info in enumerate(data_list):
        descriptor = info[0]
        min_value = info[1]
        max_value = info[2]
        
        user_value = get_employee_info(descriptor, min_value, max_value)
        p = get_departure_probability(user_value, column_name[indeks], data_frame)
        probability_list.append(p)
        probability_dictionary[column_name[indeks]] = p
        
    return probability_list, probability_dictionary

## Input data:
def get_employee_info(descriptor, minim, maxim):
    while True:
        a = input(f'Enter the {descriptor} the employee: \n')
        if (a.isdigit() and int(a) >= minim and int(a) <= maxim):
            return int(a)
        elif a == '':
            return 0.0
        print(f'Incorrect value, enter correct value - between {minim} - {maxim} or leave it blank')


# Check probability
def get_departure_probability(user_value, column_name, data_frame):
    group_size = data_frame[[column_name, 'EmployeeNumber']].groupby(by = column_name).count()
    group_size [column_name] = group_size.index.get_level_values(column_name)
    want_leave = data_frame[data_frame['Attrition'] == 'Yes'].groupby(by = column_name).count()
    group_size ["Want_leave"] = want_leave['Attrition']
    group_size = group_size.fillna(0.0)
    group_size['Probability_of_departure'] = group_size ["Want_leave"]/ group_size['EmployeeNumber']
#     print(group_size)
    p = check_equality(user_value, column_name, group_size)
    if p == None:
        k = int(math.sqrt(sum(group_size['EmployeeNumber'])))
        groups = pd.cut(group_size[column_name], bins = k)
        groups_2 = groups.values.unique()
        probablity = group_size.groupby(groups)['Probability_of_departure'].mean().fillna(0.0)
        for j in range(0, len(groups_2)):
            if (user_value in groups_2[j]) == True:
                p = probablity[j]
#                 print(f'Prawdopodobieństwo odejścia wynosi:{p}')
                break
    return p 

##Check equality value
def check_equality(user_value, column_name, group_size):
    for i in range(len(group_size[column_name])):
        if user_value == group_size[column_name].values[i]:
            p = group_size['Probability_of_departure'].values[i]
#             print(f'Prawdopodobieństwo odejścia wynosi:{p}')
            return p
    return None


## Count final probability
def count_final_probability(probability_list):
    probability_cleared = copy.copy(probability_list)
    probability_cleared = clear_list(probability_cleared, probability_list)
    final_probability = st.mean(probability_cleared)
    print('The probability of this employee leaving is approx {:.2%}'.format(final_probability))
    return probability_cleared
    

## Clear the list from extreme elements (0 and 1 and None)
def clear_list(probability_cleared, probability_list):
    for element in probability_list:
        if element == None or element == 1 or element == 0:
            probability_cleared.remove(element)
    return probability_cleared

    
## Recommendations

def give_recommendations(probability_cleared, probability_dictionary):
    probablity_minimum = min(probability_cleared)
    probablity_maxium = max(probability_cleared)
    check_min_factory(probablity_minimum, probability_dictionary)
    check_max_factory(probablity_maxium, probability_dictionary)
            

def check_min_factory(probablity_minimum, probability_dictionary):
    for key, value in probability_dictionary.items():
        if value == probablity_minimum:
            key = insert_spaces(key)
            a = print(f'The least important factory is {key}')


def check_max_factory(probablity_maximum, probability_dictionary):
    recommendation_list = ['', '', 'The employee received too low pay raises.', '',  '', 'The employee has not been promoted for a long time.',
    'An employee likes to change jobs often.', 'You should increase the employee\'s salary', 'The employee\'s job level is too low.']
    i = 0 
    for key, value in probability_dictionary.items():
        if value == probablity_maximum:
            key = insert_spaces(key)
            a = print(f'The problem is {key} of the employee.', recommendation_list[i])
            i += 1

## Put spaces between words starting with capital letters
def insert_spaces(key):
    key = re.sub("([A-Z])", " \\1", key).strip()
    return key
            
