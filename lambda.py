# -*- encoding: utf-8 -*-

from parsel import Selector
from html2text import html2text
import requests



import pdb
pdb.set_trace()


url = 'http://www.nytimes.com/newsletters/2016/12/29/evening-briefing?nlid=1833217'
body = requests.get(url)

response = Selector(text=body.text)
rows = response.css('table[@class*="outer-layout"] tr')