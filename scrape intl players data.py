import requests as req
import os
import time
import json

# ------------------------------
unique_players = {}
with open(r'intl player db\SLInternationalPlayers.json', 'r') as lf:
    unique_players = json.load(lf)

# --------------------------------
espn = 'http://www.espncricinfo.com{}'

# --------------------------------
os.chdir('SL_player_profiles')
for index, plyr in enumerate(unique_players):
    # download player profile page
    try:
        res = req.get(espn.format(
            unique_players[plyr]['url'])).content.decode()
    except:
        print('{} profile can\'t be downloaded'.format(plyr))
    # store in local file
    with open(plyr + '_profile.html', 'w', encoding='utf-8') as lf:
        lf.write(res)
    print('#', end='')
    if (index >= 20) and (index % 20 == 0):
        print('sleeping for 5 seconds')
        time.sleep(5)
os.chdir('..')