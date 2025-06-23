import requests
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
#import os

def getN(url):
    uResponse=webdriver.Chrome()
    uResponse.get(url)
    log1=uResponse.execute_script("Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});")
    log2=uResponse.execute_script("window.navigator.webdriver")
    #print(log1)
    #print(log2)
    uResponse.implicitly_wait(10)
    resText=uResponse.page_source

    soup= BeautifulSoup(resText, 'html.parser')
    #print(soup.prettify())
    allNext=soup.find_all('a', string="下一页")
    if allNext:
        nextPageUrl=allNext[0].get('href')
    if not allNext:
        chapterNext=soup.find_all('a', string="下一章")
        if not chapterNext:
            print("No more. exit.")
            exit()
        nextPageUrl=chapterNext[0].get('href')
    temp=nextPageUrl
    nextPageUrl=""
    lst='a'
    befor=False
    for ch in uResponse.current_url:
        if (ch=='/' and lst=='/'):
            befor=True
        if (ch=='/' and lst!='/' and befor==True):
            break
        nextPageUrl=nextPageUrl+ch
        lst=ch
    nextPageUrl=nextPageUrl+temp
    print("The nextPageUrl is:")
    print(nextPageUrl)
    gTitle=soup.find_all(attrs={'class':'title'})
    #print("title is ")
    #print(gTitle[0].get_text())
    if not gTitle:
        print("Cannot find the title of this Chapter. exit.")
        exit()
    with open("result.txt", "a", encoding='utf-8') as f:
        f.write("\n\n")
        f.write(gTitle[0].get_text())
    #exit()
    conText=soup.find_all("br")
    print(conText)
    for aLine in conText:
        print("    Try write")
        print(aLine.next_sibling)
        with open("result.txt", "a", encoding='utf-8') as f:
            f.write(aLine.next_sibling)
            f.write('\n')
    if not conText:
        print("[Note]The title exists but there seems that no context is here")
        exit()
    uResponse.close()
    #os.system("pause")
    getN(nextPageUrl)

print("Hello")
firstUrl=input()
getN(firstUrl)
