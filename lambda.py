# -*- encoding: utf-8 -*-
import sys
import os
helpers_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, helpers_path)

import nytimes
import contentful

def main():
	with open('sample.html', 'r') as html:
		data = html.read()


	briefing, pieces = nytimes.parse(data)
	pieces = [pieces[1]]

	piece_ids = []
	[piece_ids.append(contentful.create_piece(piece)) for piece in pieces]


	# response = contentful.create_briefings(briefing)

main()