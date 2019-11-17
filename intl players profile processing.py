import requests as req
from bs4 import BeautifulSoup as bs
from bs4 import Tag
import os
import time
import json
import html5lib

# --------------------------------
profiles = []
os.chdir('NZD_player_profiles')
profiles = os.listdir()
for file in profiles:
    # for avoiding directories
    if os.path.isdir(file):
        continue
    # if file is not html file then continue for avoiding .ini file
    if not '.html' in file:
        continue
    player_profile = {}
    with open(file, 'r') as lf:
        s = lf.read()  # read file
        html = bs(s, 'html5lib').find(class_='pnl490M')
        player_profile['country'] = html.div.div.h3.text.strip()
        # -----------------------------------------------
        # player detail such as name, born, teams played
        dtl = html.contents[3].div
        for p in dtl.find_all('p'):
            if isinstance(p, Tag):
                # join used for brother and father relation span
                player_profile[p.b.text.strip().lower()] = ''.join(
                    span.text.strip().lower() for span in p.find_all('span'))
        # -------------------------------------
        # player batting and fielding statistics
        bfavg = html.contents[5].span.text.strip().lower()
        player_profile[bfavg] = ''
        tbl = html.contents[7]
        player_profile[bfavg] = player_profile[bfavg] + (
            ''.join(heading.text.strip() + '|' for heading in tbl.thead.tr
                    if isinstance(heading, Tag)) + '\n')
        for row in tbl.tbody:
            if isinstance(row, Tag):
                player_profile[bfavg] = player_profile[bfavg] + (
                    ''.join(item.text.strip() + '|' for item in row
                            if isinstance(item, Tag)) + '\n')
        #------------------------------------------
        # player bowling statistics
        bowlavg = html.contents[9].span.text.strip().lower()
        player_profile[bowlavg] = ''
        tbl = html.contents[11]
        player_profile[bowlavg] += (
            ''.join(heading.text.strip() + '|' for heading in tbl.thead.tr
                    if isinstance(heading, Tag)) + '\n')
        for row in tbl.tbody:
            if isinstance(row, Tag):
                player_profile[bowlavg] += (
                    ''.join(item.text.strip() + '|' for item in row
                            if isinstance(item, Tag)) + '\n')
        # -----------------------------------------------
        # debuts details
        debuts = html.contents[15].tbody
        for row in debuts.find_all('tr', class_='data2'):
            if not isinstance(row, Tag):
                continue
            key = row.td.b.text.strip().lower()
            #             s = row.contents[3].next_element.strip()
            #             print(s,file)
            #             i = s.index(',')
            #             value = [s[:i].strip(),s[i+1:].strip()]
            player_profile[key] = row.contents[3].next_element.strip()
        # domestic debuts missed due to class selection above
#         print(len())
        ddebuts = list(debuts.find_all('tr', class_='data1'))
        ddebuts.reverse()
        #         print(len(ddebuts) if ddebuts != None)
        #         if ddebuts != None:
        #             print(len(ddebuts))
        if ddebuts != None and len(ddebuts) > 0:
            for index, dd in enumerate(ddebuts):
                if not index < 3:
                    break
                key = dd.td.b.text.strip().lower()
                player_profile[key] = dd.contents[3].next_element.strip()
    # ------------------------------
    # write player profile to json file
    os.chdir('processed_profiles')
    with open(file.split('.')[0] + '.json', 'w') as lf:
        json.dump(player_profile, lf)
        print('#')
        del player_profile
        del html
        del debuts
        del ddebuts, dtl, bowlavg, bfavg, tbl
    os.chdir('..')
