# -*- coding: utf-8 -*-

if 0:
	from gluon.dal import *
	from gluon.html import *
	from gluon.globals import *
	session = Session
	request = Request
	response = Response
	db = DAL

@auth.requires_login()
def new():
	form = SQLFORM(db.userv,request.args(0))

	if form.process().accepted:
		redirect(URL(r=request,f='index'))
	elif form.errors:
		response.flash = T('Corrige los errores señalados')


	return dict(form=form)



@auth.requires_login()
def index():

	data = db(db.userv.created_by == auth.user_id).select()
	#services = SQLTABLE(data)

	services = TABLE(THEAD(TR(
	TH(''),

	TH('Servicio'),
	TH('Ip'),
	TH('Descripción'),
	TH('Link'),
	TH('Activo'),
	TH('Actualizado'),
	TH(''),
	)))

	for d in data:
		services.append(TR(
		TD(A(SPAN(_class='icon loop'),'IP',callback=URL(f='update_ip',args=[d.id]),_class='button positive',target='servip%s' % (d.id))),

		TD(d.service),
		TD(d.ip,_id='servip%s' % (d.id)),
		TD(d.desc),
		TD(A(SPAN(_class='icon home'),'link',_href=URL(c='go',f='index',vars=dict(servid=d.id)),_class='button'),
		TD(d.is_active),
		TD(d.modified_on),
		TD(A(SPAN(_class='icon pen'),_href=URL(f='new',args=d.id),_class='button')),

		)))


	return dict(services=services)

@auth.requires_login()
def update_ip():
	if len(request.args)==0:
		return None

	userv_id = request.args(0)
	new_ip = request.client
	db.userv[userv_id].update_record(ip=new_ip)
	#db.commit()
	return new_ip
