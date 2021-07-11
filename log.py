def save_wrong_predict(dir_path, file_names, labels, predicts):
    wrong_cnt = 0
    wrong_txt = ''
    for path, list_elem, predict in zip(file_names, labels, predicts):
        if list_elem != predict:
            wrong_txt += '======================================================================================================================\n'
            wrong_txt += 'wrong predicted path : {}\noriginal value : {}\npredict value : {}\n'.format(path, list_elem, predict)
            wrong_cnt += 1
    wrong_txt += '======================================================================================================================\n'
    wrong_txt += 'wrong_cnt / test_set_length = {}'.format(wrong_cnt/len(labels))
    
    f = open('{}/wrong_predicted_log.txt'.format(dir_path), 'w')
    f.write(wrong_txt)
    f.close()
    
    return wrong_txt