# -*- coding: utf-8 -*-

if 0:
	from gluon.dal import *
	from gluon.html import *
	from gluon.globals import *
	session = Session
	request = Request
	response = Response
	db = DAL

def index():

	if request.get_vars.servid: servid = request.get_vars.servid
	else: return None

	if db.userv[servid].is_active:
		return redirect('%(protocol)s://%(host)s:%(port)s/%(path)s' % dict(
					protocol = db.userv[servid].protocol or 'http',
					host = db.userv[servid].ip,
					port = db.userv[servid].port or 80,
					path = db.userv[servid].path
					))
	else:
		session.flash = 'El host está explícitamente desactivado.'
		return redirect(URL('default','index.html'))