import web

db = web.database(dbn="mysql", user="", pw="", db="", host="", port=3306)

def new_sync(y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s):
	db.insert('sync', youtube=y_id, twitch=t_id, y_start=int(y_start_h)*3600+int(y_start_m)*60+int(y_start_s), t_start=int(t_start_h)*3600+int(t_start_m)*60+int(t_start_s))
