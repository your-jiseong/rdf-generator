# -*- coding: utf-8 -*-

import sys, re, json
import rdflib

def service(i_json, conf):
	o_json = None

	# Service routine -------------------------------------
	g = rdflib.Graph()

	for x in i_json:
		s = rdflib.URIRef(x['subject'])
		p = rdflib.URIRef(x['property'])
		o = x['object']

		if type(o) == str or type(o) == unicode:
			if 'http://' in o:
				o = rdflib.URIRef(o)
			else:
				o = rdflib.Literal(o)
		else:
			o = rdflib.Literal(o)

		g.add((s, p, o))

	o_json = g.serialize(format='turtle')

	# /Service routine -------------------------------------

	return o_json

i_json = [{'subject': u'http://dbpedia.org/resource/park', 'property': 'http://dbpedia.org/property/birthYear', 'object': 'http://dbpedia.org/resource/kim'}]
conf = {}

print service(i_json, conf)