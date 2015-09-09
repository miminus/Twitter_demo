#coding=utf-8
import time,re
import sys,os,chardet
import MySQLdb as mdb
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

reload(sys)
sys.setdefaultencoding('utf-8')
#################################################
db = mdb.connect(host="localhost",user="root",passwd="minus",db="new_opinion",charset="utf8" )
cur=db.cursor()
#################################################
uid=sys.argv[1]
page_all=int(sys.argv[2])

post_id_pattern=re.compile(r'mid="(\d+)"')
sub_p_1=re.compile(r'<[^<>]*?>|\r\t',re.S)
post_time_pattern=re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
repost_pattern=re.compile(r'(\d*)\s*</span>')
like_pattern=re.compile(r'(\d*)\s*</em>')
##############################################################################################
baseurl='http://weibo.com/'+uid+'?is_search=0&visible=0&is_tag=0&profile_ftype=1&page='
poster_url='http://weibo.com/'+uid
page=1
driver=webdriver.Ie()
while page<=page_all:
	url=baseurl+str(page)
	page+=1
	driver.get(url)

	print driver.title

	driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')
	print '1'
	time.sleep(3)
	driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')
	print '2'
	time.sleep(3)
	driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')
	time.sleep(3)
	print '3'

	#lists_map=driver.find_element_by_xpath('//div[@idPl_Official_MyProfileFeed__18]')
	lists_map=driver.find_elements_by_xpath('//div[@tbinfo]')
	cnt=0
	for i in lists_map:
		content=i.get_attribute('outerHTML')
		soup=BeautifulSoup(content)
		con=soup.prettify()
		f=open('d:/aa.txt','wb')
		f.write(con)
		f.close()
		##############################################################################################
		###################################½âÎö²¿·Ö###################################################
		##############################################################################################
		#post_con_pattern=re.compile(r'<html>.*?</html>',re.S)


		#post_con=re.findall(post_con_pattern,)
		scratch_time=time.strftime('%Y-%m-%d %H:%M:%S')
		post_id=re.findall(post_id_pattern,con)[0]
		print post_id
		########################
		content=soup.find_all(attrs={"node-type":"feed_list_content"})
		content= str(content[0])
		content=re.sub(sub_p_1,'',content)
		content=content.replace(' ','')
		#print content
		########################
		post_time=soup.find_all(attrs={"node-type":"feed_list_item_date"})
		post_time=post_time[len(post_time)-1]
		post_time=str(post_time)
		post_time=re.findall(post_time_pattern,post_time)[0]
		#print post_time
		#######################
		inner_flag=0
		if 'class="WB_feed_expand"' in str(con):
			inner_flag=1
		#print inner_flag
		
		#######################
		repost=soup.find_all(attrs={"node-type":"forward_btn_text"})
		repost=str(repost[0])
		repost_num=re.findall(repost_pattern,repost)[0]
		if repost_num=='':
			repost_num=0
		repost_num=int(repost_num)
		#print repost_num
		#######################
		comment=soup.find_all(attrs={"action-type":"fl_comment"})
		comment=str(comment[0])
		comment_num=re.findall(repost_pattern,comment)[0]
		if comment_num=="":
			comment_num=0
		comment_num=int(comment_num)
		#print comment_num
		######################
		like=soup.find_all(attrs={"action-type":"fl_like"})
		like=str(like[len(like)-1])
		like_num=re.findall(like_pattern,like)[0]
		if like_num=="":
			like_num=0
		like_num=int(like_num)
		#print like_num
		query='insert ignore into user_post (post_id,post_time,content,poster_id,poster_url,repost_num,comment_num,inner_flag) values(%s,%s,%s,%s,%s,%s,%s,%s)'
		params=(post_id,post_time,content,uid,poster_url,repost_num,comment_num,inner_flag)
		cur.execute(query,params)
		db.commit()
		print '++++++++++++++++++++++++'
driver.quit()

