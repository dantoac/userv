# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

if 0:
	from gluon.html import *

def index():
	'''
	Busca por get_vars entre los servicios registrados en el sistema.
	Si el servicio existe entonces redirige directamente al controlador
	go.py, sino	presenta una lista de servicios con nombre similar.

	Ejemplo:
		http://ejemplo.com?go=NOMBRE_SERVICIO

	Si NOMBRE_SERVICIO existe en la DB entonces redirigirá hacia el
	respectivo protocolo,ip,puerto y ruta registrada.
	Si NOMBRE_SERVICIO no existe en la DB entonces mostrará una lista
	de servicios con nombre similar (db.userv.service.contains(NOMBRE_SERVICIO))
	'''

	form = FORM(
	LABEL('Buscar'),
	INPUT(_type='text',_name='go'),
	INPUT(_type='submit'),
	_method='GET',_action=URL(f='index')
	)

	resultados = TAG.div(_id='resultados')

	if not request.get_vars.go:
		return dict(form=form,resultados=resultados)
	go = request.get_vars.go.strip().lower()

	data = db((db.userv.slug == go) | (db.userv.service == go)).select()


	if len(data)==0:
		data = db(
		(db.userv.slug.contains(go)) | (db.userv.service.contains(go)) | (db.userv.desc.contains(go))
		).select()

		if len(data)>0:
			for d in data:
				resultados.append(TAG.div(A(TAG.strong(d.service),_href=URL(f='index',vars=dict(go=d.slug))),TAG.br(EM(d.desc)),_class='resultado'))

			resultados = CAT(H3('Quiso decir...'),resultados)
		else:
			resultados = P('No hubo resultados')
	else:

		#redirect(URL(c='go',vars=dict(servid = data.as_list()[0]['id'])))
		raise HTTP(301,Location=URL(c='go',vars=dict(servid = data.as_list()[0]['id'])))
		#for d in data:
		#	resultados.append(LI(A(d.service,_href=URL(f='index',vars=dict(go=d.slug)))))

	return dict(form=form,resultados=resultados)

    #return dict(message=T('Hello World'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
