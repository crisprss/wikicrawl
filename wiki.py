#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import urllib
import time

start_url = 'https://en.wikipedia.org/wiki/Chris_Gragg'
target_url = 'https://en.wikipedia.org/wiki/Philosophy'
def continue_crawl(search_history,target_url,max_steps=25):
    if(search_history[-1] == target_url):
        print("found target url! \n")
        print(target_url)
        return False
    elif(len(search_history) > max_steps):
        print("over length,done! \n")
        return  False
    elif(search_history[-1] in search_history[:-1]):
        print("already crawl it,done! \n")
        return False
    else:
        return True

def find_first_link(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html,'html.parser')
    content_div = soup.find(id='mw-content-text').find(class_='mw-parser-output')
    first_link = None
    for element in content_div.find_all('p',recursive=False):
        if(element.find("a",recursive=False)):
            first_link = element.find("a",recursive=False).get('href')
            break

    if not first_link:
        return
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/',first_link)
    return first_link

link_chain = [start_url]

while continue_crawl(link_chain,target_url):
    print(link_chain[-1])

    first_link = find_first_link(link_chain[-1])
    if not first_link:
        print("no link,done! \n")
        break
    link_chain.append(first_link)
    time.sleep(2)
