#OSM Road Tags Notes
Wednesday, 20. September 2017 07:21PM 

###highway
---
#### highway=motorway
* Highest-performance roads with control of access
* In US, it's a freeway, turnpike, or interstate.

#### highway=trunk
* High performance or high importance roads that don't meet the requirement for ```motorway```.
* Usually with a central barrier 
* Surface expressway: A relatively high-speed divided road (at least 40 MPH with a barrier or median separating each direction of traffic), with a limited amount of intersections and driveways; or a major intercity highway. This includes many U.S. Highways (that do not parallel an Interstate) and some state highways.

#### highway=primary
* A major highway linking large towns, in developed countries normally with 2 lanes.
* No central barriers.
* Can be either both ways or one way.
* **U.S. Highways** are mostly primary. Some **State Roads** or **State Routes** may also be primary, if they have a significant role in linking two major cities.

#### highway=secondary
* A secondary way forms a link in the national route network. 
* Normally has 2 lanes and either both way or one way. 
* Separated by a central line on the road. 

#### highway=tertiary
* Roads connecting smaller settlements, and **within large** settlements for roads connecting local centres
* **Quieter** linking roads are ```highway=unclassified```
* **Busier** through routes are ```highway=secondary```

#### highway=unclassified
* Minor public roads typically at the lowest level of the interconnecting grid network.
* Usable by motor cars.

#### highway=residential
*  Streets or roads generally used for local traffic **within** settlement.

#### highway=service
* For access to a fuel station.
* Main ways on parking lot .
* Driveway to a recidence.
* A narrow road, alley or path between properties.

#### highway=xxx_link
* The link roads (sliproads/ramps) leading to/from a **xxx** from/to a **xxx** or lower class. 
* Normally with the same restrictions of a **xxx** class. 
---
### footway

#### footway=sidewalk
* A sidewalk alongside a street, separately mapped with ```highway=footway```.

#### footway=crossing
* A pedestrian crossing, usually connecting two sidewalks.

---
### name
* The ```name``` key equals to either ```NULL``` or the road name.

---
### lanes
* The ```lanes``` key equals to either the number of lanes or ```NULL```
* There are sub keys:```lanes_backward``` and ```lanes_forward```, the values indicate the numbers of backward and forward lanes.

---
### surface
#### surface=paved
* A highway feature is predominantly paved along its length; i.e., it is covered with paving stones, concrete or bitumen. 

#### surface=asphalt
* It does not mean that the road surface is only asphalt. Most such roads are tagged as less clear surface=paved. 

#### surface=concrete
* Cement based Concrete, forming a large, continuous surface, typically cast in place. 

#### surface=unpaved
* A highway feature is predominantly unsealed along its length; i.e., it has a loose covering ranging from compacted stone chippings to earth.

#### surface=dirt
* It is prone to erosion and therefore often uneven. Gravel is sometimes mistakenly called dirt. Some ```surface=compacted``` roads are sometimes called dirt too.

#### surface=compacted
* A mixture of larger (e.g., gravel) and smaller (e.g., sand) parts, compacted (e.g., with a roller), so the surface is more stable than loose gravel.

*Other values of surface can be seen from the wiki.*

---
### oneway
* The ```oneway``` key equals to ```yes``` or ```no``` or ```NULL```.

---
### maxspeed
* The ```maxspeed``` key equals to either the maximum speed in ```mph``` or ```NULL```.

---
### crossing
#### crossing=traffic_signals
* When the crossing-traffic (pedestrian, bicycles) have their own traffic lights. 
* It has sub keys ```traffic_signals:sound=yes/no``` and ```traffic_signals:vibration=yes/no```.
#### crossing=uncontrolled
* A generic crossing with no traffic-signals of any type, just road markings. e.g. Zebra-crossings.

#### crossing=island
* A crossing with a small traffic-island for pedestrians in the middle of the road. 

#### crossing=unmarked
* A crossing without road markings or traffic lights.

---
### lit

* Indicates the presence of lighting.
#### lit=24/7
* Both night and day.
#### lit=yes
* At night.
#### lit=automatic
* When someone enters the way the lights are turned on.
#### lit=no
* There are no lights installed.
#### lit=operating times
* For example, ```05:00-07:45``

---
### sidewalk
* A sidewalk may be separated from the carriageway by only a curb, by a road verge or alternatively may be at some distance from the road (but still associated with it). It also may be separated from the road by some form of barrier, for example bushes or a line of trees. A road may have a sidewalk on only one side of the carriageway, or both side or have no sidewalks. 
* ```sidewalk=right/left/no/NULL```

---
### turn_lanes
* The ```turn_lanes``` key is used to specify the indicated direction in which a way or a lane will lead```left|through;right```











