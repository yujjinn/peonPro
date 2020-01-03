from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import pymysql.cursors


hostName = '호스트명'
userName = '사용자명'
passWord = '비밀번호'

array_dum = []
array_dum_price = []
array_dum_img = []

array = []
array_price = []
array_img = []
url = 'http://www.7-eleven.co.kr/product/presentList.asp'

driver = webdriver.Chrome('chromedriver')
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


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
            CREATE TABLE seven_Dum (
                item_img varchar(255) ,
                item_name varchar(255) ,
                item_price varchar(255) ,
                item_dum_img varchar(255) ,
                item_dum_name varchar(255),
                item_dum_price varchar(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()

except :
    print('already exists')
    with conn.cursor() as cursor:
        sql = '''
            DROP TABLE seven_Dum
'''
        cursor.execute(sql)
    conn.commit()
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE seven_Dum (
                item_img varchar(255) ,
                item_name varchar(255) ,
                item_price varchar(255) ,
                item_dum_img varchar(255) ,
                item_dum_name varchar(255),
                item_dum_price varchar(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()


print('db is ready')


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
                print(count)
        except :
            break

    print('총 페이지 ', count)


def dum() :

    more(3)


    # get name
    prodName = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[1]/div/div/div[1]')
    for name in prodName :
        array.append(name.text)


    # get price
    prodPrice = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[1]/div/div/div[2]/span')
    for price in prodPrice :
        array_price.append(price.text)

    # get img
    #prodImg_two = driver.find_elements_by_css_selector('li > div > img')
    #for img in prodImg_two :
    #    url = img.get_attribute('src')
    #    array_dum_img.append(url)
    prodImg = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[2]/div/img')
    for img in prodImg :
        url = img.get_attribute('src')
        array_img.append(url)


    # get dum name
    prodName_dum = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[2]/div/div/div[1]')
    for name in prodName_dum :
        array_dum.append(name.text)


    # get dum price
    prodPrice_dum = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[2]/div/div/div[2]/span')
    for price in prodPrice_dum :
        array_dum_price.append(price.text)

    # get dum img
    #prodImg_dum = driver.find_elements_by_css_selector('li > div > img')
    #for img in prodImg_dum :
    #    url = img.get_attribute('src')
    #    array_dum_img.append(url)
    prodImg_dum = driver.find_elements_by_xpath('//*[@id="listUl"]/li[*]/a[2]/div/img')
    for img in prodImg_dum :
        url = img.get_attribute('src')
        array_dum_img.append(url)



driver.execute_script("fncTab('3');")# 2+1 탭 이동 후 상품 추출
print('go to dum event')
dum()


print('본품')
print(array)
print(array_price)
print(array_img)
print('증정품')
print(array_dum)
print(array_dum_price)
print(array_dum_img)


print(len(array))
print(len(array_price))
print(len(array_img))
print(len(array_dum))
print(len(array_dum_price))
print(len(array_dum_img))

#sql = "insert into seven_Dum(item_img,item_name,item_price,item_dum_img, item_dum_name, item_dum_price) values(%s, %s, %s,%s, %s, %s)"


#with conn.cursor() as cursor:
#    for a in range(0, len(array)):
#        cursor.execute(sql,(array_img[a], array[a],array_price[a],array_dum_img[a],array_dum[a],array_dum_price[a]))
#conn.commit()
#conn.close()
