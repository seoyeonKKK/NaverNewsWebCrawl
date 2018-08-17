from bs4 import BeautifulSoup
import urllib.request
import re
from IPython.display import display
import pandas as pd
import numpy as np

# 출력 파일 명
OUTPUT_FILE_NAME = 'output.txt'
CLEAR_FILE_NAME = 'clear.txt'
# 긁어 올 URL
URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055&aid=0000445667'

# 크롤링 함수
def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser', from_encoding='EUC-KR')
    text = ''
    for item in soup.find_all('div', id='articleBodyContents'):
        text = text + str(item.find_all(text=True))
    return text

# 클리닝 함수
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text

# 메인 함수
def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()
    read_file = open(OUTPUT_FILE_NAME, 'r')
    write_file = open(CLEAR_FILE_NAME, 'w')
    text = read_file.read()
    text = clean_text(text)
    df = []
    #dataframe
    df = pd.DataFrame(data = np.array([[text.count('신선'), text.count('시원'), text.count('혹독한'), text.count('만')]]), columns=['신선', '시원', '혹독한', '만'])
    display(df)
    #tocsv
    df.to_csv("crawl.csv", mode='a', header='false')
    print('\n')

    #series
    my_series = pd.Series({"선선": text.count('선선'), "시원": text.count('시원'), "혹독한": text.count('혹독한'), "만": text.count('만')})
    display(pd.DataFrame(my_series))
    print('\n')
    
    #dict
    my_dict = {"선선": [text.count('선선')], "시원": [text.count('시원')], "혹독한": [text.count('혹독한')], "만": [text.count('만')]}
    display(pd.DataFrame(my_dict))
    print('\n')
    # write_file.write(text)
    read_file.close()
    write_file.close()

if __name__ == '__main__':
    main()