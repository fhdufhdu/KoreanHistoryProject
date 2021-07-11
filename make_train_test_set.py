from random import random, randrange
from save_files import load_json, save_json, save_file
from sklearn.model_selection import train_test_split

raw_data_dict = load_json('history_1.json')
#'{}␞{}'
document_list = [list_elem['document'].replace('\n', '').replace('            ', '') for list_elem in raw_data_dict['list']]

x_train, x_valid, _, _ = train_test_split(
    document_list, document_list, test_size=0.2, shuffle=True, random_state=34)

save_file('train.txt', text_list=x_train)
save_file('test.txt', text_list=x_valid)
