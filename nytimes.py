# -*- encoding: utf-8 -*-

from parsel import Selector
import re
from html2text import html2text
import time

def parse(data):
	body = Selector(text=data.decode('UTF-8'))
	css = 'table table[style="padding:0;background-color:#fff"] tr'
	detection_strings = ['_____', 'Photographs may appear out of order']
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
			inner_html = row.css('td').extract_first()
			inner_html = re.sub('<td(.*?)>', '', inner_html).strip('</td>').strip()

			if not piece.get('number'):
				headline = ' '.join(row.css('strong::text').extract())
				piece['number'], piece['title'] = [x.strip() for x in headline.split('.', 1)]
				piece['number'] = int(piece['number'])

				inner_html = clean_text_part(inner_html, row)
				
			piece['pieceTextContent'] += html2text(inner_html).strip()

	return briefing, pieces

def clean_text_part(inner_html, row):
	rgx = '>(\d+)\.'
	strong = row.css('strong::text')

	inner_html = inner_html.split('</strong>', 1)[-1] if len(strong) > 1 else re.sub(rgx, '', inner_html)
	return inner_html.strip()

def initiate_piece():
	return {
		'date': time.strftime('%Y-%m-%d'),
		'pieceTextContent': ''
	}
