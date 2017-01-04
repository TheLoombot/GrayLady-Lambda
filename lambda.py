# -*- encoding: utf-8 -*-
import sys
import os
helpers_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, helpers_path)

import nytimes

def main():
	with open('sample.html', 'r') as html:
		data = html.read()

	briefing, pieces = nytimes.parse(data)

main()