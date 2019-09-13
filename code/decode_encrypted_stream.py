# coding=gbk
import sys
import os
import re
import requests
from pyquery import PyQuery as pq

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")




header_pinlunx = {
'Host': 'www.dianping.com',
'Accept-Encoding': 'gzip',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
}

header_css = {
'Host': 's3plus.meituan.net',
'Accept-Encoding': 'gzip',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

}


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



def css_get(doc):
    css_link = "http:"+doc("head > link:nth-child(11)").attr("href")
    print('css_link : ',css_link)
    background_link = requests.get(css_link, headers=header_css)
    r = r'background-image: url(.*?);'
    matchObj = re.compile(r, re.I)
    svg_link = matchObj.findall(background_link.text)[0].replace(")", "").replace("(", "http:")
    print('svg_link: ',svg_link)
    """
    svg_text() ����������svg�ֿ⣬��ץȡ������
    dict_svg_text: svg���������ֿ⣬���ֵ���ʽ����
    list_svg_y��svg�����е�<path>��ǩ���[x,y]�����ᣬ��[x,y]��ʽ����
    """
    #list_y data[0],data[2]:  60  2471
    #dict_avg data[0],data[2] 77  ��˳â��Ϲ���ϰ����ӽ�ݽ��ʿ���������ҹ�ѭ��Ⱦ
    dict_avg_text, list_svg_y = svg_text(svg_link)
    """
    css_dict() ����������css��ʽ��background����ʽ��
    dict_css: ����css�ֵ���ʽ
    """
    dict_css = css_dict(background_link.text)
    return dict_avg_text, list_svg_y, dict_css


# 2-���������
def svg_text(url):
    html = requests.get(url)
    dict_svg, list_y = svg_dict(html.text)
    return dict_svg, list_y


# 3-����svg�ֿ��ֵ�
def svg_dict(csv_html):
    svg_text_r = r'<textPath xlink:href="(.*?)" textLength="(.*?)">(.*?)</textPath>'
    svg_text_re = re.findall(svg_text_r, csv_html)
    print('svg_text_re type: ',type(svg_text_re))
    dict_avg = {}
    # ����svg����������ֵ�
    if len(svg_text_re) == 0:
        print('dianping svg_text_re structure maybe change,please analyze it')
        return
    for data in svg_text_re:
        print('dict_avg data[0],data[1],data[2]',data[0],data[1],data[2])
        dict_avg[data[0].replace("#", "")] = list(data[2])

        #print('dict_avg: ',dict_avg)
    """
    �ص㣺http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/74d63812e5b327d850ab4a8782833d47.svg
        svg <path> ��ǩ�����ݶ�Ӧcss��ʽ��background��y�������С�ڹ�ϵ��
        ���css��ʽ�е�background��y����С�� svg_y_re ��������С������������ȡy�ᣬ('18', 'M0', '748', 'H600')��
        ��.gqi4j {background: -98.0px -745.0px;} �е�y-745��ȡ����745��С��748�����Ӧ�����ֿ�ʵ��y��Ϊ748����Ӧ��18����<textPath>�е�x��
    """
    svg_y_r = r'<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>'
    svg_y_re = re.findall(svg_y_r, csv_html)
    list_y = []
    # �洢('18', 'M0', '748', 'H600') eg:(x���꣬δ֪��y���꣬δ֪)
    if len(svg_y_re) == 0:
        print('dianping svg_y_re structure maybe change,please analyze it')
        return
    for data in svg_y_re:
        list_y.append([data[0], data[2]])
        print('list_y data[0],data[1],data[2]: ',data[0], data[1], data[2])
    return dict_avg, list_y


# 4-����css�ֿ��ֵ�
def css_dict(html):
    css_text_r = r'.(.*?){background:(.*?)px (.*?)px;}'
    css_text_re = re.findall(css_text_r, html)
    dict_css = {}
    if len(css_text_re) == 0:
        print('css_dict html structure maybe change,please analyze it again')
        return
    for data in css_text_re:
        #print('css_dict data: ',data) #��ʽ��css_dict data:  ('jh5yp', '-364.0', '-1476.0')
        """
        �����ֿ�.gqi4j {background: -98.0px -745.0px;}��svg�ļ���Ӧ��ϵ��x/14������svg�ļ����������±�
        y��ԭ�����أ���Ҫ��svg������������
        """
        x = int(float(data[1])/-14)
        """
        �ֵ������{css��������(background-x,background-y,background-x/14,background-y)}
        """
        dict_css[data[0]] = (data[1], data[2], x, data[2]) #��ʽ��{'jh5yp': ('-364.0', '-1476.0', 26, '-1476.0')}
        #print('dict_css: ',dict_css)
    return dict_css


