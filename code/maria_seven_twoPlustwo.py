from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors


def DataBase() : 
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
                CREATE TABLE seven_TwoPlusOne (
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
                DROP TABLE seven_TwoPlusOne
    '''
            cursor.execute(sql)
        conn.commit()
        with conn.cursor() as cursor:
            sql = '''
                CREATE TABLE seven_TwoPlusOne (
                    item_img varchar(255) NOT NULL,
                    item_name varchar(255) NOT NULL,
                    item_price varchar(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    '''
            cursor.execute(sql)
        conn.commit()


    print('db is ready')

# ----------------------------------------------------

array_2 = []
array_2_price = []
array_2_img = []


url = 'http://www.7-eleven.co.kr/product/presentList.asp'

driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


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

   

def two() :
    more(2)
    # 더보기 페이지 끝까지 펼침


    # get name
    prodName_two = driver.find_elements_by_class_name("name")
    for name in prodName_two :
        array_2.append(name.text)
     

    # get price
    prodPrice_two = driver.find_elements_by_class_name("price")
    for price in prodPrice_two :
        array_2_price.append(price.text)
 
    # get img
    prodImg_two = driver.find_elements_by_css_selector('li > div > img')
    for img in prodImg_two :
        url = img.get_attribute('src')
        array_2_img.append(url)
    prodImg_two = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/div/div/img')
    for img in prodImg_two :
        url = img.get_attribute('src')
        array_2_img.append(url)

        
    count = 0
    while count < len(array_2_price) :
        array_2_price[count] = array_2_price[count].replace('원','')
        array_2_price[count] = int(array_2_price[count].replace(',',''))
        count = count +1

        
    print(len(array_2))
    print(len(array_2_price))
    print(len(array_2_img))
        
        


driver.execute_script("fncTab('2');")# 2+1 탭 이동 후 상품 추출
print('go to 2+1 event')  
two()




