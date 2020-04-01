from bs4 import BeautifulSoup
import requests
import time
import os
import re


def get_subjects_url(start, end, url, data=None):
    wb_data = requests.get(url)
    time.sleep(2)
    Soup = BeautifulSoup(wb_data.text, "lxml")
    href_l_list = str(Soup.select("body > div.container-category > div.topCatPage.container.keyStageOne > div.col1.col-12.col-md-8")).split('a href="')
    i = 0
    for h in href_l_list[1:]:
        href_l = re.split('"', h)[0]
        href_f = "https://www.twinkl.co.uk"
        href = href_f + href_l + '/'
        print(href)
        filename = "resources_%d.txt"%(i)
        get_subSubjects_url(filename, start, end, href)
        i = i+1


def get_subSubjects_url(filename, start, end, url, data=None):
    wb_data = requests.get(url)
    time.sleep(2)
    Soup = BeautifulSoup(wb_data.text, "lxml")
    href_l_list = str(Soup.select("#group-1")).split('a href="')
    for h in href_l_list[1:]:
        href_l = re.split('"', h)[0]
        href_f = "https://www.twinkl.co.uk/"
        href = href_f + href_l + '/'
        get_pages_url(filename, href, start, end)


def get_pages_url(filename, href, start, end):
    urls = [href + "{}".format(i) for i in range(start, end)]
    for url in urls:
        try:
            get_video_url(filename, url)
        except:
            print("An exception occurred")



def get_video_url(filename, url, data=None):
    wb_data = requests.get(url)
    time.sleep(2)
    Soup = BeautifulSoup(wb_data.text, "lxml")
    href_l_list = re.split('href="', str(Soup.select("#resources > li > a:nth-of-type(1)")))
    for h in href_l_list[1:]:
        href_l = re.split('"', h)[0]
        href_f = "https://www.twinkl.co.uk"
        href = href_f + href_l
        get_download_url(filename, href)



def get_download_url(filename, url, data=None):
    '''
    s = requests.Session()
    signIn_url = "https://www.twinkl.co.uk/sign-in"
    data = {
        'username': '1823865296@qq.com',
        'password': 'rmr123456789'
    }
    s.post(signIn_url, data)
    '''

    wb_data = requests.get(url)
    time.sleep(2)
    Soup = BeautifulSoup(wb_data.text, "lxml")
    href_l = str(Soup.select('#resource > div > meta:nth-of-type(3)')).split('content="')[1].split('"')[0]
    # href_l = str(Soup.select("#download_link")).split('href="')[1].split('"')[0]
    href_f = "https://www.twinkl.co.uk/download/"
    href = href_f + href_l
    write_file(filename, href)


def write_file(filename, download_url):
    path = os.getcwd()
    save_file = path + '/' + filename
    if not os.path.exists(path):
        os.mkdir(path)
    url_file = open(save_file, 'a+')
    url_file.write(download_url + '\n')
    url_file.close()


if __name__ == '__main__':
    get_subjects_url(1, 10, "https://www.twinkl.co.uk/resources")