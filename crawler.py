import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime

def get_doubantitle(group, page, keywords=[]):
    href = []
    title = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    for i in range(page):
        url = 'https://www.douban.com/group/{}/discussion?start={}'.format(group,i*25)
        print('try to get page {}...'.format(i))
        r = requests.get(url,headers=headers)
        if r.status_code == 200:
            content = r.content
        else:
            print('Failed')
        print('cool.')
        soup = BeautifulSoup(content,"lxml")

        titleset = soup.find_all('td',class_ = 'title')

        for item in titleset:
            link = item.find('a')
            if link:
                thread_url = link.attrs['href']
                thread_title = link.attrs.get('title', '')
                print(f'Checking content for thread: {thread_title}')
                
                # Fetch the content of the thread
                thread_r = requests.get(thread_url, headers=headers)
                if thread_r.status_code == 200:
                    thread_content = thread_r.content
                    thread_soup = BeautifulSoup(thread_content, "lxml")
                    thread_text = thread_soup.get_text(separator=' ').lower()  # Get all text from the page and convert to lower case

                    # Check if any of the keywords are in the content
                    if any(keyword.lower() in thread_text for keyword in keywords):
                        href.append(thread_url)
                        title.append(thread_title)
                        print(f'Found matching content for title: {thread_title}')
                else:
                    print(f'Failed to retrieve content for thread: {thread_title}')
        print('page {} done, 1 seconds to next page'.format(i))
        time.sleep(1)

    return href,title

filter_keywords=["女性"]
href,title = get_doubantitle('GirlsLoveGames', 3, filter_keywords)

df = pd.DataFrame([title,href]).T
df.drop_duplicates(inplace= True)
df.index = range(df.shape[0])
df.to_csv('filename.csv', sep=',', header=True, index=False, encoding='utf-8', compression=None, columns=None)
print(df)