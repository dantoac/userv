# -*- coding: utf-8 -*-

if 0:
	from gluon.dal import *
	from gluon.html import *
	from gluon import current
	db = DAL


def index():
	form = SQLFORM(db.userv)

	if form.process().accepted:
		redirect(URL(f='my'))
	elif form.errors:
		response = T('Corrige los errores señalados')
	return dict(form=form)

@auth.requires_login()
def my():
	data = db(db.userv.created_by == auth.user_id).select()
	#services = SQLTABLE(data)

	services = TABLE(THEAD(TR(
	TH(''),
	TH('Servicio'),
	TH('Link'),
	TH('Ip'),
	TH('Descripción'),
	)))

	for d in data:
		services.append(TR(
		TD(A('Renovar',callback=URL(f='update_ip',args=[d.id]),_class='button positive',target='current_ip')),
		TD(d.service),
		TD(A('link',_href=URL(c='go',f='index',vars=dict(servid=d.id))),
		TD(d.ip,_id='current_ip'),
		TD(d.desc),

		)))

	return dict(services=services)

@auth.requires_login()
def update_ip():
	if len(request.args)==0:
		return None

	userv_id = request.args(0)
	new_ip = request.client
	db.user[userv_id].ip = new_ip
	return new_ip
