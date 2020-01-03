from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors


url = 'http://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N'
driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

array_name = []
array_price = []
array_img = []


hostName = '호스트명'
userName = '사용자명'
passWord = '비밀번호'

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
            CREATE TABLE cu_OnePlusOne (
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
            DROP TABLE cu_OnePlusOne
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE cu_OnePlusOne (
                item_img varchar(255) NOT NULL,
                item_name varchar(255) NOT NULL,
                item_price varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()


print('db is ready')


# -------------------------------------------------------

count= 1
def more(num) : # 더 보기 개수 찾기
    driver.execute_script("goDepth(23);")
    global count
    while True :
        time.sleep(1)
        driver.execute_script("nextPage(1);")
        time.sleep(1)
        try :
            more = driver.find_element_by_class_name('prodListBtn-e')
            if more.text == '맨위로' :
                count = count + 1
        except:
            break


more(1)
driver.execute_script("goDepth(23);")
a = 1
while a <= count :
    time.sleep(1)
    driver.execute_script("nextPage(1);")
    time.sleep(1)
    a = a +1


def one() :

    time.sleep(1)
    prodName = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[1]/a')
    for name in prodName :
        array_name.append(name.text)


    prodPrice = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/p[2]/span')
    for price in prodPrice :
        array_price.append(price.text)



    prodImg = driver.find_elements_by_xpath('//*[@id="contents"]/div[1]/div[2]/ul/li[*]/div/a/img')
    for img in prodImg :
        url = img.get_attribute('src')
        array_img.append(url)

one()


sql = "insert into cu_OnePlusOne(item_img,item_name,item_price) values(%s, %s, %s)"

with conn.cursor() as cursor:
    for a in range(0, len(array_name),1):
        cursor.execute(sql,(array_img[a],array_name[a],array_price[a]))
conn.commit()
conn.close()
