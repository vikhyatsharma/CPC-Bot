import requests
import bs4
import json

res = requests.get('https://clist.by/')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
match = soup.find_all('a',class_='data-ace')

all_competition = []
leetcode = []
atcoder = []
codechef = []
codeforces = []

for i in range(len(match)):
    all_competition.append(json.loads(match[i]['data-ace']))

for competition in all_competition:
  if competition['location'] == 'leetcode.com':
      leetcode.append(competition)
  elif competition['location'] == 'atcoder.jp':
      atcoder.append(competition)
  elif competition['location'] == 'codechef.com':
      codechef.append(competition)
  elif competition['location'] == 'codeforces.com':
      codeforces.append(competition)

def leetcode_update():
  return leetcode
def atcoder_update():
  return atcoder
def codechef_update():
  return codechef
def codeforces_update():
  return codeforces



