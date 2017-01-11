# -*- encoding: utf-8 -*-

from parsel import Selector
import re
from html2text import html2text
import time

def parse(data):
	body = Selector(text=data.decode('UTF-8'))
	css = 'table table[style="padding:0;background-color:#fff"] tr'
	detection_strings = ['_____', 'Photographs may appear out of order']
	rgx = '>(\d+)\.'
	image_url = 'https://static01.nyt.com'

	briefing = {}
	briefing['briefingDate'] = time.strftime('%Y-%m-%d')
	for row in body.css(css):
		title = row.css('a[style*="font-size:32px;line-height:36px;"]::text').extract_first()
		if title:
			briefing['briefingTitle'] = title.strip()
			continue

		if briefing.get('briefingTitle') and not briefing.get('briefingAuthor'):
			author = row.css('h6::text').extract_first().strip()
			
			if author:
				briefing['briefingAuthor'] = author.replace('By ', '')
				break

	pieces = []
	piece = initiate_piece()
	for row in body.css(css):
		image_tag = row.css('td img::attr(src)').extract_first()
		if image_tag:
			image = image_tag.strip().split(image_url)[-1]
			piece['image'] = image_url + image.replace('-articleLarge.jpg', '-superJumbo.jpg')

			caption = row.css('td span::text').extract_first().encode('utf-8')
			piece['imageCaption'] = caption.split(' — ', 1)[0].strip()

			continue

		if [x for x in row.css('em::text, td::text').extract() for y in detection_strings if y in x.strip()]:
			pieces.append(piece)

			piece = piece = initiate_piece()
			continue

		if piece.get('image'):
			html = row.css('td').extract_first()
			html = re.sub('<td(.*?)>', '', html).strip('</td>').strip()

			if not piece.get('number'):
				number = re.findall(rgx, html)[0].strip()
				piece['number'] = int(number)
				
				html = re.sub(rgx, '', html)

			piece['pieceTextContent'] += html2text(html).strip()

	return briefing, pieces

def initiate_piece():
	return {
		'date': time.strftime('%Y-%m-%d'),
		'pieceTextContent': ''
	}
