# -*- coding: utf-8 -*-

import sys, json
import urllib, urllib2

from bottle import route, run, template, request, response, post
import ipfinder

import rdflib

host_ip = ipfinder.get_ip_address('eth0')
port = '7402'

def service(i_json, conf):
	o_json = None

	# Service routine -------------------------------------
	g = rdflib.Graph()

	for x in i_json['input']:
		s = rdflib.URIRef(x['subject'])
		p = rdflib.URIRef(x['property'])
		o = x['object']

		if type(o) == str or type(o) == unicode:
			if is_prefix('http://', o):
				o = rdflib.URIRef(o)
			else:
				o = rdflib.Literal(o)
		else:
			o = rdflib.Literal(o)

		g.add((s, p, o))

	o_json = {'output': g.serialize(format='turtle')}

	# /Service routine -------------------------------------

	return o_json

def is_prefix(prefix, string):
	if prefix == string[0:len(prefix)]:
		return True
	else:
		return False

def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if request.method != 'OPTIONS':
			# actual request; reply with the actual response
			return fn(*args, **kwargs)
		
	return _enable_cors

def send_postrequest(url, input_string):
	opener = urllib2.build_opener()
	request = urllib2.Request(url, data=input_string, headers={'Content-Type':'application/json'})
	return opener.open(request).read()
	
def set_conf(new_conf):
	# default configuration
	i_file = open('conf.json', 'r')
	sInput = i_file.read()
	i_file.close()
	conf = json.loads(sInput)

	# updated configuration
	conf.update(new_conf)

	return conf

@route(path='/service', method=['OPTIONS', 'POST'])
@enable_cors
def do_request():
	if not request.content_type.startswith('application/json'):
		return 'Content-type:application/json is required.'

	# input reading
	i_text = request.body.read()
	try:
		i_text = i_text.decode('utf-8')
	except:
		pass
	i_json = json.loads(i_text)

	# configuration setting
	try:
		conf = set_conf(i_json['conf'])
	except:
		conf = set_conf({})

	# request processing
	o_json = service(i_json, conf)
	o_text = json.dumps(o_json, indent=5, separators=(',', ': '), sort_keys=True)	

	return o_text

run(server='cherrypy', host=host_ip, port=port)