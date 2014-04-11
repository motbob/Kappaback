#!/usr/bin/env python

### You need to keep the top line!!

import web
import admin
import datetime
import db

### Connect a certain URL type to a certain class
urls = (
    '/', 'Index',
    '/admin/', 'Admin',
    '/admin', 'Admin',
    '/listed/(.*)', 'Listed',
    '/listed/(.*)/', 'Listed',
    '/search/', 'Search',
    '/chat/(.*)/', 'Chat',
    '/chartest/', 'Chartest',
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

	### The web form that shows up when you open the Admin page.
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
		### Display the form
		form = self.form()
                return render.register(form)

        def POST(self):
		from urllib2 import urlopen
                import json
		from xml.dom.minidom import parseString
		from random import randint
		### Create a place for the submitted web data to go
		data = web.input()
		y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s = data.y_id, data.y_start_h, data.y_start_m, data.y_start_s, data.t_id, data.t_start_h, data.t_start_m, data.t_start_s
		### Send the submitted data to a database
                admin.new_sync(y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s)
		### Fetch the video creation date/time and the channel name of the relevant Twitch video
                response = urlopen('https://api.twitch.tv/kraken/videos/a'+t_id)
		jsonRaw = response.read()
		t_data = json.loads(jsonRaw)
		creation = t_data["recorded_at"]
		channel = t_data["channel"]["name"]
		### Format the creation date/time
		begin = datetime.datetime.strptime(creation, "%Y-%m-%dT%H:%M:%SZ")
		### Fetch the video duration of the youtube video and use that to determine how many 5 minute chunks of chat we need
                url = 'https://gdata.youtube.com/feeds/api/videos/' + y_id + '?v=2'
                xml_stuff = urlopen(url).read()
                strings = parseString(xml_stuff)
                magic = strings.getElementsByTagName('yt:duration')[0]
                seconds_string = magic.attributes['seconds']
                seconds = int(seconds_string.value)
                number_c = seconds/300+1
		### Create database rows for each chunk of chat. One row was already created during admin.new_sync.
		admin.chunkprep(y_id, number_c)
		### Determine the date/time that the youtube VOD was created
		t_start_secs = int(t_start_h)*3600+int(t_start_m)*60+int(t_start_s)
		y_start_secs = int(y_start_h)*3600+int(y_start_m)*60+int(y_start_s)
		t_start2, y_start2 = datetime.timedelta(seconds=t_start_secs), datetime.timedelta(seconds=y_start_secs)
		youtube_start_date = begin + t_start2 - y_start2
		### Create a table from which random chat colors can be drawn
                chat_color = ["#FF0000", "#0000FF", "#008000", "#B22222", "#FF7F50", "#9ACD32", "#FF4500", "#2E8B57", "#DAA520", "#D2691E", "#5F9EA0", "#1E90FF", "#FF69B4", "#8A2BE2", "#00FF7F"]
                ### Create a dictionary that will allow us to render Twitch emotes, and write a function that will let us use that dictionary.
                reps = {'AsianGlow':'<span class=\\\"emo-1 emoticon\\\"></span>','BibleThump':'<span class=\\\"emo-2 emoticon\\\"></span>','DAESuppy':'<span class=\\\"emo-3 emoticon\\\"></span>','DansGame':'<span class=\\\"emo-4 emoticon\\\"></span>','DogFace':'<span class=\\\"emo-5 emoticon\\\"></span>','EvilFetus':'<span class=\\\"emo-6 emoticon\\\"></span>','FailFish':'<span class=\\\"emo-7 emoticon\\\"></span>','FrankerZ':'<span class=\\\"emo-8 emoticon\\\"></span>','Kappa':'<span class=\\\"emo-9 emoticon\\\"></span>','Keepo':'<span class=\\\"emo-10 emoticon\\\"></span>','KevinTurtle':'<span class=\\\"emo-11 emoticon\\\"></span>','Kippa':'<span class=\\\"emo-12 emoticon\\\"></span>','Kreygasm':'<span class=\\\"emo-13 emoticon\\\"></span>','MrDestructoid':'<span class=\\\"emo-14 emoticon\\\"></span>','OMGScoots':'<span class=\\\"emo-15 emoticon\\\"></span>','OneHand':'<span class=\\\"emo-16 emoticon\\\"></span>','PJSalt':'<span class=\\\"emo-17 emoticon\\\"></span>','PogChamp':'<span class=\\\"emo-18 emoticon\\\"></span>','RalpherZ':'<span class=\\\"emo-19 emoticon\\\"></span>','SMOrc':'<span class=\\\"emo-20 emoticon\\\"></span>','SwiftRage':'<span class=\\\"emo-21 emoticon\\\"></span>','TehFunrun':'<span class=\\\"emo-22 emoticon\\\"></span>','TheThing':'<span class=\\\"emo-23 emoticon\\\"></span>','TriHard':'<span class=\\\"emo-24 emoticon\\\"></span>','WinWaker':'<span class=\\\"emo-25 emoticon\\\"></span>'}
		def replace_all(text, dic):
                        for i, j in dic.iteritems():
                                text = text.replace(i, j)
                        return text
                ### Create the chat chunks
                for chunk in range(0, number_c):
                        ### Create an sql query that selected all the chat from the relevant channel in 5 minute chunks
                        entries_iter = db.db.query("select * from main where (time between \'" + str(youtube_start_date + datetime.timedelta(seconds=300*chunk)) + "\' and \'" + str(youtube_start_date + datetime.timedelta(seconds=300*(chunk+1))) + "\') and channel = \'" + channel + "\'")
                        entries = list(entries_iter)
                        length_l = len(entries)
                        ### Construct the object that we're going to put on the webpage (long line of chat data)
                        x = "{"
                        j_time = datetime.timedelta(seconds=100000000)
			for div in range(0, length_l):
                                if j_time != datetime.timedelta.total_seconds(entries[div].time - youtube_start_date):
                                        if div != 0:
                                                x += "\", "
                                        x += "\""
                                        j_time = datetime.timedelta.total_seconds(entries[div].time - youtube_start_date)
                                        x += str(int(datetime.timedelta.total_seconds(entries[div].time - youtube_start_date)))
                                        x += "\": \"<div class=\\\"chat_msg\\\"><b><font color=\\\"" + chat_color[randint(0,14)] + "\\\">"
                                        x += entries[div].name
                                        x += "</font></b>: "
                                        r = json.dumps(entries[div].message)
                                        t = replace_all(r, reps)
                                        x += t
                                        x += "</div>"
                                else:
                                        x += "<div class=\\\"chat_msg\\\"><b><font color=\\\"" + chat_color[randint(0,14)] + "\\\">"
                                        x += entries[div].name
                                        x += "</font></b>: "
                                        r = json.dumps(entries[div].message)
                                        t = replace_all(r, reps)
                                        x += t
                                        x += "</div>"
                        x += "\"}"
                        db.db.update('sync', where="chunks = " + str(chunk) + " AND youtube = " + y_id, chat = x)
                raise web.seeother('/')

class Listed:
        def GET(self, id):
                return render.vodtemp(id)

class Chat:
	def GET(self, id):
		yt = id[0:11]
		chnk = id[-2:]
		if int(chnk[:1]) == 0:
			chnk = chnk[-1:]
		thing = db.db.select('sync', what='chat', where='chunks = \'' + str(chnk) + '\' AND youtube = \'' + str(yt) + '\'')
		return thing[0].chat

class Chartest:
	def GET(self):
                return "I will lie here until needed"

class Search:
        def GET(self):
		return "What"

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
