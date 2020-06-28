'''
Author: Hiddenstrawberry
'''
import os
import re
import execjs
import requests
url='https://zhujiye.haodf.com/'

session=requests.session()
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
         'Cookie':'',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
         'Accept-Encoding': 'gzip, deflate, br'}
html=session.get(url,headers=headers,verify=False)
headers['Cookie']=html.headers['Set-Cookie'].split(';')[0]+';'
html=html.content.decode('utf8')
os.environ["EXECJS_RUNTIME"] = "Node"
js_data = html.replace('<script>','').replace('</script>','')

x=re.findall('var x=(.*?),y',js_data,re.S)[0]
y=re.findall(',y=(.*?),f=function',js_data,re.S)[0]
_var=r"""var x={},y={},""".format(x,y)
with open('init.js') as f:
    js=f.read()
compiled_js = execjs.compile(_var+js)
cookie=compiled_js.eval("xxx")
cookie=re.findall(".cookie=(.*?)\+';Expires=",str(cookie),re.S)[0]
headers['Cookie']=headers['Cookie']+compiled_js.eval(cookie)+';'

html=session.get(url,headers=headers,verify=False).content.decode('gbk')
print(html)
