# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Daniel Aguayo <daniel@varpub.org>'
response.meta.description = 'Aplicación simple para compartir servidores virtuales personales.'
response.meta.keywords = 'virtual server,personal server, servidor personal,ip dinámica,dynamic ip'
response.meta.generator = 'Web2py Web Framework, Kdevelop, GNU Emacs, GNU/Linux'
response.meta.copyright = 'Copyleft 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def usermenu():
	response.menu.append(['Userv',None,URL(c='serv',f='index')])

usermenu()