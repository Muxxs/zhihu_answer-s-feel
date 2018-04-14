#coding=utf-8

from selenium import webdriver
import time,re

import urllib

from bs4 import BeautifulSoup

import html.parser
from bosonnlp import BosonNLP
def main():
    driver = webdriver.Chrome('/Users/wangjiao/Desktop/video/video_web/chromedriver')  # Optional argument, if not specified will search path.
    #driver = webdriver.Chrome()  # 打开浏览器
    driver.get("https://www.zhihu.com/question/272263239") # 打开想要爬取的知乎页面

    # 模拟用户操作
    def execute_times(times):

        for i in range(0,times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()
                print("page" + str(i))
                time.sleep(2)

            except:
                pass
    feeling=""
    def remove_tag(content):
        f=content.split("<")
        if f[-1].replace(";","").replace(" ","")=="":
            return "",0
        if f[0].find(">")==-1:
            all=f[0]
        all=""
        for x in f:
            try:
                content=x.split(">")[1]
                all=all+content
            except:pass

        from bosonnlp import BosonNLP
        # 注意：在测试时请更换为您的API Token
        nlp = BosonNLP('API Token')
        result = nlp.sentiment(all)
        print(result)
        return all+"------积极度:"+str(result[0][0]),result[0][0]

    def draw(mem):

        low=0
        mid=0
        high=0
        very_high=0
        for i in mem:
            if i<=0.4:
                low=low+1
            elif i<=0.65:
                mid=mid+1
            elif i<=0.9:
                high=high+1
            else:
                very_high=very_high+1

        import numpy as np
        import matplotlib.pyplot as plt

        labels = 'low', 'mid', 'high', 'very_high'
        fracs = [low, mid, high, very_high]
        explode = [0.1, 0.1, 0.1, 0.1]  # 0.1 凸出这部分，
        plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
        # autopct ，show percet
        plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
                shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6

                )
        '''
        labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
        autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        shadow，饼是否有阴影
        startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
        pctdistance，百分比的text离圆心的距离
        patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
        '''

        plt.show()

    from functools import reduce

    def str2float(s):
        return reduce(lambda x, y: x + int2dec(y), map(str2int, s.split('.')))

    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

    def str2int(s):
        return reduce(lambda x, y: x * 10 + y, map(char2num, s))

    def intLen(i):
        return len('%d' % i)

    def int2dec(i):
        return i / (10 ** intLen(i))









    execute_times(15)

    result_raw = str(driver.page_source)  # 这是原网页 HTML 信息
    res=result_raw.split('<span class="RichText CopyrightRichText-richText" itemprop="text">')
    num=0
    for i in res:
        i=i.split("<!-- react-empty")[0].replace('&gt;',">").replace("&lt","<").replace("&amp;gt",">").replace("&amp;lt","<")
        if num is not 0:
            content=remove_tag(i)[0]
            feeling = feeling + "|" +str( remove_tag(i)[1])
            print(str(num)+":"+content+"\n")
        num=num+1
    all_feel = []
    for i in feeling.split("|"):
        if not i=="0":
            if not i=="":
                all_feel.append(round(str2float(i), 4))
    draw(all_feel)
if __name__ == '__main__':
    main()
