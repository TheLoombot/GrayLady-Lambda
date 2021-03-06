# -*- encoding: utf-8 -*-

from parsel import Selector
import re
from datetime import datetime
import requests
import quopri

from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs

import html2text
html2text = html2text.HTML2Text()
html2text.body_width = 0

def parse(body):
	document = Selector(text=body)
	title = document.css('title::text').extract_first()

	xpath = '//table[.//table[.//a[contains(text(), "%s")]]]' % title
	table = document.xpath(xpath)[-1]

	detection_strings = ['_____', 'Photographs may appear out of order']
	sanitize_regex = [
		('</strong>\s*<strong>', ''),
		('>\d{1,2}\s*. ', '>'),
		('<strong>\s*</strong>', ''),
	]

	briefing = create_briefing(table)

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
				piece['pieceTextContent'] = piece['pieceTextContent'].strip('\n\n')
				pieces.append(piece)

			piece = initiate_piece()
			continue

		headline = row.css('strong::text').extract()
		if piece.get('image') or headline:
			inner_html = row.css('td').extract_first()
			inner_html = clean_tags(['td'], inner_html)

			inner_html = re.sub('title="(.*?)"', '', inner_html)

			if not piece.get('number'):
				headline = ' '.join(headline)
				piece['number'], piece['title'] = [x.strip() for x in headline.split('.', 1)]

				for regex in sanitize_regex:
					inner_html = re.sub(regex[0], regex[1], inner_html)

				piece['number'] = int(piece['number'].replace(' ', ''))
				if piece['title'] == '':
					piece['title'] = str(piece['number'])

			content = '\n\n' + html2text.handle(inner_html).strip()
			piece['pieceTextContent'] += remove_link_params(content, row)

	return briefing, pieces

def create_briefing(document):
	date = date_time_now_iso_format()
	title = document.css('a::text').extract_first().strip()

	xpath = '//h6[contains(text(), "By ")]//text()'
	authors = document.xpath(xpath).extract_first().replace('By ', '').strip()

	briefing = {
		'briefingDate': date,
		'briefingTitle': title,
		'briefingAuthor': authors
	}

	return briefing

def clean_tags(tags, html):
	for tag in tags:
		html = re.sub('<%s(.*?)>' % tag, '', html).replace('</%s>' % tag, '').strip()
	return html

def initiate_piece():
	return {
		'date': date_time_now_iso_format(),
		'pieceTextContent': ''
	}

def get_complete_briefings(body):
	body = quopri.decodestring(body)
	data = Selector(text=body.decode('UTF-8'))

	link = data.xpath('//a[text()="Browser"]//@href').extract_first()
	print('News Url: %s' % link)

	response = requests.get(link)
	return response.text

def date_time_now_iso_format():
	return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

def remove_link_params(content, row):
	unwanted_query_tags = ['te', 'nl', 'emc', '_r']

	urls = row.css('a::attr(href)').extract()
	for url in urls:
		link = urlparse(url)

		query = parse_qs(link.query)
		[query.pop(tag) for tag in unwanted_query_tags if tag in query]

		link = link._replace(query=urlencode(query, True))
		content = content.replace(url, urlunparse(link))
	return content
