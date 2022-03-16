import requests
import bs4
import json

res = requests.get('https://www.facebook.com/')

print(res.text)