# 5-�������ۻ���
def css_decode(css_html, svg_dict, svg_list, pinglun_html):
    """
    :param css_html: css ��HTMLԴ��
    :param svg_dict: svg�����ֿ���ֵ�
    :param svg_list: svg�����ֿ��Ӧ����������[x, y]
    :param pinglun_html: ���۵�HTMLԴ�룬��Ӧ0-����ҳ�����ۣ��ڴ˴���
    :return: ���պϳɵ�����
    """
    #print('pinglun_html: ',pinglun_html)
    #print('pinglun_html replace: ',pinglun_html.replace('<span class="', ',').replace('"/>', ",").replace('">', ","))
    if 0:
        css_dict_text = css_html
        csv_dict_text, csv_dict_list = svg_dict, svg_list
        # ��������Դ���е�span��ǩ�������ֵ�key
        pinglun_text = pq(str(pinglun_html).replace('<span class="', ',').replace('"/>', ",").replace('">', ",")).text()
        #print('pinglun_text: ',pinglun_text) #,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
        pinglun_list = [x for x in pinglun_text.split(",") if x != '']
        #print('pinglun_list: ',pinglun_list)#['jhs0x', '��ͦ�óԵģ�', 'jh8qj', '��', 'jh21p', '��', 'jhnvt', '�ģ���˵', 'jh0fe', '��', 'jhank', '�ҷֵ�
        pinglun_str = []
        #print('css_dict_text: ',css_dict_text)
        #print('csv_dict_text: ',csv_dict_text)
        #print('csv_dict_list: ',csv_dict_list)
    print('css_decode pinglun_html: ', pinglun_html)
    # print('pinglun_html replace: ',pinglun_html.replace('<span class="', ',').replace('"/>', ",").replace('">', ","))
    css_dict_text = css_html
    csv_dict_text, csv_dict_list = svg_dict, svg_list
    # ��������Դ���е�span��ǩ�������ֵ�key
    # print('css_decode debug1')
    # print('pinglun_html: ',str(pinglun_html),type(pinglun_html))

    pinglun_text = pq(
        str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace(
            '">', ",")).text()
    print('css_decode pinglun_text: ', pinglun_text)  # ,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    print('css_decode pinglun_list: ',pinglun_list)  # ['jhs0x', '��ͦ�óԵģ�', 'jh8qj', '��', 'jh21p', '��', 'jhnvt', '�ģ���˵', 'jh0fe', '��', 'jhank', '�ҷֵ�
    pinglun_str = []
    for msg in pinglun_list:
        # ����м��ܱ�ǩ
        if msg in css_dict_text:
            # ����˵����[x,y] css��ʽ��background ��[x/14��y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # Ѱ��background��y���svg<path>��ǩ���y��С�ĵ�һ��ֵ��Ӧ���������<textPath>��hrefֵ
            for g in csv_dict_list:
                if y < int(g[1]):
                    # print(g)
                    # print(csv_dict_text[g[0]][x])
                    pinglun_str.append(csv_dict_text[g[0]][x])
                    break
        # û�м��ܱ�ǩ
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun

