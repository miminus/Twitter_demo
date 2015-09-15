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

print 'start'
##############################################################################
##############################################################################
db = mdb.connect(host="127.0.0.1",user="root",passwd="minus",db="twitter",charset="utf8" )
cur=db.cursor()
##############################################################################
##############################################################################
current_dir=os.path.dirname(sys.argv[0]).replace('\\','/')
#current_file=os.path.
##############################################################################
##############################################################################
def sec_to_time(s):
	return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(s))
##############################################################################
##############################################################################

reload(sys) 
sys.setdefaultencoding('utf8')
def main():
	f=open(r'd:/posts.txt','wb')
	driver = webdriver.Firefox()
	print 'go in'
	###############################翻页数###########################################
	scroll_time=5
	driver.get("https://twitter.com/search?f=realtime&q=happiness&src=typd")
	while scroll_time>0:
		driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')
		time.sleep(3)
		print 'new scroll'
		scroll_time-=1
	main_area=driver.find_element_by_id('stream-items-id')
	print main_area
	content=main_area.get_attribute('outerHTML')
	content=content.decode('utf-8','ignore').encode('gbk','ignore')
	##########################################################################

	soup=BeautifulSoup(content)
	f.write(soup.prettify().decode('utf-8','ignore').encode('gbk','ignore'))
	f.close()
	content=soup.prettify().decode('utf-8','ignore').encode('gbk','ignore')
	##########################################################################
	block_pattern=re.compile(r'(<li class="js-stream-item stream-item stream-item.*?<div class="dropdown">)',re.S)
	poster_pattern=re.compile(r'<strong class="fullname.*?>\s*(.*?)\s*</strong>',re.S)
	poster_img_pattern=re.compile(r'<img alt="" class="avatar js-action-profile-avatar" src="(https://pbs.twimg.com/.*?)">',re.S)
	post_con_pattern=re.compile(r'(<p class="js-tweet-text tweet-text".*?<div class="expanded-content js-tweet-details-dropdown">)',re.S)
	post_time_pattern=re.compile(r'data-long-form="true" data-time="(\d+)"',re.S)
	poster_id_pattern=re.compile(r'data-user-id="(\d+)"',re.S)
	post_id_pattern=re.compile(r'data-tweet-id="(\d+)"',re.S)
	poster_homepage_pattern=re.compile(r'data-user-id="\d+" href="(/\w+)">')

	area=r'class="ProfileTweet-actionCount" data-tweet-stat-count="(\d*)">'.decode('utf-8').encode('gbk')
	down_area_pattern=re.compile(area,re.S)
	a=r'<span class="ProfileTweet-actionCountForAria" data-aria-label-part="">\s*(.*?)\s*转推'.decode('utf-8').encode('gbk')
	repost_pattern=re.compile(a,re.S)
	aa=r'<span class="ProfileTweet-actionCountForAria">\s*(\d*)\s*回复'.decode('utf-8').encode('gbk')
	reply_pattern=re.compile(aa,re.S)
	aaa=r'<span class="ProfileTweet-action--favorite u-hiddenVisually">.*?<span class="ProfileTweet-actionCountForAria" data-aria-label-part="">\s*(.*?)\s*收藏'.decode('utf-8').encode('gbk')
	collect_pattern=re.compile(aaa,re.S)

	sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
	def parse_html_content(str):
		'''return a unicode string'''
		str = re.sub(sub_p_1, '', str)    
		str = str.replace('&nbsp;', ' ')
		str = str.replace('&amp;', '')
		str = str.replace('#039;', '')
		str = str.replace('#', '')
		str = str.replace('&#160;', ' ')
		str = str.replace('&lt;', '<')
		str = str.replace('&gt;', '>')
		str = str.replace('&amp;', '&')
		str = str.replace('&quot;', '"')
		str = str.replace('  ','')
		str = str.replace('\r\n','')
		str = str.replace('\n','')
		ustr = str
		return ustr
	blocks=re.findall(block_pattern,content)
	print len(blocks)


	##########################################################################
	for b in blocks:
		#print b
		try:
			scratch_time = time.strftime('%Y-%m-%d %H:%M:%S')
			poster=re.findall(poster_pattern,b)[0]
			#print poster.decode('utf-8','ignore').encode('gbk','ignore')
			
			post_id=re.findall(post_id_pattern,b)[0]
			print post_id
			
			poster_id=re.findall(poster_id_pattern,b)[0]
			#print poster_id
			
			poster_image=re.findall(poster_img_pattern,b)[0]
			#print poster_image
			
			poster_homepage=re.findall(poster_homepage_pattern,b)[0]
			poster_homepage='https://twitter.com'+poster_homepage
			
			post=re.findall(post_con_pattern,b)
			post=map(lambda x:parse_html_content(str(x)),post)[0]
			#print post.decode('utf-8','ignore').encode('gbk','ignore')
			
			post_time=re.findall(post_time_pattern,b)[0]
			post_time=float(post_time)
			post_time=sec_to_time(post_time)
			#print post_time
			
			#repost_num=re.findall(repost_pattern,b)[0]
			#print repost_num
			
			#reply_num=re.findall(reply_pattern,b)[0]
			#print reply_num
			
			down_area=re.findall(down_area_pattern,b)
			reply_num,repost_num,collect_num=down_area
			print reply_num,reply_num,collect_num
			
			#collect_num=re.findall(collect_pattern,b)[0]
			#print collect_num
			print '++++++++++++++++++++++++++++++++++++++++'
			#################################################################################
			query='insert ignore into twitter_happiness (post_id,scratch_time,post_time,content,image,poster,poster_id,poster_url,repost_num,comment_num,collect_num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			params=(post_id,scratch_time,post_time,post,poster_image,poster,poster_id,poster_homepage,repost_num,reply_num,collect_num)
			cur.execute(query, params)
			db.commit()
		except:
			pass
		
	##########################################################################
	##########################################################################

	driver.quit()
	print len(blocks)

##########################################################################
##########################################################################



##########################################################################
##########################################################################

if __name__=="__main__":
	while 1:
		main()
		time.sleep(120)

#driver.get('http://weibo.com/p/1035051189591617/weibo?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=3#feedtop')


