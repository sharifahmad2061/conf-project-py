import requests as req
from bs4 import BeautifulSoup as bs
from bs4 import Tag
import json
import html5lib

# -------------------------
# base_url = 'http://www.espncricinfo.com/bangladesh/content/player/caps.html?country=25;class={}'
# base_url = 'http://www.espncricinfo.com/southafrica/content/player/caps.html?country=3;class={}'
# base_url = 'http://www.espncricinfo.com/newzealand/content/player/caps.html?country=5;class={}'
# base_url = 'http://www.espncricinfo.com/westindies/content/player/caps.html?country=4;class={}'
# base_url = 'http://www.espncricinfo.com/srilanka/content/player/caps.html?country=8;class={}'
# base_url = 'http://www.espncricinfo.com/ireland/content/player/caps.html?country=29;class={}'
# base_url = 'http://www.espncricinfo.com/zimbabwe/content/player/caps.html?country=9;class={}'
base_url = 'http://www.espncricinfo.com/afghanistan/content/player/caps.html?country=40;class={}'

test_caps = req.get(base_url.format(1))
# with open('test_caps.html', 'w') as lf:
#     lf.write(test_caps.content.decode())
odi_caps = req.get(base_url.format(2))
# with open('odi_caps.html', 'w') as lf:
#     lf.write(odi_caps.content.decode())
t20_caps = req.get(base_url.format(3))
# with open('t20_caps.html', 'w') as lf:
# lf.write(t20_caps.content.decode())
print('stage 1 completed')

# -----------------------------------
test_caps_html = bs(test_caps.content.decode(),
                    'html5lib').find(class_='ciPlayerbycapstable').ul
odi_caps_html = bs(odi_caps.content.decode(),
                   'html5lib').find(class_='ciPlayerbycapstable').ul
t20_caps_html = bs(t20_caps.content.decode(),
                   'html5lib').find(class_='ciPlayerbycapstable').ul

# --------------------------------
test_players = {}
for player in test_caps_html:
    if not isinstance(player, Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        test_players[key] = value

# ---------------------------------
odi_players = {}
for player in odi_caps_html:
    if not isinstance(player, Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        odi_players[key] = value

# ------------------------------------
t20_players = {}
for player in t20_caps_html:
    if not isinstance(player, Tag):
        continue
    else:
        key = player.ul.contents[3].text
        try:
            value = player.ul.contents[3].a['href']
        except KeyError:
            print('url for {} does not exist'.format(key))
            value = None
        t20_players[key] = value
print('stage 2 completed')

# --------------------------------------
unique_players = {}
# append test players
for player, history in test_players.items():
    temp = {}
    temp['url'] = history
    # f is for formats played
    temp['f'] = ['test']
    unique_players[player] = temp
# append odi players
for player, history in odi_players.items():
    try:
        if unique_players[player] and unique_players[player]['url'] == history:
            unique_players[player]['f'].append('odi')
    except KeyError:
        temp = {}
        temp['url'] = history
        # f is for formats played
        temp['f'] = ['odi']
        unique_players[player] = temp
# append t20 players
for player, history in t20_players.items():
    try:
        if unique_players[player] and unique_players[player]['url'] == history:
            unique_players[player]['f'].append('t20')
    except KeyError:
        temp = {}
        temp['url'] = history
        # f is for formats played
        temp['f'] = ['t20']
        unique_players[player] = temp
print('stage 3 completed')
print(len(unique_players))

# -------------------------------------
with open('AFGInternationalPlayers.json', 'w') as lf:
    json.dump(unique_players, lf)