def css_get_for_shopDetails(doc):
    #css_link = "http:"+doc("head > link:nth-child(11)").attr("href")
    shoplist_or_eachShop = False
    css_index = 0
    #css_link = "http:" + doc("head > link:nth-child(0)").attr("href")
    for each in doc("head > link"):

        print(pq(each))
        print(pq(each).attr('href'))
        if css_index == 4:
            css_link = "http:" + pq(each).attr('href')
        css_index = css_index + 1
    print('css_link : ',css_link)
    background_link = requests.get(css_link, headers=header_css)
    r = r'background-image: url(.*?);'
    matchObj = re.compile(r, re.I)
    #svg_link = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link1 = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link2 = matchObj.findall(background_link.text)[2].replace(")", "").replace("(", "http:")
    #svg_link3 = matchObj.findall(background_link.text)[3].replace(")", "").replace("(", "http:")
    svg_link0 = matchObj.findall(background_link.text)[0].replace(")", "").replace("(", "http:")
    #svg_link4 = matchObj.findall(background_link.text)[4].replace(")", "").replace("(", "http:")
    print('css_get_for_shopDetails svg_link: ',svg_link,len(svg_link))
    print('css_get_for_shopDetails svg_link1: ', svg_link1, len(svg_link1))
    print('css_get_for_shopDetails svg_link2: ', svg_link2, len(svg_link2))
    #print('svg_link3: ', svg_link3, len(svg_link3))
    print('css_get_for_shopDetails svg_link0: ', svg_link0, len(svg_link0))
    """
    svg_text() ����������svg�ֿ⣬��ץȡ������
    dict_svg_text: svg���������ֿ⣬���ֵ���ʽ����
    list_svg_y��svg�����е�<path>��ǩ���[x,y]�����ᣬ��[x,y]��ʽ����
    """
    #list_y data[0],data[2]:  60  2471
    #dict_avg data[0],data[2] 77  ��˳â��Ϲ���ϰ����ӽ�ݽ��ʿ���������ҹ�ѭ��Ⱦ
    dict_avg_text, list_svg_y ,shoplist_or_eachShop= svg_text_shoplist(svg_link)
    """
    css_dict() ����������css��ʽ��background����ʽ��
    dict_css: ����css�ֵ���ʽ
    """
    #print('background_link.text: ',background_link.text)
    dict_css = css_dict_shopDetails(background_link.text)
    #dict_css: {'jbtvod': ('-196.0', '-63.0', 14, '-63.0'), 'ezglgj': ('-0.0', '-1700.0', 0, '-1700.0')}
    #list_y data[0],data[1],data[2]:  2 M0 88
    #dict_avg data[0],data[1],data[2] #2 518 ϸ����Ѹ������ʰ�߱Ƕ����ҳۿ�¶����ˤ���ɵ�ɭʼ�����������ͺӭȷ������
    return dict_avg_text, list_svg_y, dict_css,shoplist_or_eachShop

def css_get_for_shopFoodMenuList(doc):
    #css_link = "http:"+doc("head > link:nth-child(11)").attr("href")
    shoplist_or_eachShop = False
    css_index = 0
    #css_link = "http:" + doc("head > link:nth-child(0)").attr("href")
    for each in doc("head > link"):

        print(pq(each))
        print(pq(each).attr('href'))
        css_link = ''
        #if css_index == 4:
        #    css_link = "http:" + pq(each).attr('href')
        #css_index = css_index + 1
    print('pq(doc("head > link:nth-last-child(2)")).attr(href): ',pq(doc("head > link:nth-last-child(2)")).attr('href'))
    print('css_link : ',css_link)
    background_link = requests.get(css_link, headers=header_css)
    r = r'background-image: url(.*?);'
    matchObj = re.compile(r, re.I)
    #svg_link = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link = matchObj.findall(background_link.text)[2].replace(")", "").replace("(", "http:")
    svg_link1 = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link2 = matchObj.findall(background_link.text)[2].replace(")", "").replace("(", "http:")
    #svg_link3 = matchObj.findall(background_link.text)[3].replace(")", "").replace("(", "http:")
    svg_link0 = matchObj.findall(background_link.text)[0].replace(")", "").replace("(", "http:")
    #svg_link4 = matchObj.findall(background_link.text)[4].replace(")", "").replace("(", "http:")
    print('svg_link: ',svg_link,len(svg_link))
    print('svg_link1: ', svg_link1, len(svg_link1))
    print('svg_link2: ', svg_link2, len(svg_link2))
    #print('svg_link3: ', svg_link3, len(svg_link3))
    print('svg_link0: ', svg_link0, len(svg_link0))
    """
    svg_text() ����������svg�ֿ⣬��ץȡ������
    dict_svg_text: svg���������ֿ⣬���ֵ���ʽ����
    list_svg_y��svg�����е�<path>��ǩ���[x,y]�����ᣬ��[x,y]��ʽ����
    """
    #list_y data[0],data[2]:  60  2471
    #dict_avg data[0],data[2] 77  ��˳â��Ϲ���ϰ����ӽ�ݽ��ʿ���������ҹ�ѭ��Ⱦ
    dict_avg_text, list_svg_y ,shoplist_or_eachShop= svg_text_shoplist(svg_link)
    """
    css_dict() ����������css��ʽ��background����ʽ��
    dict_css: ����css�ֵ���ʽ
    """
    dict_css = css_dict_shopDetails(background_link.text)
    return dict_avg_text, list_svg_y, dict_css,shoplist_or_eachShop


