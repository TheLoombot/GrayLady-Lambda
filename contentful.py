# -*- encoding: utf-8 -*-
import requests
import json

access_token = 'ce03285b239a8bebc753266729ec5f8bbaf28dedba2d63721728ce850af99f09'
locale = 'en-US'

def create_briefings(briefing):
	url = 'https://api.contentful.com/spaces/clmzlcmno5rw/entries'
	
	response = requests.post(url, data=briefing_payload(briefing), headers=briefing_headers())
	return response

def briefing_headers():
	return {
		'Authorization': 'Bearer ' + access_token,
		'Content-Type': 'application/vnd.contentful.management.v1+json',
		'X-Contentful-Content-Type': 'briefing'
	}

def briefing_payload(briefing):
	return json.dumps({'fields' : {key: {locale: briefing[key]} for key in briefing}})