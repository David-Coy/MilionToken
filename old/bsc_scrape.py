import pdb, os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib.error
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl import load_workbook
import time

headers = {'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
#reg_url = "https://etherscan.io/token/0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611"
bsc_url = "https://bscscan.com/token/0xbf05279f9bf1ce69bbfed670813b7e431142afa4"
while True:
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    req = Request(url=bsc_url, headers=headers)
    try:
        if  urlopen(req).read():### Need to  have error pass here 
            html = urlopen(req).read() 
            soup = BeautifulSoup(html,'html.parser')
            #print(soup.prettify())
            #pdb.set_trace()
            price = float(soup.body.find_all('span', attrs={'class': 'd-block'})[12].text.split(' ')[0].split('$')[1])
            holders = float(soup.body.find('div', attrs={'class': 'mr-3'}).getText().split(' ')[0].split('\n')[1].replace(',',''))
            market_cap = float(soup.body.find_all('span', attrs={'class':'d-block'})[-1].getText().split('$')[1].split('\n')[0].replace(',',''))

            df = pd.DataFrame({'Date-Time': [time.ctime()],
                        'Date': [now.date()],
                        'Year': [now.year],
                        'Month': [now.month],
                        'Day': [now.day],
                        'Hour': [now.hour],
                        'Minute': [now.minute],
                        'Second': [now.second],
                        'Time': [now.ctime().split(' ')[3]],
                        'Price': [price],
                        'Holders': [holders],
                        'Market Cap [$USD]': [market_cap]
                        })
            print(df)
            #pdb.set_trace()
            #df.to_excel('data.xlsx', index=False)
            with open('data_bsc.csv', 'a') as f: # 'a' is for append mode
                df.to_csv(f, header=False)

        
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
        print('URLError: {}'.format(e.reason))

    time.sleep(60*1)# This will pause it every 5 minutes so as not to get kicked off server.