def css_get_for_shoplist(doc):
    #css_link = "http:"+doc("head > link:nth-child(11)").attr("href")
    shoplist_or_eachShop = False

    css_link = "http:" + doc("head > link:nth-child(21)").attr("href")
    print('css_link : ',css_link)
    background_link = requests.get(css_link, headers=header_css)
    r = r'background-image: url(.*?);'
    matchObj = re.compile(r, re.I)
    #svg_link = matchObj.findall(background_link.text)[0].replace(")", "").replace("(", "http:")
    svg_link = matchObj.findall(background_link.text)[2].replace(")", "").replace("(", "http:")
    svg_link1 = matchObj.findall(background_link.text)[1].replace(")", "").replace("(", "http:")
    svg_link2 = matchObj.findall(background_link.text)[2].replace(")", "").replace("(", "http:")
    svg_link3 = matchObj.findall(background_link.text)[3].replace(")", "").replace("(", "http:")
    svg_link0 = matchObj.findall(background_link.text)[0].replace(")", "").replace("(", "http:")
    #svg_link4 = matchObj.findall(background_link.text)[4].replace(")", "").replace("(", "http:")
    print('css_get_for_shoplist svg_link: ',svg_link,len(svg_link))
    print('css_get_for_shoplist svg_link1: ', svg_link1, len(svg_link1))
    print('css_get_for_shoplist svg_link2: ', svg_link2, len(svg_link2))
    print('css_get_for_shoplist svg_link3: ', svg_link3, len(svg_link3))
    print('css_get_for_shoplist svg_link0: ', svg_link0, len(svg_link0))
    """
    svg_text() ����������svg�ֿ⣬��ץȡ������
    dict_svg_text: svg���������ֿ⣬���ֵ���ʽ����
    list_svg_y��svg�����е�<path>��ǩ���[x,y]�����ᣬ��[x,y]��ʽ����
    """
    #list_y data[0],data[2]:  60  2471
    #dict_avg data[0],data[2] 77  ��˳â��Ϲ���ϰ����ӽ�ݽ��ʿ���������ҹ�ѭ��Ⱦ
    dict_avg_text, list_svg_y ,shoplist_or_eachShop= svg_text_shoplist(svg_link)
    """
    css_dict() ����������css��ʽ��background����ʽ��
    dict_css: ����css�ֵ���ʽ
    """
    dict_css = css_dict_shoplist(background_link.text)
    return dict_avg_text, list_svg_y, dict_css,shoplist_or_eachShop


# 2-���������
def svg_text_shoplist(url):
    html = requests.get(url)
    shoplist_or_eachShop = False #ture is shoplist
    #print('*****************************: ',html.text)
    print('str(html.text).find(xlink)',str(html.text).find('textPath'))
    if str(html.text).find('textPath') != -1:
        dict_svg, list_y = svg_dict(html.text)
        shoplist_or_eachShop = False
    else:
        dict_svg, list_y = svg_dict_shoplist(html.text)
        shoplist_or_eachShop = True
    return dict_svg, list_y,shoplist_or_eachShop


# 3-����svg�ֿ��ֵ�
def svg_dict_shoplist(csv_html):
    svg_text_r = r'<text x="(.*?)" y="(.*?)">(.*?)</text>'
    svg_text_re = re.findall(svg_text_r, csv_html)
    print('svg_text_re type: ',type(svg_text_re))
    dict_avg = {}
    list_y = []
    # ����svg����������ֵ�
    if len(svg_text_re) == 0:
        print('dianping svg_text_re structure maybe change,please analyze it')
        return
    for data in svg_text_re:
        print('svg_dict_shoplist data: ',data)
        #print('svg_dict_shoplist data[0],data[1],data[2]',data[0],data[1],type(data[1]),(data[2]))
        dict_avg[data[1]] = list(data[2])
        list_y.append(int(data[1]))
        #print('dict_avg: ',dict_avg)
    """
    �ص㣺http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/74d63812e5b327d850ab4a8782833d47.svg
        svg <path> ��ǩ�����ݶ�Ӧcss��ʽ��background��y�������С�ڹ�ϵ��
        ���css��ʽ�е�background��y����С�� svg_y_re ��������С������������ȡy�ᣬ('18', 'M0', '748', 'H600')��
        ��.gqi4j {background: -98.0px -745.0px;} �е�y-745��ȡ����745��С��748�����Ӧ�����ֿ�ʵ��y��Ϊ748����Ӧ��18����<textPath>�е�x��
    """

    return dict_avg, list_y


