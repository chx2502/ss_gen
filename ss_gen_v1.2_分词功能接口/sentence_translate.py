import re
import time
import http.client
import hashlib
import json
import urllib
import random

  
def translate(content, src_lang, tar_lang):
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    #百度翻译api需申请这个帐号和密码，且每月有翻译限制，超出限制要收费
    appid = '20200527000472035'
    secretKey = 'He2ApQ8UI_a3ap9eEx_Q'
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = src_lang # 源语言'zh'
    toLang = tar_lang # 翻译后的语言'jp' 'en' 'fra' 'de'等，其中'fra'为法语，效果较差
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
  
    try:
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")# 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse) # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"]) # 取得翻译后的文本结果
        #print(dst) # 打印结果
        return dst
    except Exception as e:
        print("mes:",e)
    finally:
        if httpClient:
            httpClient.close()

def Synonymous_sentence():   
    with open('src.txt', 'r', encoding='utf-8-sig', errors='ignore') as f1:
        with open('tar.txt', 'w',encoding='utf-8', errors='ignore') as f2:
            for line in f1.readlines():
                temp = line.strip('\n').split('\t')[0]
                print(temp)
                #中-德-中
                m1 = translate(temp, 'zh', 'de')
                time.sleep(1)
                m2 = translate(m1,  'de', 'zh')
                time.sleep(1)
                f2.write(temp+'\t'+m2+'\t'+'1'+'\n')
                #中-英-中
                m1 = translate(temp, 'zh', 'en')
                time.sleep(1)
                m2 = translate(m1,  'en', 'zh')
                time.sleep(1)
                f2.write(temp+'\t'+m2+'\t'+'1'+'\n')
                #中-日-中
                m1 = translate(temp, 'zh', 'jp')
                time.sleep(1)
                m2 = translate(m1,  'jp', 'zh')
                time.sleep(1)
                f2.write(temp+'\t'+m2+'\t'+'1'+'\n')

if __name__ == '__main__':
    Synonymous_sentence()