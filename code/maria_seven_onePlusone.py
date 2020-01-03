from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors

hostName = 'donggi.c4jpx1idd7lu.ap-northeast-1.rds.amazonaws.com'
userName = 'donggidonggi'
passWord = 'ehdrlehdrl1996^^'
# ---------- ready for DB ---------- 

conn = pymysql.connect(host= hostName,
                       port = 3306,
                       user= userName ,
                       password= passWord,
                       db='o2',
                       charset='utf8')

try:
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE seven_OnePlusOne (
                item_img varchar(255) NOT NULL,
                item_name varchar(255) NOT NULL,
                item_price varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()

except :
    print('already exists')
    with conn.cursor() as cursor:
        sql = '''
            DROP TABLE seven_OnePlusOne
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE seven_OnePlusOne (
                item_img varchar(255) NOT NULL,
                item_name varchar(255) NOT NULL,
                item_price varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()


print('db is ready')


# ------------------------------------------------------- 
url = 'http://www.7-eleven.co.kr/product/presentList.asp'

driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

array_1 = [] # name
array_1_price = [] # price
array_1_img = [] # img url

array_2 = []
array_2_price = []
aray_2_img = []

# ----------- extract data from Seven-Eleven ----------- 


def more(num) :  # num+1에서의 더보기 버튼 클릭
    count=0
    driver.execute_script("fncTab('1');")
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


    # get name
    prodName_one = driver.find_elements_by_class_name("name")
    for name in prodName_one :
        array_1.append(name.text)
     

    # get price
    prodPrice_one = driver.find_elements_by_class_name("price")
    for price in prodPrice_one :
        array_1_price.append(price.text)


 
    # get img
    prodImg_one = driver.find_elements_by_css_selector('li > div > img')
    for img in prodImg_one :
        url = img.get_attribute('src')
        array_1_img.append(url)
    prodImg_one = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/div/div/img')
    for img in prodImg_one :
        url = img.get_attribute('src')
        array_1_img.append(url)
        

        

print('go to 1+1 event')  
one()

#sql = "insert into seven_OnePlusOne(item_img,item_name,item_price) values(%s, %s, %s)"

#with conn.cursor() as cursor:
#    for a in range(0, len(array_1)):
#        cursor.execute(sql,(array_1_img[a],array_1[a],array_1_price[a]))
#conn.commit()
#conn.close()