# 4-����css�ֿ��ֵ�
def css_dict_shoplist(html):
    css_text_r = r'.(.*?){background:(.*?)px (.*?)px;}'
    css_text_re = re.findall(css_text_r, html)
    dict_css = {}
    if len(css_text_re) == 0:
        print('css_dict html structure maybe change,please analyze it again')
        return
    for data in css_text_re:
        #print('css_dict data: ',data) #��ʽ��css_dict data:  ('jh5yp', '-364.0', '-1476.0')
        """
        �����ֿ�.gqi4j {background: -98.0px -745.0px;}��svg�ļ���Ӧ��ϵ��x/14������svg�ļ����������±�
        y��ԭ�����أ���Ҫ��svg������������
        """
        #x = int(float(data[1])/-14)
        x = int(float(data[1]) / -12)
        """
        �ֵ������{css��������(background-x,background-y,background-x/14,background-y)}
        """
        dict_css[data[0]] = (data[1], data[2], x, data[2]) #��ʽ��{'jh5yp': ('-364.0', '-1476.0', 26, '-1476.0')}
        #print('css_dict_shoplist: ',dict_css)
        #print('dict_css: ',dict_css)
    #print('css_dict function: ',dict_css)
    return dict_css

def css_dict_shopDetails(html):
    css_text_r = r'.(.*?){background:(.*?)px (.*?)px;}'
    css_text_re = re.findall(css_text_r, html)
    dict_css = {}
    if len(css_text_re) == 0:
        print('css_dict html structure maybe change,please analyze it again')
        return
    for data in css_text_re:
        #print('css_dict data: ',data) #��ʽ��css_dict data:  ('jh5yp', '-364.0', '-1476.0')
        """
        �����ֿ�.gqi4j {background: -98.0px -745.0px;}��svg�ļ���Ӧ��ϵ��x/14������svg�ļ����������±�
        y��ԭ�����أ���Ҫ��svg������������
        """
        x = int(float(data[1])/-14)
        #x = int(float(data[1]) / -12)
        """
        �ֵ������{css��������(background-x,background-y,background-x/14,background-y)}
        """
        dict_css[data[0]] = (data[1], data[2], x, data[2]) #��ʽ��{'jh5yp': ('-364.0', '-1476.0', 26, '-1476.0')}
        #print('dict_css: ',dict_css)
    #css_dict function:  {'jbtvod': ('-196.0', '-63.0', 14, '-63.0'), 'ezglgj': ('-0.0', '-1700.0', 0, '-1700.0')}
    #print('css_dict_shopDetails css_dict function: ',dict_css)
    return dict_css

# 5-�������ۻ���
def css_decode_shoplist_old(css_html, svg_dict, svg_list, pinglun_html):
    """
    :param css_html: css ��HTMLԴ��
    :param svg_dict: svg�����ֿ���ֵ�
    :param svg_list: svg�����ֿ��Ӧ����������[x, y]
    :param pinglun_html: ���۵�HTMLԴ�룬��Ӧ0-����ҳ�����ۣ��ڴ˴���
    :return: ���պϳɵ�����
    """
    print('css_decode_shoplist pinglun_html: ',pinglun_html)
    #print('pinglun_html replace: ',pinglun_html.replace('<span class="', ',').replace('"/>', ",").replace('">', ","))
    css_dict_text = css_html
    csv_dict_text, csv_dict_list = svg_dict, svg_list
    # ��������Դ���е�span��ǩ�������ֵ�key
    #print('css_decode debug1')
    #print('pinglun_html: ',str(pinglun_html),type(pinglun_html))

    #print(pq(pinglun_html)('.emoji-img'))
    img_str =  pq(pinglun_html)('.emoji-img')
    for each in img_str:
        #print('each in img_str: ',each)
        #print('each in img_str: ', pq(each))
        pinglun_html = str(pinglun_html).replace(str(pq(each)),'')
    pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",")).text()    #shoplist
    #pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",").replace('<br/>','').).text()


    #print('css_decode_shoplist pinglun_text before: ',pinglun_text) #,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    #print('css_decode_shoplist pinglun_list after: ',pinglun_list)#['jhs0x', '��ͦ�óԵģ�', 'jh8qj', '��', 'jh21p', '��', 'jhnvt', '�ģ���˵', 'jh0fe', '��', 'jhank', '�ҷֵ�
    pinglun_str = []
    #print('--------------------------------: ',css_dict_text)
    #print('--------------------------------: ',csv_dict_text)
    #print('--------------------------------: ', csv_dict_list)
    for msg in pinglun_list:
        # ����м��ܱ�ǩ
        if msg in css_dict_text:
            # ����˵����[x,y] css��ʽ��background ��[x/14��y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # Ѱ��background��y���svg<path>��ǩ���y��С�ĵ�һ��ֵ��Ӧ���������<textPath>��hrefֵ

            for g in csv_dict_list:
                print('css_decode_shoplist: csv_dict_list: ',csv_dict_list)
                #print('css_decode_shoplist g,y: ',g,y)
                if int(y) < int(g):
                    # print(g)
                    # print(csv_dict_text[g[0]][x])
                    #print('csv_dict_text[str(g)][x],msg: ',csv_dict_text[str(g)][x],msg)
                    pinglun_str.append(csv_dict_text[str(g)][x])
                    break
        # û�м��ܱ�ǩ
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun


