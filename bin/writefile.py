from news_spider import item_info
import codecs
import os

def write_context(file_name, month_name='01'):
    file = codecs.open(file_name, 'w+', 'utf-8')
    num = 0
    i = 0
    for data in item_info.find():
        try:
            i += 1
            month = data["date"]["month"]
            if month_name in month:
                content = data["content"]
                file.write(content)
        except:
            num += 1
            print("error:" + str(num) + " num:" + str(i) + " " + str(data["_id"]))
    file.close()

if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\contents\\'
    print(path)
    month_name = '03'
    file_name = path + month_name + '_content.txt'
    print(file_name)
    write_context(file_name, month_name)
