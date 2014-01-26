#!/usr/bin/env python

### You need to keep the top line!!

import web
import admin

### Connect a certain URL type to a certain class
urls = (
    '/', 'Index',
    '/admin/', 'Admin',
    '/admin', 'Admin',
    '/listed/(.*)', 'Listed',
    '/listed/(.*)/', 'Listed',
    '/search/', 'Search',
)

web.config.debug = True

### Use web.input() to manage different times of a VOD.
### Templates folder
render = web.template.render('templates')

### Classes
class Index:
        def GET(self):
                return "This is the home page."

class Admin:	
	
	form = web.form.Form(
        web.form.Textbox("y_id", description="Youtube ID"),
        web.form.Textbox("y_start_h", description="Youtube Game Start, hours"),
        web.form.Textbox("y_start_m", description="Youtube Game Start, minutes"),
        web.form.Textbox("y_start_s", description="Youtube Game Start, seconds"),
        web.form.Textbox("t_id", description="Twitch ID"),
        web.form.Textbox("t_start_h", description="Twitch Game Start, hours"),
        web.form.Textbox("t_start_m", description="Twitch Game Start, minutes"),
        web.form.Textbox("t_start_s", description="Twitch Game Start, seconds"),
        web.form.Button("submit")
)

        def GET(self):
		form = self.form()
                return render.register(form)

        def POST(self):
		data = web.input()
		y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s = data.y_id, data.y_start_h, data.y_start_m, data.y_start_s, data.t_id, data.t_start_h, data.t_start_m, data.t_start_s
                admin.new_sync(y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s)
		raise web.seeother('/')

class Listed:
        def GET(self, id):
                return render.vodtemp(id)

class Search:
        def GET(self):
                return 'This is a page where you can search for past matches.'

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
