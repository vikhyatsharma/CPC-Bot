import json
import clist
from datetime import datetime, timezone
from os import path
import pytz
import discord
import time
import calendar
# date_format = "%Y-%m-%d %H:%M:%S%z"
date_format = "%B %d, %Y %H:%M:%S%z"

class BOT:
    def __init__(self, file='db.json'):
        self.db = file

    def discover_new_contests(self,):
        discovered_contests = {
            "leetcode": clist.leetcode_update(),
            "atcoder": clist.atcoder_update(),
            # "codechef": clist.codechef_update(),
            "codeforces": clist.codeforces_update(),
        }

        new_contests = {}
        saved_contests = self.get_saved_contests()
        for site, contests in discovered_contests.items():
            new_contests[site] = []
            for contest in contests:
                saved_contests_for_current_site = saved_contests[site] if site in saved_contests else []
                if contest['title'] not in [cont['title'] for cont in saved_contests_for_current_site if 'title' in cont]:
                    new_contests[site].append(contest)

        return new_contests

    def get_saved_contests(self,):
        if path.exists(self.db):
            with open(self.db) as f:
                all_contests = json.load(f)
        else:
            all_contests = {}
        return all_contests

    def remove_old_contests(self,):
        all_contests = self.get_saved_contests()
        new_contests = {}
        for site, contests in all_contests.items():
            new_contests[site] = [contest for contest in contests if datetime.strptime(contest['time']['end']+contest['time']['zone'], date_format)\
                                    > datetime.now(datetime.strptime(contest['time']['end']+contest['time']['zone'], date_format).tzinfo)]
        with open(self.db, 'w+') as f:
            json.dump(new_contests, f, indent = 4, default=str) 

    def add_new_contests(self, new_contests):
        new_contests = self.discover_new_contests()
        current_contests = self.get_saved_contests()
        for site, contests in new_contests.items():
            if site not in current_contests:
                current_contests[site] = []
            for contest in contests:
                current_contests[site].append(contest)
        with open(self.db, 'w+') as f:
            json.dump(current_contests, f, indent = 4, default=str) 

    def update_contests(self,):
        self.remove_old_contests()
        new_contests = self.discover_new_contests()
        self.add_new_contests(new_contests)

    def time_convert(self,time_UTC):
        dic ={
            "January":"01",
            "February":"02",
            "March":"03",
            "April":"04",
            "May":"05",
            "June":"06",
            "July":"07",
            "August":"08",
            "September":"09",
            "October":"10",
            "November":"11",
            "December":"12",
        }
        parts = time_UTC.split()
        parts[1] = parts[1][:-1]
        parts[0] = dic[parts[0]]
        correct_format = parts[2] + '-' + parts[0] + '-' + parts[1] + ' ' + parts[3]
        time_tuple = time.strptime(correct_format, "%Y-%m-%d %H:%M:%S")
        t = calendar.timegm(time_tuple)
        current_zone_time = time.ctime(t)

        return current_zone_time

    def list_new_contests(self,):
        leetcode_icon = 'https://leetcode.com/favicon-192x192.png'
        atcoder_icon = 'https://img.atcoder.jp/assets/atcoder.png'
        codeforces_icon = 'https://sta.codeforces.com/s/58287/android-icon-192x192.png'
        temp_icon = 'https://i.imgur.com/axLm3p6.jpeg'
        temp_color = 0xff0000
        cards = []
        output = ""
        all_new_contests = self.discover_new_contests()
        for site, contests in all_new_contests.items():
            if len(contests) > 0:
                output += site + ":\n"
                for contest in contests:
                    if contest['location'].split('.')[0] == 'leetcode':
                        temp_icon = leetcode_icon
                        temp_color = 0xff8800
                    elif contest['location'].split('.')[0] == 'atcoder':
                        temp_icon = atcoder_icon
                        temp_color = 0xfafafa
                    elif contest['location'].split('.')[0] == 'codeforces':
                        temp_icon = codeforces_icon
                        temp_color = 0x08bbf7
                    embed=discord.Embed(title=contest['desc'].split()[1], url=contest['desc'].split()[1],description= contest['title'],color=temp_color)
                    embed.set_author(name=contest['location'].split('.')[0], icon_url=temp_icon)
                    embed.set_thumbnail(url=temp_icon)
                    embed.add_field(name="Start", value=self.time_convert(contest['time']['start']), inline=True)
                    print("1",contest['time']['start'],"2",self.time_convert(contest['time']['start']))
                    embed.add_field(name="End", value=self.time_convert(contest['time']['end']), inline=True)
                    cards.append(embed)
        self.update_contests()
        return cards

