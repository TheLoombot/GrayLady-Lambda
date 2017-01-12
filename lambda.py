# -*- encoding: utf-8 -*-
import sys
import os
helpers_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, helpers_path)

from __future__ import print_function
import json

import nytimes
import contentful
print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)

	response = nytimes.get_complete_briefings(message)
	briefing, pieces = nytimes.parse(response)
	
	briefing['piece'] = [contentful.create_piece(piece) for piece in pieces]
	response = contentful.create_briefings(briefing)    

    return message