# -*- encoding: utf-8 -*-

from parsel import Selector
import re
import time
import requests
import quopri

import html2text
html2text = html2text.HTML2Text()
html2text.body_width = 0

def parse(body):
	document = Selector(text=body)
	title = document.css('title::text').extract_first()

	xpath = '//table[.//table[.//a[contains(text(), "%s")]]]' % title
	table = document.xpath(xpath)[-1]

	detection_strings = ['_____', 'Photographs may appear out of order']

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

			caption = row.css('td span::text').extract_first()
			piece['imageCaption'] = caption.encode('utf-8').strip() if caption else ''

			continue

		if [x for x in row.css('em::text, td::text').extract() for y in detection_strings if y in x.strip()]:
			if piece.get('title') and piece.get('image'):
				piece['pieceTextContent'] = piece['pieceTextContent'].strip('&nbsp;\n')
				pieces.append(piece)

			piece = piece = initiate_piece()
			continue

		headline = row.css('strong::text').extract()
		if piece.get('image') or headline:
			inner_html = row.css('td').extract_first()
			inner_html = clean_tags(['td'], inner_html)

			if not piece.get('number'):
				headline = ' '.join(headline)

				piece['number'], piece['title'] = [x.strip() for x in headline.split('.', 1)]
				piece['number'] = int(piece['number'].replace(' ', ''))

				inner_html = re.sub('</strong>\s*<strong>', '', inner_html)
				inner_html = re.sub('>\d{1,2}\s*. ', '>', inner_html)

			piece['pieceTextContent'] += html2text.handle(inner_html) + '&nbsp;\n'

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
	body = quopri.decodestring(body)
	data = Selector(text=body.decode('UTF-8'))

	link = data.xpath('//a[text()="Browser"]//@href').extract_first()
	print('News Url: %s' % link)

	response = requests.get(link)
	return response.text
