import web
import db

def new_sync(y_id, y_start_h, y_start_m, y_start_s, t_id, t_start_h, t_start_m, t_start_s):
	db.db.insert('sync', youtube=y_id, twitch=t_id, y_start=int(y_start_h)*3600+int(y_start_m)*60+int(y_start_s), t_start=int(t_start_h)*3600+int(t_start_m)*60+int(t_start_s), chunks=0)

def chunkprep(y_id, number_c):
	for chunky in range(1,number_c):
		db.db.insert('sync', youtube=y_id, chunks=chunky)
