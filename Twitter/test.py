#coding=utf-8
import time
import sys
import os,chardet
from selenium import webdriver
import urllib2,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import MySQLdb as mdb

driver=webdriver.PhantomJS()
driver.get('https://twitter.com/search?q=Kim%20Jong-un&src=typd')
aa=driver.page_source
f=open('d:/mm.txt','wb')
f.write(aa)
f.close()
driver.quit()