def css_decode_shoplist_backup(css_html, svg_dict, svg_list, pinglun_html):
    """
    :param css_html: css ��HTMLԴ��
    :param svg_dict: svg�����ֿ���ֵ�
    :param svg_list: svg�����ֿ��Ӧ����������[x, y]
    :param pinglun_html: ���۵�HTMLԴ�룬��Ӧ0-����ҳ�����ۣ��ڴ˴���
    :return: ���պϳɵ�����
    """
    print('css_decode_shoplist pinglun_html: ',pinglun_html)
    #print('pinglun_html replace: ',pinglun_html.replace('<span class="', ',').replace('"/>', ",").replace('">', ","))
    css_dict_text = css_html
    csv_dict_text, csv_dict_list = svg_dict, svg_list
    # ��������Դ���е�span��ǩ�������ֵ�key
    #print('css_decode debug1')
    #print('pinglun_html: ',str(pinglun_html),type(pinglun_html))

    #print(pq(pinglun_html)('.emoji-img'))
    img_str =  pq(pinglun_html)('.emoji-img')
    for each in img_str:
        #print('each in img_str: ',each)
        #print('each in img_str: ', pq(each))
        pinglun_html = str(pinglun_html).replace(str(pq(each)),'')
    pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",")).text()    #shoplist
    #pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",").replace('<br/>','').).text()

    print('css_decode_shoplist replace tag: ',pinglun_text)
    #print('css_decode_shoplist pinglun_text before: ',pinglun_text) #,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    #print('css_decode_shoplist pinglun_list after: ',pinglun_list)#['jhs0x', '��ͦ�óԵģ�', 'jh8qj', '��', 'jh21p', '��', 'jhnvt', '�ģ���˵', 'jh0fe', '��', 'jhank', '�ҷֵ�
    pinglun_str = []
    #print('--------------------------------: ',css_dict_text)
    #print('--------------------------------: ',csv_dict_text)
    #print('--------------------------------: ', csv_dict_list)
    for msg in pinglun_list:
        # ����м��ܱ�ǩ
        if msg in css_dict_text:
            # ����˵����[x,y] css��ʽ��background ��[x/14��y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # Ѱ��background��y���svg<path>��ǩ���y��С�ĵ�һ��ֵ��Ӧ���������<textPath>��hrefֵ
            #print('css_decode_shoplist: csv_dict_list: ', csv_dict_list)
            #print('csv_dict_text: ', csv_dict_text)
            for g in csv_dict_list:
                #print('csv_dict_list: ',csv_dict_list)
                #print('css_decode_shoplist g,y: ',g,y)

                if int(y) < int(g[1]):
                    # print(g)
                    # print(csv_dict_text[g[0]][x])
                    #print('csv_dict_text[str(g)][x],msg: ',csv_dict_text[str(g)][x],msg)
                    pinglun_str.append(csv_dict_text[g[0]][x])
                    break
        # û�м��ܱ�ǩ
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun

