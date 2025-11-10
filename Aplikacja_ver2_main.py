import utils as u
import os   
         
def main():
    print('Provide data about your employee:\n')
    
    data_frame, data_list, column_name = u.store_data(os.path.dirname(os.path.realpath(__file__)) + '/Dane.csv')
    
    probability_list, probability_dictionary = u.specify_list_of_probabilities(data_frame, data_list, column_name)
    
    probability_cleared = u.count_final_probability(probability_list)
    
    u.give_recommendations(probability_cleared, probability_dictionary)
    

main()
