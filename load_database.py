'''
Function:Load the data base and query
Date: 09/20/2017
Author: Yu (Brian) Yao

Input: 
    long: Longitude coordinate in float.
    lat:  Latitude coordinate in float.
    
Output:
    Top three nearest road. 
'''
import sqlite3

class sql():
    def __init__(self, db_name):
        # connect to database
        self.conn = sqlite3.connect(db_name)
        self.conn.enable_load_extension(True)
        self.conn.load_extension("mod_spatialite")
        
        self.num_roads = 5
        
    def reorder_roads(self, location):
        '''
        Reorder road data by distance 
        '''
        long = location[0]
        lat = location[1]
        '''Find the nearest road''' 
        # data = conn.execute("SELECT *, MIN(DISTANCE(geometry, ST_POINT( -83.702175,42.297199))) as dist \
        #                     FROM OSM_AA_POLYLINES_NEW as osm \
        #                     JOIN ways_tags as wt USING (id)")

        '''Order the roads by distances to the point.'''
        res = conn.execute("SELECT *,ST_Distance(osm.geometry, ST_POINT(?,?)) as dist\
                            FROM OSM_AA_POLYLINES as osm\
                            ORDER BY ST_Distance(osm.geometry, ST_POINT(?,?))",(long,lat,long,lat))
        data = res.fetchall()
        self.check_roads(data)
        
    def check_roads(self, data):
        '''
        Given the reordered road data, find the nearest possible road
        '''
        nearest_road_0 = data[0][0:18]
        dist_0 = data[0][19]
        
        print (nearest_road_0)
        print (dist_0)
        
if __name__ == "__main__":
    db_name = "data/OSM_AA_new.osm.db"
    SQL = sql(db_name)
    
    long = -83.702175
    lat = 42.297199
    location = [long, lat]
    SQL.reorder_roads(location)
    
