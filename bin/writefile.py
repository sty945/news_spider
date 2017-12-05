from homework1 import item_info
import codecs
import os
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\contents\\'

def write_single_file(file):
    num = 0
    i = 0
    file = codecs.open(file, 'w+', 'utf-8')
    for data in item_info.find():
        try :
            i += 1
            #link = data["link"]
            month = data["month"]
            if '11' in month:
                content = data['content']
                file.write(content)
        except:
            num += 1
            print("error:" + str(num) + " num:" + str(i) + " " + str(data["_id"]))
    file.close()

def write_all_file(start_num, end_num):
    for i in range(start_num, end_num):
        if i < 10:
            file_name = '0' + str(i)
        else:
            file_name = str(i)
        file_name += 'content'
        file = path + file_name + '.txt'
        write_single_file(file)
print(path)
write_all_file(11, 12)

