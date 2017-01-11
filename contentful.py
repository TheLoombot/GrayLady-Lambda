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
publish_asset_url = 'https://api.contentful.com/spaces/%s/assets/%s'

def create_piece(piece):
	piece['image'] = create_asset(piece['image'], piece['number'], piece['imageCaption'])

	response = requests.post(url, data=contentful_payload(piece), headers=contentful_headers('piece'))
	return response

def create_asset(image, title, caption):
	asset = {
		'title': str(title),
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
	process_asset(response)
	publish_asset(response)

	return asset_param(asset_id)

def process_asset(asset_id):
	return requests.put(process_asset_url % (space_id, asset_id, locale), headers=contentful_headers(''))

def publish_asset(asset_id):
	return requests.put(process_asset_url % (space_id, asset_id, locale), headers=contentful_headers(''))

def asset_param(asset_id):
	return {
		'sys': {
			'type': 'Link',
			'linkType': 'Asset',
			'id': asset_id
		}
	}

def create_briefings(briefing):
	response = requests.post(url, data=contentful_payload(briefing), headers=contentful_headers('briefing'))
	return response

def contentful_headers(content_type):
	return {
		'Authorization': 'Bearer ' + access_token,
		'Content-Type': 'application/vnd.contentful.management.v1+json',
		'X-Contentful-Content-Type': content_type
	}

def contentful_payload(resource):
	return json.dumps({'fields' : {key: {locale: resource[key]} for key in resource}})
