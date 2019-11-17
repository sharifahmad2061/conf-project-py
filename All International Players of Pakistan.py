#!/usr/bin/env python
# coding: utf-8

# # save the html pages for handling locally

# In[1]:


import requests as req
from bs4 import BeautifulSoup as bs
from bs4 import Tag, NavigableString
import os
import time
import json
import html5lib


# In[2]:


test_caps = req.get('http://www.espncricinfo.com/pakistan/content/player/caps.html?country=7;class=1')
with open('test_caps.html','w') as localfile:
    localfile.write(test_caps.content.decode())
odi_caps = req.get('http://www.espncricinfo.com/pakistan/content/player/caps.html?country=7;class=2')
with open('odi_caps.html','w') as localfile:
    localfile.write(odi_caps.content.decode())
t20_caps = req.get('http://www.espncricinfo.com/pakistan/content/player/caps.html?country=7;class=3')
with open('t20_caps.html','w') as localfile:
    localfile.write(t20_caps.content.decode())


# # read html files from local source

# In[3]:


with open('test_caps.html','r') as lf:
    test_caps = lf.read()
with open('odi_caps.html','r') as lf:
    odi_caps = lf.read()
with open('t20_caps.html','r') as lf:
    t20_caps = lf.read()


# # feed string file representation into beautiful soup

# In[4]:


test_caps_html = bs(test_caps,'html5lib').find(class_ = 'ciPlayerbycapstable').ul
odi_caps_html = bs(odi_caps,'html5lib').find(class_ = 'ciPlayerbycapstable').ul
t20_caps_html = bs(t20_caps,'html5lib').find(class_ = 'ciPlayerbycapstable').ul


# # convert response object to beautiful soup parsed tree

# In[5]:


test_caps_html = bs(test_caps.content.decode(),'html5lib').find(class_ = 'ciPlayerbycapstable').ul
odi_caps_html = bs(odi_caps.content.decode(),'html5lib').find(class_ = 'ciPlayerbycapstable').ul
t20_caps_html = bs(t20_caps.content.decode(),'html5lib').find(class_ = 'ciPlayerbycapstable').ul


# In[5]:


test_caps_html


# # start parsing all players from html

# ### test players

# In[6]:


test_players = {}
for player in test_caps_html:
    if not isinstance(player,Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        test_players[key] = value


# In[18]:


test_players


# ### odi players

# In[7]:


odi_players = {}
for player in odi_caps_html:
    if not isinstance(player,Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        odi_players[key] = value


# In[20]:


odi_players


# ### t20 players

# In[8]:


t20_players = {}
for player in t20_caps_html:
    if not isinstance(player,Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        t20_players[key] = value


# In[9]:


t20_players


# # Remove redundant players

# In[10]:


unique_players = {}


# #### append test players

# In[11]:


for player,history in test_players.items():
    temp = {}
    temp['url'] = history
    # f is for formats played
    temp['f'] = ['test']
    unique_players[player] = temp


# In[25]:


unique_players


# #### append odi players

# In[12]:


for player,history in odi_players.items():
    try:
        if unique_players[player] and unique_players[player]['url'] == history:
            unique_players[player]['f'].append('odi')
    except KeyError:
        temp = {}
        temp['url'] = history
        # f is for formats played
        temp['f'] = ['odi']
        unique_players[player] = temp


# In[28]:


unique_players


# #### append t20 players

# In[13]:


for player,history in t20_players.items():
    try:
        if unique_players[player] and unique_players[player]['url'] == history:
            unique_players[player]['f'].append('t20')
    except KeyError:
        temp = {}
        temp['url'] = history
        # f is for formats played
        temp['f'] = ['t20']
        unique_players[player] = temp


# In[30]:


unique_players


# # Write to json file

# In[14]:


with open('PakInternationalPlayers.json','w') as lf:
    json.dump(unique_players,lf)


# In[ ]:




