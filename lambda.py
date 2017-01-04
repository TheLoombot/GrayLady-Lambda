# -*- encoding: utf-8 -*-

from parsel import Selector
import re
from html2text import html2text
import time


def main():
	with open('sample.html', 'r') as html:
		data = html.read()

	body = Selector(text=data.decode('UTF-8'))

	css = 'table table[style="padding:0;background-color:#fff"] tr'
	pieces = []

	briefing = {}
	briefing['Date'] = time.strftime('%d/%m/%Y')

	piece = {}
	piece['Text Content'] = ''

	detection_strings = ['_____', 'Photographs may appear out of order']

	for row in body.css(css):

		title = row.css('a[style*="font-size:32px;line-height:36px;"]::text').extract_first()
		if title:
			briefing['Title'] = title.strip()
			continue

		if briefing.get('Title') and not briefing.get('Author'):
			briefing['Author'] = row.css('h6::text').extract_first().strip()
			continue

		image_tag = row.css('td img::attr(src)').extract_first()
		if image_tag:
			piece['Image'] = image_tag.strip()
			piece['Image Caption'] = row.css('td span::text').extract_first().strip()

			continue

		if [x for x in row.css('em::text, td::text').extract() for y in detection_strings if y in x.strip()]:
			pieces.append(piece)

			piece = {}
			piece['Text Content'] = ''

			continue

		if piece.get('Image'):
			html = row.css('td').extract_first()
			html = re.sub('<td(.*?)>', '', html).strip('</td>').strip()

			markdowm = html2text(html).replace('\\. ****', '. ')
			piece['Text Content'] += markdowm.strip()

	import pdb
	pdb.set_trace()

	return pieces


main()