from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright as pw
import numpy as np 

def linkSelect(p:str): 
    #print(f"select{p}")
    op=False
    result=''
    lst=''
    for ch in p:
        if (ch=='/' and lst=='/'):
            op=True
        if (ch=='/' and lst!='/' and op==True):
            break
        result=result+ch 
        lst=ch
    return result

with open("result.txt", "w", encoding='utf-8') as f:
    f.write('')
nowUrl=input("Url of the first Page:")
#getN(firstUrl)
p=pw().start()
browser=p.chromium.launch(headless=False)
opt:int=1
filter=np.loadtxt("filters.txt", delimiter=',', dtype=str, encoding='utf-8').tolist()
print(f"filters:{filter}")
while True:
    page=browser.new_page()
    page.goto(nowUrl)
    page.evaluate("Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});")
    soup=BeautifulSoup(page.content(), 'lxml')

    allNext=soup.find_all(lambda tag: tag.name=='a' and (tag.get_text()=='下一页' or tag.get_text()=='下一章'))
    try:
        nextLink=linkSelect(nowUrl)+allNext[0].get('href')
    except Exception as e:
        print(f"[ERROR IN FINDING NEXTLINK]{e}")
        browser.close()
        p.stop()
        exit()
    theTitle=soup.select('.title')[0].text.strip()
    conText=soup.select('div#chaptercontent')[0]
    
    if (not theTitle) and (not conText):
        if opt==2:
            page.close()
            nowUrl=nextLink
            print(f"jumped in {nowUrl}")
            continue
        print(f"next is found :{nextLink}\nHowever there's no content in this page\nChange the code or continue?\n(0:exit 1:continue 2:continue and remember my choice)")
        opt=input()
        if opt==0:
            browser.close()
            p.stop()
            exit()
        else:
            continue
    with open("result.txt", "a", encoding="utf-8") as f:
        f.write('\n\n'+theTitle+'\n\n')
        for aLine in conText:
            ops=False
            ch=aLine.getText()
            for a in filter:
                if(a in ch):
                    ops=True
                    break
            if ops:
                continue
            f.write(ch)
    page.close()
    nowUrl=nextLink
    print(f"nextLink:{nextLink}")
