# -*- encoding: utf-8 -*-
import requests
import json
import time

# get this token from this page `	Login to get a token button	`
# https://www.contentful.com/developers/docs/references/authentication/#the-management-api
access_token = 'ce03285b239a8bebc753266729ec5f8bbaf28dedba2d63721728ce850af99f09'
space_id = 'clmzlcmno5rw'
locale = 'en-US'

url = 'https://api.contentful.com/spaces/%s/entries' % space_id
assets_url = 'https://api.contentful.com/spaces/%s/assets' % space_id
process_asset_url = 'https://api.contentful.com/spaces/%s/assets/%s/files/%s/process'
publish_asset_url = 'https://api.contentful.com/spaces/%s/assets/%s/published'

publish_entry_url = 'https://api.contentful.com/spaces/%s/entries/%s/published'

delay = 4

def create_asset(image, title, caption):
	asset = {
		'title': title,
		'description': caption,
		'file': {
			'contentType': 'image/jpeg',
			'fileName': "briefing 1-%s.jpg" % title,
			'upload': image
		}
	}

	data = requests.post(assets_url, data=contentful_payload(asset), headers=contentful_headers('')).json()
	asset_id = data['sys']['id']

	print('Create Assets: %s' % clean(data))

	process_asset(asset_id)
	publish_asset(asset_id)

	return contentful_link(asset_id, 'Asset')

def create_piece(piece):
	print('Creating Piece: %s' % piece['title'])
	piece['image'] = create_asset(piece['image'], piece.pop('title'), piece['imageCaption'])

	data = post_request(url, contentful_payload(piece), contentful_headers('piece'))
	piece_id = data['sys']['id']

	print('Creating piece: %s' % clean(data))

	publish_entry(piece_id)
	return contentful_link(piece_id, 'Entry')

def create_briefings(briefing):
	data = requests.post(url, data=contentful_payload(briefing), headers=contentful_headers('briefing')).json()

	print('Creating Briefing: %s' % clean(data))

	briefing_id = data['sys']['id']
	publish_entry(briefing_id)
	return data

def contentful_headers(content_type):
	return {
		'Authorization': 'Bearer ' + access_token,
		'Content-Type': 'application/vnd.contentful.management.v1+json',
		'X-Contentful-Content-Type': content_type
	}

def contentful_payload(resource):
	return json.dumps({'fields' : {key: {locale: resource[key]} for key in resource}})

def contentful_link(sys_id, link_type):
	return {
		'sys': {
			'type': 'Link',
			'linkType': link_type,
			'id': sys_id
		}
	}

def publish_entry(sys_id):
	time.sleep(delay)
	response = requests.put(publish_entry_url % (space_id, sys_id), headers=publish_header(1)).json()

	print('Publishing Entry: %s' % clean(response))
	return response

def publish_asset(sys_id):
	time.sleep(delay)
	response = requests.put(publish_asset_url % (space_id, sys_id), headers=publish_header(2)).json()

	print('Publishing Assets: %s' % clean(response))
	return response

def process_asset(asset_id):
	time.sleep(delay)
	response = requests.put(process_asset_url % (space_id, asset_id, locale), headers=contentful_headers(''))
	return response

def publish_header(version):
	return dict(contentful_headers(''), **{'X-Contentful-Version': unicode(version)})

def post_request(url, payload, headers):
	time.sleep(delay)
	response = requests.post(url, data=payload, headers=headers).json()
	return response

def clean(text):
	return ' '.join(str(text).split())
