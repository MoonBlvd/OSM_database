## Data sets
* OpenStreetMap (osm)
* MDOT Traffic Volumes (AADT)
## Rough match
A **Spatial Index** of a geometry is described by a minimum bounding rectangle of the geometry, i.e. (xmin, xmax, ymin, ymax).  The spatial query finds the ROWID of geometries in **f_table** whose bounding rectangles have intersections (no matter how much they are intersected) with bounding rectangles of the **search_frame**.

Use **Spatial Index** to match osm road segments with AADT road segments (both are **Linestring** geometry). Ignore the osm roads with **highway=NULL**.
 
	SELECT *
	FROM michigan_road_osm as osm,
	     "2016_Traffic_Volumes" as AADT2016
	WHERE osm.ROWID IN(
		SELECT ROWID
		FROM SpatialIndex
		WHERE f_table_name = 'michigan_road_osm' AND f_geometry_column = 'GEOMETRY' AND
		      search_frame = ST_Envelope(AADT2016.geometry)
	) OR AADT2016.ROWID IN(
		SELECT ROWID
		FROM SpatialIndex
		WHERE f_table_name = '2016_Traffic_Volumes' AND f_geometry_column = 'GEOMETRY' AND
		      search_frame = ST_Envelope(osm.geometry)
	)

Note that each osm road might match with multiple AADT roads and vice versa. Because these two data sets divide road to segments in different ways, sometimes the osm segments are larger and contain several AADT segments, and sometimes the AADT segments are larger and contain multiple osm segments.
h

Find the road segments that are are longitudinal or lateral, the ```1.48352986``` and ```0.08726646``` are thresholds correspond to ```85 deg``` and ```5 deg```. Then extend each of these segments by adding two new points to the linestring geometry:

	SELECT Geometry, ST_AddPoint(ST_AddPoint(Geometry, ST_Point(ST_minX(Geometry)-0.00045,ST_minY(Geometry)-0.00045)),ST_Point(ST_maxX(Geometry)-0.00045,ST_maxY(Geometry)+0.00045)) as extended_geom
	FROM
	(
		SELECT abs(ST_maxX(Geometry) - ST_minX(Geometry)) as lon_diff, abs(ST_maxY(Geometry) - ST_minY(Geometry)) as lat_diff, atan(abs(ST_maxY(Geometry) - ST_minY(Geometry))/abs(ST_maxX(Geometry) - ST_minX(Geometry))) as angle, StartPoint(Geometry) as end1, EndPoint(Geometry) as end2,Geometry, ST_Envelope(Geometry)
		FROM ("2016_Traffic_Volumes")
		WHERE  angle > 1.48352986 or angle < 0.08726646
	)
	
	
	
Create a temporal table to store extended geometry info in indices

	CREATE TABLE tmp_extend_lines
	AS
	SELECT ID,Geometry, 
		ST_AddPoint(ST_AddPoint(Geometry, ST_Point(ST_minX(Geometry)-0.00045,ST_minY(Geometry)-0.00045)),ST_Point(ST_maxX(Geometry)+0.00045,ST_maxY(Geometry)+0.00045)) as extended_geom
	FROM
	(
	SELECT ROWID as id,
		abs(ST_maxX(Geometry) - ST_minX(Geometry)) as lon_diff, 
		abs(ST_maxY(Geometry) - ST_minY(Geometry)) as lat_diff,
		atan(abs(ST_maxY(Geometry) - ST_minY(Geometry))/abs(ST_maxX(Geometry) - ST_minX(Geometry))) as angle,
		StartPoint(Geometry) as end1, EndPoint(Geometry) as end2,Geometry, ST_Envelope(Geometry)
	FROM michigan_road
	WHERE  angle > 1.48352986 or angle < 0.08726646
	)
	
	
Update the Geometries of the longitudinal and lateral road segments of the AADT database

	UPDATE "2016_Traffic_Volumes"
	SET Geometry=(
		SELECT extended_geom
		FROM tmp_extend_lines as tmp
		WHERE tmp.ID == "2016_Traffic_Volumes".id)	
	
 
