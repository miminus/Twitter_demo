#coding=utf-8
import time
import sys
import MySQLdb as mdb
import os,chardet
from selenium import webdriver
import urllib2,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import math
print 'start'

#################################################
db = mdb.connect(host="localhost",user="root",passwd="minus",db="new_opinion",charset="utf8" )
cur=db.cursor()
###############################################

homepage=sys.argv[1]
#f=open('C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\user_main.txt','wb')
#homepage=sys.argv[1]
#homepage='http://weibo.com/u/'+homepage
#homepage='http://weibo.com/kaifulee'

reload(sys) 
sys.setdefaultencoding('utf8')

#time.sleep(8)
#WebDriverWait(driver, 10)..until(EC.presence_of_element_located((By.ID,'someid')))
while True:
	try:
		driver=webdriver.Ie()
		#driver.implicitly_wait(10)
		print 'go in'
		driver.get(homepage)
		time.sleep(2)
		element = WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID,"plc_main")))
		print 'ok'
		#print element
		flag=0
		print 'here'
		# try:
		main_area=driver.find_element_by_id('plc_main')
		head_area=driver.find_element_by_class_name('photo_wrap')
		gender_area=driver.find_element_by_class_name('pf_username')     
		person_message_area=driver.find_element_by_class_name('ul_detail')
		driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')

		# except:
			# main_area=driver.find_element_by_class_name('PRF_profile_header')
			# flag=1
		break
	except:
		driver.quit()
		continue
content=main_area.get_attribute('outerHTML')
head=head_area.get_attribute('outerHTML')
gender=gender_area.get_attribute('innerHTML')
person_message=person_message_area.get_attribute('innerHTML')

content=content.encode('utf-8')
head=head.encode('utf-8')
gender=gender.encode('utf-8')
per_mess=person_message.encode('utf-8')


soup=BeautifulSoup(content)
# f=open('d:/aa.txt','wb')
# f.write(content)
# f.close()
if flag==0:
	#f.write(soup.prettify())
	#f.close()
	content=soup.prettify()
	#############解析开始#########################
	uid_pattern=re.compile('src="http://.*?sinaimg.cn/(\d+)/',re.S)
	user_pattern=re.compile('alt=(.*?)src')
	user_image_pattern=re.compile('src="(http://tp\d{1}.sinaimg.cn/.*?/[01])"',re.S)
	
	per_mess_pattern=re.compile(r'<span class="item_text W_fl">.*?</li>',re.S)
	sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)	
	class_pattern=re.compile(r'Lv.(\d+)',re.I)
	digit_pattern=re.compile(r'>\s*(\d+)\s*<',re.S)
	#aa='(\d+)\s*<.*?>\s*<.*?>\s*关注'.decode('gbk').encode('utf-8')
	#followee_pattern=re.compile(aa,re.S)
	#follower_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*粉丝',re.S)
	#postnum_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*微博',re.S)
	#################################################################
	uid=re.findall(uid_pattern,head)[0]
	#print uid
	user=re.findall(user_pattern,head)[0].strip()
	#print user
	user_image=re.findall(user_image_pattern,head)[0]
	#print user_image
	if 'female' in gender:
		gender_sex='female'
	else:
		gender_sex='male'
	#print gender_sex
	
	per_message=re.findall(per_mess_pattern,content)
	message=''
	for m in per_message:
		m= m.replace('\n','')
		m= m.replace(' ','')
		m= re.sub(sub_p_1,' ',m)  
		
		message+=m
	#print message
	strongs=soup.find_all('strong')
	dig=[]
	for i in strongs:
		try:
			a=re.findall(digit_pattern,str(i))[0]
			print a
			dig.append(a)
		except:
			pass
	followee_num=dig[0]
	follower_num=dig[1]
	posts_num=dig[2]
	

	_class=re.findall(class_pattern,content)[0]
	print _class
##########################################################
##########################################################
##########################################################
driver.quit()
query='insert ignore into weibo_user (user_id,user_name,user_image,gender,message,class,post_num,follower_num,followee_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
params=(uid,user,user_image,gender_sex,message,_class,posts_num,follower_num,followee_num)			
cur.execute(query,params)
db.commit()

#####################访问关注与粉丝#############################
follower_url='http://weibo.com/'+uid+'/fans?page='
followee_url='http://weibo.com/'+uid+'/follow?page='

follower_page=int(math.ceil(float(int(follower_num)/20.0)))
followee_page=int(math.ceil(float(int(followee_num)/20.0)))

if follower_page>5:
	follower_page=5
if followee_page>5:
	followee_page=5
if posts_num>100:
	post_page=3
else:
	post_page=int(math.ceil(float(int(posts_num)/45.0)))
	
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\follower.py %s %d %s %s' %(follower_url,follower_page,uid,user))
time.sleep(4)
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\followee.py %s %d %s %s' %(followee_url,followee_page,uid,user))
time.sleep(4)
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\userpost.py %s %d' % (uid,post_page))
time.sleep(4)
###################################################















