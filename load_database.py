import sqlite3

# connect to database
db_name = "09182017.osm.db"
conn = sqlite3.connect(db_name)
conn.enable_load_extension(True)
conn.load_extension("mod_spatialite")

res = conn.execute("SELECT * FROM spatialIndex")

#res = conn.execute("SELECT")
print (res.fetchall())
#print res