Create the rough match table:

	CREATE TABLE rough_match
	AS
	SELECT *,osm.Geometry as osm_geom, AADT.geom_backup as AADT_geom,
		atan(abs(ST_maxY(osm.Geometry) - ST_minY(osm.Geometry))/abs(ST_maxX(osm.Geometry) - ST_minX(osm.Geometry))) as osm_angle,
		atan(abs(ST_maxY(AADT.geom_backup) - ST_minY(AADT.geom_backup))/abs(ST_maxX(AADT.geom_backup) - ST_minX(AADT.geom_backup))) as AADT_angle
	FROM michigan_road as osm,
		"2016_Traffic_Volumes" as AADT
	WHERE osm.ROWID IN(
			SELECT ROWID
			FROM SpatialIndex
			WHERE f_table_name = 'michigan_road' AND f_geometry_column = 'Geometry' AND
			      search_frame = ST_Envelope(AADT.Geometry)
		) AND ST_Distance(osm_geom, AADT_geom) < 0.00027


#### ISSUES

* SInce the two data sets are independently collected, there are cases that the bounding rectangles of correlated road segments **have no intersection** (e.g. two segments are parallel with an offset). In these cases we may **NOT** be able to match them.

* Can we use **County Spaial Indices** and run for loop county by county? Not sure, sometimes a road might be separated by county boundaries so that those roads are not matched with any counties.
**But** the number of roads missed by this method can be much less than using the **Road Spatial Indices**.

* 

## Accurate match

After the road segments are roughly matched,  

	SELECT id, name, highway, StartPoint(osm.geometry) as end1, EndPoint(osm.geometry) as end2, StartPoint(AADT2016.geometry) as end3, EndPoint(AADT2016.geometry) as end4, osm.geometry as osm_geom, AADT2016.geometry as AADT_geom ,ST_Distance(AADT2016.geometry,osm.geometry) as distance
	
	
FInd the angles of osm road segments and AADT road segments after the rough matching.
	
	SELECT *,
	atan(abs(ST_maxY(osm.Geometry) - ST_minY(osm.Geometry))/abs(ST_maxX(osm.Geometry) - ST_minX(osm.Geometry))) as osm_angle,
	atan(abs(ST_maxY(AADT.Geometry) - ST_minY(AADT.Geometry))/abs(ST_maxX(AADT.Geometry) - ST_minX(AADT.Geometry))) as AADT_angle
	FROM michigan_road_osm as osm,
	     "2016_Traffic_Volumes" as AADT
	WHERE osm.ROWID IN(
		SELECT ROWID
		FROM SpatialIndex
		WHERE f_table_name = 'michigan_road_osm' AND f_geometry_column = 'GEOMETRY' AND
		      search_frame = ST_Envelope(AADT.geometry)
	)
	
	

	
	CREATE TABLE new_match
	AS
	SELECT *, min(ST_Distance(osm_geom, AADT_geom)) as distance
	FROM
	(
	SELECT *
	FROM
	(
	SELECT *,osm.Geometry as osm_geom, AADT.Geometry as AADT_geom,
		atan(abs(ST_maxY(osm.Geometry) - ST_minY(osm.Geometry))/abs(ST_maxX(osm.Geometry) - ST_minX(osm.Geometry))) as osm_angle,
		atan(abs(ST_maxY(AADT.Geometry) - ST_minY(AADT.Geometry))/abs(ST_maxX(AADT.Geometry) - ST_minX(AADT.Geometry))) as AADT_angle
		FROM michigan_road_osm as osm,
		     "2016_Traffic_Volumes" as AADT
		WHERE osm.ROWID IN(
			SELECT ROWID
			FROM SpatialIndex
			WHERE f_table_name = 'michigan_road_osm' AND f_geometry_column = 'GEOMETRY' AND
			      search_frame = ST_Envelope(AADT.geometry)
		) AND highway is not NULL AND ST_Distance(osm_geom, AADT_geom) < 0.00045
	)
	WHERE abs(osm_angle - AADT_angle) < 0.26
	) 
	GROUP BY id



	SELECT *
	FROM 
	(
		SELECT *, min(distance+distance_1+distance_2) as min_total_distance
		FROM rough_match
		GROUP BY id
	)
	where
