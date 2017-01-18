# -*- encoding: utf-8 -*-
import requests
import json

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

def create_asset(image, title, caption):
	asset = {
		'title': title,
		'description': caption,
		'file': {
			'contentType': 'image/jpg',
			'fileName': "briefing 1-%s.jpg" % title,
			'upload': image
		}
	}

	response = requests.post(assets_url, data=contentful_payload(asset), headers=contentful_headers('asset'))
	data = json.loads(response.text)

	asset_id = data['sys']['id']
	process_asset(asset_id)
	publish_asset(asset_id)

	return contentful_link(asset_id, 'Asset')

def create_piece(piece):
	print('Creating Piece: %s' % piece['title'])
	piece['image'] = create_asset(piece['image'], piece.pop('title'), piece['imageCaption'])

	response = requests.post(url, data=contentful_payload(piece), headers=contentful_headers('piece'))
	data = json.loads(response.text)

	piece_id = data['sys']['id']
	publish_entry(piece_id)
	return contentful_link(piece_id, 'Entry')

def create_briefings(briefing):
	response = requests.post(url, data=contentful_payload(briefing), headers=contentful_headers('briefing'))
	data = json.loads(response.text)

	briefing_id = data['sys']['id']
	publish_entry(briefing_id)
	return response

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
	print('Publishing Entry: %s' % sys_id)
	response = requests.put(publish_entry_url % (space_id, sys_id), headers=publish_header(1))

	print(response.text)
	return response

def publish_asset(sys_id):
	print('Publishing Assets: %s' % sys_id)
	response = requests.put(publish_asset_url % (space_id, sys_id), headers=publish_header(2))

	print(response.text)
	return response

def process_asset(asset_id):
	print('Processing Assets: %s' % asset_id)
	response = requests.put(process_asset_url % (space_id, asset_id, locale), headers=contentful_headers(''))

	print(response.text)
	return response

def publish_header(version):
	return dict(contentful_headers(''), **{'X-Contentful-Version': unicode(version)})
