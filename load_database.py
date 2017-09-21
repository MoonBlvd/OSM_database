'''
Function:Load the data base and query
Date: 09/20/2017
Author: Yu (Brian) Yao

Input: 
    long: Longitude coordinate in float.
    lat:  Latitude coordinate in float.
    
Output:
    Top three nearest road. 
    
Database file:
    0 - 6:   id, highway, footway, name, tiger:cfcc, lanes, service
    7 - 12:  surface, oneway, amenity, maxspeed, crossing, lit
    13 - 16: lanes:backward, lanes:forward, source, parking
    17 - 19: sidewalk, turn:lanes:backward, turn:lanes:forward
    20 - 24: turn:lanes, destination:ref, barrier, tunnel, water
    25 - 26: hourse, railway
    27:      geometry
    *28:     distance 
    
'''
import sqlite3
MAX = 1E-4
MIN = 1E-5
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
        res = self.conn.execute("SELECT *,ST_Distance(osm.geometry, ST_POINT(?,?)) as dist\
                            FROM OSM_AA_POLYLINES_NEW as osm\
                            ORDER BY ST_Distance(osm.geometry, ST_POINT(?,?))",(long,lat,long,lat))
        data = res.fetchall()
        nearest_road = self.check_roads(data)
        
        res = self.conn.execute("SELECT AsText(?), NumPoints(?)",(nearest_road['geometry'], nearest_road['geometry']))
        data = res.fetchall()
        
        return nearest_road
    def check_roads(self, data):
        '''
        Given the reordered road data, find the nearest possible road
        '''
        flag = True
        i = 0
        while flag:
            road = self.load_dict(data[i])
            if i == 0 :
                nearest_road = road
            else:
                if road['dist'] - dist_prev < MIN:
                    # Both roads are close
                    if highway_prev == 'footway':
                        # if the closer road is a footway, it may be false
                        # check the next close road
                        if road['highway'] != 'footway':
                            nearest_road = road
                        continue
                elif road['dist'] - dist_prev > MAX:
                    # new road is far
                    return  nearest_road
            dist_prev = road['dist']
            highway_prev = road['highway']
            i += 1
        return nearest_road
            
    def load_dict(self, data):
        road = {}
        road['id'] = data[0]
        road['highway'] = data[1]
        road['footway'] = data[2]
        road['name'] = data[3]
        road['cfcc'] = data[4]
        road['lanes'] = data[5]
        road['service'] = data[6]
        road['surface'] = data[7]
        road['oneway']= data[8]
        road['amenity'] = data[9]
        if data[10] != None:
            road['maxspeed'] = float(data[10][0:2])*0.44704 # mph to m/s
        road['crossing'] = data[11]
        road['lit'] = data[12]
        road['lanes_back'] = data[13]
        road['lanes_forward'] = data[14]
        road['source'] = data[15]
        road['parking'] = data[16]
        road['sidewald'] = data[17]
        road['turn_back'] = data[18]
        road['turn_forward'] = data[19]
        road['turn'] = data[20]
        road['destination'] = data[21]
        road['barrier'] = data[22]
        road['tunnel'] = data[23]
        road['water'] = data[24]
        road['horse'] = data[25]
        road['railway'] = data[26]
        road['geometry'] = data[27]
        road['dist'] = data[28]
        return road
    
    
# SELECT id, source, wn.node_id,
# MIN(DISTANCE(osm.geometry, ST_POINT( -83.702175,42.297199))) as dist 
# FROM OSM_AA_POLYLINES_NEW AS osm,
# ways_nodes AS wn
# WHERE osm.id=wn.way_id

'''Find the number of points and the points coordinate of a road.'''
# SELECT AsText(geometry), NumPoints(geometry),X(PointN(geometry,2))
# FROM OSM_AA_POLYLINES_NEW as osm
# WHERE osm.id='4411729'

if __name__ == "__main__":
    db_name = "data/OSM_AA.osm.db"
    SQL = sql(db_name)
    
    long = -83.702175
    lat = 42.297199
    location = [long, lat]
    nearest_road = SQL.reorder_roads(location)
    print (nearest_road['highway'], nearest_road['maxspeed'])