def css_decode_shoplist(css_html, svg_dict, svg_list, pinglun_html):
    """
    :param css_html: css ��HTMLԴ��
    :param svg_dict: svg�����ֿ���ֵ�
    :param svg_list: svg�����ֿ��Ӧ����������[x, y]
    :param pinglun_html: ���۵�HTMLԴ�룬��Ӧ0-����ҳ�����ۣ��ڴ˴���
    :return: ���պϳɵ�����
    """
    # dict_css: {'jbtvod': ('-196.0', '-63.0', 14, '-63.0'), 'ezglgj': ('-0.0', '-1700.0', 0, '-1700.0')}
    # list_y data[0],data[1],data[2]:  2 M0 88
    # dict_avg data[0],data[1],data[2] #2 518 ϸ����Ѹ������ʰ�߱Ƕ����ҳۿ�¶����ˤ���ɵ�ɭʼ�����������ͺӭȷ������
    ##print('css_decode_shoplist svg_dict: ',svg_dict)#{'1': ['��', 'ҩ', '��', 'ţ', '��', 'ֳ', '��'}
    #print('css_decode_shoplist svg_list: ', svg_list)#[['1', '38'], ['2', '88'], ['3', '136']
    #print('css_decode_shoplist pinglun_html: ',pinglun_html)
    #print('css_decode_shoplist css_html: ', css_html)#{'jbtvod': ('-196.0', '-63.0', 14, '-63.0'), 'ezglgj': ('-0.0', '-1700.0', 0, '-1700.0')}
    #print('pinglun_html replace: ',pinglun_html.replace('<span class="', ',').replace('"/>', ",").replace('">', ","))
    css_dict_text = css_html
    csv_dict_text, csv_dict_list = svg_dict, svg_list
    # ��������Դ���е�span��ǩ�������ֵ�key
    #print('css_decode debug1')
    #print('pinglun_html: ',str(pinglun_html),type(pinglun_html))

    #print(pq(pinglun_html)('.emoji-img'))
    img_str =  pq(pinglun_html)('.emoji-img')
    for each in img_str:
        #print('each in img_str: ',each)
        #print('each in img_str: ', pq(each))
        pinglun_html = str(pinglun_html).replace(str(pq(each)),'')
    pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",")).text()    #shoplist
    #pinglun_text = pq(str(pinglun_html).replace('<span class="tag">', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",").replace('<br/>','').).text()

    print('css_decode_shoplist replace tag: ',pinglun_text)
    #print('css_decode_shoplist pinglun_text before: ',pinglun_text) #,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    #print('css_decode_shoplist pinglun_list after: ',pinglun_list)#['jhs0x', '��ͦ�óԵģ�', 'jh8qj', '��', 'jh21p', '��', 'jhnvt', '�ģ���˵', 'jh0fe', '��', 'jhank', '�ҷֵ�
    pinglun_str = []
    #print('--------------------------------: ',css_dict_text)
    #print('csv_dict_text--------------------------------: ',csv_dict_text)
    #print('--------------------------------: ', csv_dict_list)

    for msg in pinglun_list:
        # ����м��ܱ�ǩ
        if msg in css_dict_text: #{'dpw6v': ('-408.0', '-639.0', 34, '-639.0'), 'aspzz': ('-168.0', '-1818.0', 14, '-1818.0')}
            # ����˵����[x,y] css��ʽ��background ��[x/14��y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # Ѱ��background��y���svg<path>��ǩ���y��С�ĵ�һ��ֵ��Ӧ���������<textPath>��hrefֵ
            #print('css_decode_shoplist: csv_dict_list: ', csv_dict_list)
            #print('csv_dict_text: ', csv_dict_text)
            #print('css_decode_shoplist msg,x,y: ',msg,x,y)
            for g in csv_dict_list: #����y���б�
                #print('csv_dict_list: ',csv_dict_list)
                #print('css_decode_shoplist g,y,x: ',g,int(y),x)
                if int(y) < int(g):
                #if int(y) < int(g[1]):
                    # print(g)
                    # print(csv_dict_text[g[0]][x])
                    #print('csv_dict_text[str(g)][x],msg: ',csv_dict_text[str(g)][x],msg)

                    #print('g,x��',g,x)
                    #print('csv_dict_text[g]: ',csv_dict_text[str(g)])
                    #print('csv_dict_text[g][x]: ', csv_dict_text[str(g)][x])
                    #pinglun_str.append(csv_dict_text[str(g)][x])#{'35': ['յ', '��', '��', '׳', 'ͻ', '��', '��', '��', 'ζ', '��', 'ƴ', '��', '��', '��', '��', '��'}
                    #print('csv_dict_text: ',csv_dict_text,)
                    #pinglun_str.append(csv_dict_text[g[0]][x])
                    #print('xxxxxxxxxxxxxxxxxxxx: ',csv_dict_text)
                    pinglun_str.append(csv_dict_text[str(g)][x])
                    break
        # û�м��ܱ�ǩ
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun

def get_brower_driver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # ����useragent
    # dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')  #������Ҫ���þ�����������Ϣ
    dcap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  # ������Ҫ���þ�����������Ϣ
    dcap['phantomjs.page.settings.loadImages'] = False
    driver = webdriver.PhantomJS(desired_capabilities=dcap)  # ��װ�������Ϣ
    return driver


