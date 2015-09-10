#coding=utf-8
import pycurl
import StringIO
import re,chardet
import setting
import os

def tranun(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\' and s[i+1]=='u':
			ss=ss+unichr(int(s[i+2:i+6],16))
			i=i+6
		else:
			ss=ss+s[i]
			i=i+1
	return ss
def tran(s):
	l=len(s)
	ss=''
	i=0
	while i<l:
		if s[i]=='\\':
			i=i+1
		else:
			ss=ss+s[i]
			i=i+1
	return ss

def main(con):
	
	b=tranun(con)
	c=tran(b)
	pattern=re.compile(r'rnt{0,25}|t{3,25}',re.S)
	pattern1=re.compile(r'>n*\s*t*\s*t*',re.S)
	c=re.sub(pattern,'',c)
	c=c.replace('n<','<')
	d=re.sub(pattern1,'>',c)
	d=d.encode('utf-8')

    
	file_path=setting.CURRENT_PATH+'/res.txt'
	f=open(file_path,'wb')
	f.write(d)
	f.close()
	
def getpage(url):
    c=pycurl.Curl()
    c.setopt(pycurl.URL,url)
    
    b=StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION,b.write)
    c.perform()
    f=open('d:/mi.txt','wb')
    f.write(b.getvalue())
    f.close()
    return b.getvalue()
    
def cutpage(html):
    patt=re.compile('{"pid":"pl_wb_feedlist".*?<script>STK',re.S)
    con=re.findall(patt,html)[0]
    #f=open('d:/mii.txt','wb')
    #f.write(con)
    #f.close()
    return con
    
if __name__=='__main__':
    html=getpage('http://s.weibo.com/wb/%25E5%25BC%25A0%25E7%258E%2589%25E8%2590%258D&xsort=time&Refer=weibo_wb')
    #html=getpage('http://s.weibo.com/wb/%25E6%25A6%2586%25E6%259E%2597&xsort=time&page=3')
    content=cutpage(html)
    main(content)
    os.system('python %s/parse_post.py' % setting.CURRENT_PATH)