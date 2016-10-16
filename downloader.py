
# coding: utf-8

# In[5]:

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from multiprocessing import Pool


# In[35]:

urls = []
page_num = 1
while True:
    r = requests.get("http://devpost.com/software/popular?query=is%3Afeatured&page=" + str(page_num))
    soup = BeautifulSoup(r.text, "lxml")
    projects = soup.findAll("div", {"class": "gallery-item"})
    if len(projects) == 0:
        break
    for i in projects:
        urls.append(i.find("a")['href'])
    page_num += 1


# In[119]:

def parse_user(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return len(soup.findAll("div", {"gallery-item"}))

def parse_post(url):    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    header = soup.find("header", {"id": "software-header"})
    title = ''
    title_tag = header.find("h1", {"id": "app-title"})
    if title is not None:
        title = title_tag.text
    subtitle = ''
    subtitle_tag = header.find("p", {"class": "large"})
    if subtitle_tag is not None:
        subtitle = subtitle_tag.text
    like_button = header.find("a", {"class": "like-button"})
    like_count = like_button.find("span", {"class": "side-count"}).text
    built_with = soup.find("div", {"id": "built-with"})
    categories = []
    if built_with is not None:
        for i in built_with.findAll("li"):
            span = i.find("span")
            if span is not None:
                categories.append(span.text)
        
    software_lh = soup.find("div", {"class": "software-list-content"})
    hackathon = ''
    winnings = []
    if software_lh is not None:
        hackathon = software_lh.find("a").text
        winnings = []
        prizes = software_lh.findAll("li")
        for i in prizes:
            winnings.append(i.text)
            
    body = soup.find("div", {"id": "app-details-left"})
    description = ''
    if body is not None:
        parts = []
        for h2, p in zip(body.findAll("h2"), body.findAll("p")):
            h2 = h2.text.replace("\n", "")
            if h2 != '':
                parts.append(h2)
            p = p.text.replace("\n", "")
            if p != '':
                parts.append(p)
        description = parts
        
    app_team = soup.find("section", {"id": "app-team"})
    team = []
    if app_team is not None:
        for i in app_team.findAll("a"):
            if i.text != '':
                team.append({"name": i.text, "url": i['href']})
        
    return {
        "title": title,
        "subtitle": subtitle,
        "like_count": like_count,
        "categories": categories,
        "hackathon": hackathon,
        "winnings": winnings,
        'description': description,
        'team': team
    }


# In[75]:

# a=parse_post(urls[1])


# # In[78]:

# body=a
# parts = []
# for h2, p in zip(body.findAll("h2"), body.findAll("p")):
    # parts.append(h2.text)
    # parts.append(p.text)
# descriptions = "\n".join(parts)


# In[88]:

# parse_post(urls[3])


# In[120]:

p = Pool(5)
data = p.map(parse_post, urls)
    
# data = []
# for i in urls:
#     data.append(parse_post(i))
    
with open("data.json", "w") as f:
    f.write(json.dumps(data))


# # In[96]:

# df = pd.read_json("./data.json")


# # In[14]:

# def clean_winnings(s):
    # s = s.replace("\n", "")
    # s = s.replace("Winner", "")
    # s = s.strip()
    # return s


# # In[98]:

# df['winnings'] = df['winnings'].apply(lambda x: list(map(clean_winnings, x)))
# df['num_cat'] = df['categories'].apply(lambda x: len(x))
# df['like_count'] = df['like_count'].astype(int)


# # In[29]:

# def isWinner(df):
    # df['winnings'] = df['winnings'].apply(lambda x: len(x) > 0)
    # return df


# # In[30]:

# df = isWinner(df)


# # In[102]:

# df['teamsize'] = df['team'].apply(lambda x: len(x))
# #df['total_hackathons_attended'] = df['team'].apply(lambda x: reduce(lambda acc, i: acc + int(i['hackathons_attended'], x, 0)))


# # In[103]:

# df


# # In[105]:

# tags = []
# for i in df['winnings']:
    # for w in i:
        # for tag in w.split(' '):
            # tags.append(tag.lower())


# # In[116]:

# counter = dict(map(lambda x: (x, 0), tags))


# # In[117]:

# for i in df['winnings']:
    # for w in i:
        # for tag in w.split(' '):
            # t = tag.lower()
            # counter[t] += 1


# # In[118]:




# # In[ ]:



