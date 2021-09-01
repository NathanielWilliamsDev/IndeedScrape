# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 07:33:19 2021

@author: Natha
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://au.indeed.com/jobs?q=software+developer&l=Sydney+NSW&start={page*10}'
    r = requests.get(url, headers) # 200 is OK, 404 is page not found
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# <span title="API Developer"> API Developer </span>
def transform(soup):
    divs = soup.find_all('div', class_ = 'slider_container')
    for item in divs:
        if item.find(class_ = 'label'):
            continue # need to fix, if finds a job that has a 'new' span before the title span, skips job completely
        title = item.find('span').text.strip()
        company = item.find('span', class_ = "companyName").text.strip()
        description = item.find('div', class_ = "job-snippet").text.strip().replace('\n', '')
        try:
            salary = item.find('span', class_ = "salary-snippet").text.strip()
        except:
            salary = ""
        
        job = {
                'title': title,
                'company': company,
                'salary': salary,
                'description': description
        }
        jobList.append(job)
#        print("Seeking a: "+title+" to join: "+company+" paying: "+salary+". Job description: "+description) 
    return

jobList = []

# go through multiple pages
for i in range(0,100, 10): #0-40 stepping in 10's
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

print(len(jobList))

df = pd.DataFrame(jobList)
print(df.head())
df.to_csv('jobs.csv')

# You can write:
# item.find('div', {'class' : 'job-snippet'}).text.strip()
# OR item.find('div', class_ = 'job-snippet').text.strip()