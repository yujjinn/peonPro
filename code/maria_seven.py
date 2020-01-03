from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors

# ---------- extract data from Seven-Eleven ----------
url = 'http://www.7-eleven.co.kr/product/presentList.asp'

driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

array_1 = [] # name
array_1_price = [] # price
array_1_img = [] # img url


def more(num) :  # num+1에서의 더보기 버튼 클릭
    count=0
    while True :
        time.sleep(1)
        driver.execute_script("fncMore("+str(num)+");")
        time.sleep(1)
        try :
            more = driver.find_element_by_xpath('//*[@id="moreImg"]/a/span')
            if more.text == 'MORE' :
                count = count +1
        except :
            break
    print('총 페이지 ', count)



def one() :
    more(1)
    # 더보기 페이지 끝까지 펼침

    a = 0
    # get name
    prodName_one = driver.find_elements_by_class_name("name")
    for name in prodName_one :
        array_1.append(name.text)
        a= a+1
    print('총 개수 ', a)

    a = 0
    # get price
    prodPrice_one = driver.find_elements_by_class_name("price")
    for price in prodPrice_one :
        array_1_price.append(price.text)
        a = a+1
    print('총 개수 ' , a)

    a=0
    # get img
    prodImg_one = driver.find_elements_by_css_selector('li > div > img')
    for img in prodImg_one :
        url = img.get_attribute('src')
        array_1_img.append(url)
        a= a+1
    prodImg_one = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/div/div/img')
    for img in prodImg_one :
        url = img.get_attribute('src')
        array_1_img.append(url)
        a = a+1
    print('총 개수 ' , a)





driver.execute_script("fncTab('1');")# 1+1 탭 이동 후 상품 추출
print('go to 1+1 event')
one()

# 결과물 출력
count=0
print('get name')
while count <len(array_1):
    print(array_1[count])
    count = count +1
print("-----------------------------\n")

count=0
print('get price')
while count <len(array_1_price):
    print(array_1_price[count])
    count = count +1
print("-----------------------------\n")

count = 0
print('get img url')
while count <len(array_1_img):
    print(array_1_img[count])
    count = count +1
print("-------------end-------------\n")





# ---------- save as a DB system ----------


conn = pymysql.connect(host='localhost',
                       user='root',
                       password='비밀번호',
                       db='',
                       charset='utf8')


try:
    with conn.cursor() as cursor:
        sql = 'CREATE DATABASE dongiDB'
        cursor.execute(sql)
    conn.commit()
except :
    with conn.cursor() as cursor:
        sql = 'DROP DATABASE dongiDB'
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        sql = 'CREATE DATABASE dongiDB'
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()

print('create DataBase')



conn = pymysql.connect(host='localhost',
                       user='root',
                       password='비밀번호',
                       db='MariaDB',
                       charset='utf8')

try:
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE item (
                item_name varchar(255) NOT NULL,
                item_price int NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()
