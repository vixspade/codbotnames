"""
bot name parser and distributor
example data: Fireheart,THDR,vix
"""

import tomllib
import os

botcsv = open("bots.csv", "r")
config = tomllib.load(open("config.toml", "rb"))
mode = config['script']['tag']

# warn user of possibly mistyped settings
if mode.lower() not in ['clan', 'owner', 'none']:
    print(f"WARNING: Clan tag mode is currently set to '{mode}'."
          " The script will ignore this setting, default to 'none' and won't give bots clan tags."
          f"\nPress any key to proceed, or manually close the window to interrupt.")
    input()
clanstr = config['script']['adapt']
if 'clan' not in clanstr.lower():
    print(f"WARNING: 'clan' keyword not found in '{clanstr}'."
          " The script will ignore this setting and won't give bots ADAPTED clan tags."
          f"\nPress any key to proceed, or manually close the window to interrupt.")
    input()

# get rid of \n's from the file
botlines = botcsv.readlines()
botlines = [w.replace('\n', '') for w in botlines]

botstxt = open("bots.txt", "w")
informed = False  # this is for the warning just below
for bot in botlines:
    botinfo = bot.split(',')
    if len(botinfo[0]) >= 15 and informed is False:
        # by the way games without clan tags don't have this problem i think?
        # CoD4 doesn't at least
        print(f"WARNING: Name '{botinfo[0]}' is {len(botinfo[0])} characters long"
              f" and may not display correctly in-game."
              f"\nModern Warfare 2 & 3 cut names off at 15 characters;"
              f" in this case, the name may show up as '{botinfo[0][:14]}'."
              f"\nPress any key to proceed, or manually close the window to interrupt."
              f" This message won't appear again until the script finishes.")
        input()
        informed = True
    if mode.lower() == 'clan':
        line = botinfo[0] + "," + botinfo[1]
    elif mode.lower() == 'owner':
        line = botinfo[0] + "," + botinfo[2]
    else:
        line = botinfo[0]
    botstxt.write(line + "\n")

# make a directory if it doesn't exist already
try:
    botsnctxt = open("noclan/bots.txt", "w")
except FileNotFoundError:
    os.makedirs('noclan')
    botsnctxt = open("noclan/bots.txt", "w")

for bot in botlines:
    botinfo = bot.split(',')
    if "clan" in clanstr.lower():
        if mode.lower() == 'clan':
            line = clanstr.replace('clan', botinfo[1]) + botinfo[0]
        elif mode.lower() == 'owner':
            line = clanstr.replace('clan', botinfo[2]) + botinfo[0]
    else:
        line = botinfo[0]
    botsnctxt.write(line + "\n")
    