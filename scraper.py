from bs4 import BeautifulSoup
import urllib
import datetime
import json
from win11toast import toast

with open('list.txt','r') as f:
    vns = f.readlines()

with open('dates.json','r') as f:
    dates = json.load(f)

for i in vns:

    name = i.lower().strip()
    name = name.split(' ')
    name = '-'.join(name)

    url = f'http://dikgames.com/{name}/'
    hdr = {'User-Agent': 'Mozilla/5.0'}

    try:
        request = urllib.request.Request(url,headers=hdr) 
        response = urllib.request.urlopen(request)
        htmldata = response.read()
        soup = BeautifulSoup(htmldata, 'html.parser')

        update_date = soup.find_all("span", class_="last-updated")[0].contents[0][14:]
        update_date = datetime.datetime.strptime(update_date, '%B %d, %Y').date()
    except:
        print(f"Couldn't fetch data for {name}")
        continue

    flag = True

    if(name in dates.keys()):
        prev_date = datetime.datetime.strptime(dates[name], '%B %d, %Y').date()
        if(prev_date==update_date):
            flag = False
    dates[name]=update_date.strftime('%B %d, %Y')

    if(flag):
        heading = f'New Update for {name}'
        body = f'Updated on {update_date}'
        open_link = {'activationType': 'protocol', 'arguments': url, 'content': 'Open Link'}
        try:
            a = 1/0
            toast(heading,body,on_click=url,buttons=[open_link,'Dismiss'])
        except:
            print('-------------------------')
            print(heading)
            print(body)
            print(url)

with open('dates.json','w') as f:
    dates = json.dump(dates,f)