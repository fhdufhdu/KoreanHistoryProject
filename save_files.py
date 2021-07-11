import json

# %%


def save_json(file_name, dict_):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(dict_, file, indent='\t')


def load_json(file_name):
    dict_ = None
    with open(file_name, 'r') as file:
        dict_ = json.load(file)
    return dict_


def save_file(file_name, text='', text_list=None):
    f = open(file_name, 'w')
    f.write(text)
    if text_list != None:
        for text_elem in text_list:
            f.write(text_elem)
            f.write('\n')
    f.close()
