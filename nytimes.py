# -*- encoding: utf-8 -*-

from parsel import Selector
import re
from html2text import html2text
import time
import requests

def parse(body):
	document = Selector(text=body)
	css = 'table.layout-300.te-600[style="padding: 0; background-color: #fff;"]'
	table = document.css(css)[0]

	detection_strings = ['_____', 'Photographs may appear out of order']
	image_url = 'https://static01.nyt.com'

	briefing = {
		'briefingDate': time.strftime('%Y-%m-%d'),
		'briefingTitle': table.css('a::text').extract_first().strip(),
		'briefingAuthor': table.xpath('//h6[contains(text(), "By ")]//text()').extract_first().replace('By ', '').strip()
	}

	pieces = []
	piece = initiate_piece()
	for row in table.css('tr'):
		image_tag = row.css('td img::attr(src)').extract_first()
		if image_tag:
			piece['image'] = image_tag.replace('-articleLarge.jpg', '-superJumbo.jpg')
			piece['imageCaption'] = row.css('td span::text').extract_first().encode('utf-8').strip()

			continue

		if [x for x in row.css('em::text, td::text').extract() for y in detection_strings if y in x.strip()]:
			
			pieces.append(piece)
			piece = piece = initiate_piece()

			continue

		if piece.get('image'):
			inner_html = row.css('td').extract_first()
			inner_html = clean_tags(['td', 'strong'], inner_html)

			if not piece.get('number'):
				headline = ' '.join(row.css('strong::text').extract())
				piece['number'], piece['title'] = [x.strip() for x in headline.split('.', 1)]
				piece['number'] = int(piece['number'])

				inner_html = inner_html.split('.', 1)[-1].strip()

			piece['pieceTextContent'] += html2text(inner_html).replace('\n', ' ').strip() + '\n'

	return briefing, pieces

def clean_tags(tags, html):
	for tag in tags:
		html = re.sub('<%s(.*?)>' % tag, '', html).replace('</%s>' % tag, '').strip()
	return html

def initiate_piece():
	return {
		'date': time.strftime('%Y-%m-%d'),
		'pieceTextContent': ''
	}

def get_complete_briefings(body):
	data = Selector(text=body.decode('UTF-8'))

	link = data.xpath('//a[text()="Browser"]//@href').extract_first()
	response = requests.get(link)

	return response.text