def decode_for_input_encrypted_stream(input_stream,dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop):
    proxies = {
        "http": "http://179.180.158.184:8080"  # ����ip
    }
    header_pinlun = {
        'Host': 'www.dianping.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    #url = "http://www.dianping.com/shanghai/ch10/g110"
    #html = requests.get(url=url, headers=header_pinlun, proxies=proxies)
    #print("1 ===> STATUS", html.status_code)
    # print('------------: ',html.text)
    #doc = pq(html.text)

    #html = driver.get(url)
    #doc = pq(driver.page_source)
    #print('-------------------: ',doc)
    #dict_svg_text, list_svg_y, dict_css_x_y = css_get(doc)
    print('shoplist_or_eachShop: ',shoplist_or_eachShop)
    if shoplist_or_eachShop == True:
        result = css_decode_shoplist(dict_css_x_y, dict_svg_text, list_svg_y, input_stream)
    else:
        result = css_decode(dict_css_x_y, dict_svg_text, list_svg_y, input_stream)
    print(result)
    return result


#def decode_recommend_foodlist_for_each_shop(shop_info,input_stream):



def decode_score_for_service_taste_env_price(shop_info,input_stream,score_or_price):#score_or_price:0-score,1-price
    num = {'ke3s3': 0, 'key5d': 2, 'keomp': 3, 'kehxa': 4, 'keez2': 5, 'kece4': 6, 'kes4i': 7, 'ke09w': 8, 'kewn2': 9}
    score_index = 0  # 0�ǿ�ζ��1�ǻ�����2�Ƿ���
    num_point_before = 100
    num_point_after = 100
    score_assign = ''
    for j in input_stream:
        print('***************: ', pq(j))
        # print('***************: ',pq(j).attr("class"))
        if score_or_price == 0:
            digital_code = pq(j).attr("class")
            print('digital_code: ',digital_code)
            if str(pq(j)).find('.1') != -1:
                print('score: ', str(num[digital_code]) + '.1')
                score_assign = str(num[digital_code]) + '.1'
                if score_index == 0:
                    print('---- taste core: ', score_assign)
                    shop_info.taste_score = score_assign
                elif score_index == 1:
                    print('---- environment score: ', score_assign)
                    shop_info.environment_score = score_assign
                elif score_index == 2:
                    print('---- service score: ', score_assign)
                    shop_info.service_score = score_assign
                score_index = score_index + 1
                continue

            else:
                if num_point_before == 100:
                    num_point_before = num[digital_code]
                else:
                    num_point_after = num[digital_code]
            if num_point_before != 100 and num_point_after != 100:
                score_assign = str(num_point_before) + '.' + str(num_point_after)
                if score_index == 0:
                    print('---- taste core: ', score_assign)
                    shop_info.taste_score = score_assign
                elif score_index == 1:
                    print('---- environment score: ', score_assign)
                    shop_info.environment_score = score_assign
                elif score_index == 2:
                    print('---- service score: ', score_assign)
                    shop_info.service_score = score_assign
                num_point_before = 100
                num_point_after = 100
                score_index = score_index + 1
        else:
            #print('price�� ',str(input_stream))
            price_text = pq(str(input_stream).replace('<b>"', ',').replace('</b>', ',').replace('<span class="', ',').replace('"/>', ",").replace('">', ",")).text()
            #print('price_text�� ', price_text)
            # print('pinglun_text: ',pinglun_text) #,jhs0x,��ͦ�óԵģ�,jh8qj,��,jh21p,��,jhnvt,�ģ���˵,jh0fe,��,jhank,�ҷֵ꣬
            price_list = [x for x in price_text.split(",") if x != '']
            price_str = ''
            print('price_list:',price_list)
            for each in price_list:
                if each != '��':
                    if each in num:
                        price_str = price_str + str(num[str(each)])
                    else:
                        price_str = price_str + str(each)
            shop_info.avgPrice = price_str
            #print('price_list: ',price_list)


if __name__ == '__main__':
    shoplist_or_eachShop = False
    pinglun = '''
        <span class='tag'>��<span class="ozfvt"></span><span class="ozefi"></span>
        '''
    url = "http://www.dianping.com/shanghai/ch10/g110"
    driver = get_brower_driver()
    html = driver.get(url)
    doc = pq(driver.page_source)
    dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop= css_get_for_shoplist(doc)
    decode_for_input_encrypted_stream(pinglun,dict_svg_text, list_svg_y, dict_css_x_y,shoplist_or_eachShop)