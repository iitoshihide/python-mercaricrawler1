
import os

from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import urllib.request
import sys
import linecache

import mysql.connector

import subprocess
from operator import itemgetter
import shutil

from keras.models import load_model
import numpy as np
import csv
import glob


aBrandWatch = {1816:"breitling"}


def downloadFile(url, path1, title):
    if os.path.exists(path1 + "\{0}".format(title)) == False :
        urllib.request.urlretrieve(url, path1 + "\{0}".format(title))


def loginGoogle(driver, email, password):
    driver.get('https://accounts.google.com')
    time.sleep(1.5)
    driver.find_element_by_xpath("//*[@id='identifierId']").send_keys(email)
    driver.find_element_by_xpath("//*[@id='identifierNext']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(password)
    driver.find_element_by_xpath("//*[@id='passwordNext']").click()
    time.sleep(5)


def loginMercari(driver, driver2, email, password):

    driver2.get("https://www.mercari.com/jp/login/")
    time.sleep(1.5)
    driver2.find_element_by_xpath("//*[@id='google-login']").click()
    time.sleep(2)


def getMercariContents(driver, driver2, cnx, market, brand):
    if not os.path.exists("D:\ImageOrder\src\{0}".format(market)):
        os.mkdir("D:\ImageOrder\src\{0}".format(market))
    if not os.path.exists("D:\ImageOrder\src\{0}\{1}".format(market, brand)):
        os.mkdir("D:\ImageOrder\src\{0}\{1}".format(market, brand))
    if not os.path.exists("D:\ImageOrder\dist\{0}".format(market)):
        os.mkdir("D:\ImageOrder\dist\{0}".format(market))
    if not os.path.exists("D:\ImageOrder\dist\{0}\{1}".format(market, brand)):
        os.mkdir("D:\ImageOrder\dist\{0}\{1}".format(market, brand))

    # l-container
    objs1 = driver.find_elements_by_class_name("items-box")
    
    print("market:" + str(market) + " brand:" + str(brand) + " start")

    count = 0
    for obj1 in objs1:    
            try:           
                count = count + 1
                print("count:" + str(count) + " / " + str(len(objs1)))     
                obj2 = obj1.find_elements_by_tag_name("a")
                confirmHref = obj2[0].get_attribute("href")
                print(confirmHref)

                obj3 = obj1.find_element_by_class_name("items-box-name")
                title = obj3.text
                print("title:" + title)

                obj4 = obj1.find_element_by_class_name("items-box-price")
                price = obj4.text[1:]
                price = price.replace(',', '')
                print("price:" + price)
                likes = "0"
                print("likes:" + likes)

                posConfirmHref = confirmHref.find("?_s=")
                print("posConfirmHref:" + str(posConfirmHref))
                if posConfirmHref == -1:
                    continue
                else:    
                    confirmHref = confirmHref[:posConfirmHref]
                    print(confirmHref)

                pagePreHref = "https://item.mercari.com/jp/"
                itemId = confirmHref.replace(pagePreHref, "")
                itemId = itemId.replace("/", "")
                photosHref = "https://static-mercari-jp-imgtr2.akamaized.net/photos/"
                itemPhotosHref = photosHref + itemId
                aitemPhotosHref = []
                aitemPhotosHref.append(itemPhotosHref + "_1.jpg")

                isExist = 0
                path1 = "D:\ImageOrder\src\{0}\{1}".format(market, brand) + "\\" + itemId.replace("m", "")
         
                if os.path.exists(path1) == True :
                    isExist = 1

                path2 = "D:\ImageOrder\dist\{0}\{1}".format(market, brand) + "\\" + itemId.replace("m", "")
                if os.path.exists(path2) == True :
                    isExist = 1


                if isExist == 0 :                     
                    os.mkdir(path1)
                    downloadFile(aitemPhotosHref[0], path1, itemId + "_1.jpg")

                    detectFlg = 0
                    detectItem = ""
                    bidFlg = 0
                    
                    connected = cnx.is_connected()
                    if (not connected):
                        cnx.ping(True)

                    #market, brand, confirmHref, title, price, likes, detectFlg, detectItem, bidFlg
                    #you can save above field as the result of crawling
                    

            except Exception as e:
                print("not found")



def searchMercari(driver, driver2, cnx):    

    market = 1
    for key in aBrandWatch:
        brand = key
        driver.get("https://www.mercari.com/jp/brand/" + str(brand) + "/")
        getMercariContents(driver, driver2, cnx, market, brand)


if __name__ == '__main__':

    email = 'hogeemail.com'
    password = 'hogeemailpassword'
    driver = webdriver.Chrome("c:/driver/chromedriver.exe")
    driver2 = webdriver.Chrome("c:/driver/chromedriver.exe")

    loginGoogle(driver2, email, password)    
    loginMercari(driver, driver2, email, password) 

    config = {
        'user': 'hogeuser',
        'password': 'hogepassword',
        'host': 'hogehost',
        'database' : 'hogedb',
    }
    cnx = mysql.connector.connect(**config)

    searchMercari(driver, driver2, cnx)

    cnx.close()

    driver.quit()
    driver2.quit()

  


