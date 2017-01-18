# -*- encoding: utf-8 -*-
from __future__ import print_function
import sys
import os
helpers_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, helpers_path)

import json
import nytimes
import contentful
import email

print('Loading lambda function')
def lambda_handler(event, context):
	message = event['Records'][0]['Sns']['Message']
	print(message)

	content = message['content']
	mail = email.message_from_string(content)
	message = mail.get_payload()[1].get_payload()

	response = nytimes.get_complete_briefings(message)
	briefing, pieces = nytimes.parse(response)

	briefing['piece'] = [contentful.create_piece(piece) for piece in pieces]
	response = contentful.create_briefings(briefing)

	return message
