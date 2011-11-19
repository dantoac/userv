
def index():

	if request.get_vars.servid: servid = request.get_vars.servid
	else: return None

	return redirect('%(protocol)s://%(host)s:%(port)s/%(path)s' % dict(
					protocol = db.userv[servid].protocol or 'http',
					host = db.userv[servid].ip,
					port = db.userv[servid].port or 80,
					path = db.userv[servid].path
					))