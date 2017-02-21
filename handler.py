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
import copy
import boto3

print('Loading lambda function')
def lambda_handler(event, context):
	message = event['Records'][0]['Sns']['Message']
	print(message)

	if not isinstance(message, dict):
		message = json.loads(message)
	content = message['content']

	mail = email.message_from_string(content)
	multiparts = mail.get_payload()
	if isinstance(multiparts, str):
		message = multiparts
	else:
		message = multiparts[1].get_payload()

	response = nytimes.get_complete_briefings(message)
	briefing, pieces = nytimes.parse(response)

	briefing['piece'] = []
	for piece in copy.deepcopy(pieces):
		try:
			briefing['piece'].append(contentful.create_piece(piece))
		except Exception, e:
			continue

	response = contentful.create_briefings(briefing)
	return publish_sns_topic(briefing, pieces)


def publish_sns_topic(briefing, pieces):
	body = {
		'title': briefing['briefingTitle'],
		'authors': briefing['briefingAuthor'],
		'date': briefing['briefingDate'],
		'image': pieces[0]['image'],
	}

	alert = {
		'body': body,
		'title': 'Title goes Here',
		'subtitle': 'Sub title here',
	}

	message = {
		'default': 'Irrelevant',
		'APNS_SANDBOX': {
			'aps': {
				'alert': alert,
			}
		}
	}

	print('\nSNS Topic: %s' % message)
	client = boto3.client('sns')
	response = client.publish(
		TargetArn='arn:aws:sns:us-east-1:467509107760:outbound_push',
		Message=json.dumps(message),
		MessageStructure='json'
	)

	print('\nSNS Topic Response: %s' % response)
	return response
