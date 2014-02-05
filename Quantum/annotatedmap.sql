--~ create table academic_area_extended as select distinct i.*, n.split_id as edge, md.min_distance as edge_dist
--~ from
	   --~ "Facilities" as i,network_extended as n, (
		   --~ select min(st_distance(ga.geom,gb.geom)) as min_distance
		   --~ from
			  --~ "Facilities" as ga, "network_extended" as gb
			  --~ group by ga.id
	--~ ) as md where st_distance(i.geom, n.geom)=md.min_distance;

--~ create table edget1 as select distinct on (e.split_id) e.split_id, e.geom, l.id, l.name as acad_building, l.geom as acad_geom
				--~ from network_extended as e 
					--~ LEFT JOIN "Academic_area" as l ON st_dwithin(e.geom,l.geom,10)
				--~ order by e.split_id,st_distance(e.geom,l.geom);
					

--~ create table edget2 as select distinct on (e.split_id) e.*,l.id as hostel_id, l.name as hostel_building, l.geom as hostel_geom
				--~ from edget1 as e 
					--~ LEFT JOIN "Hostel" as l ON st_dwithin(e.geom,l.geom,10)
				--~ order by e.split_id,st_distance(e.geom,l.geom);
--~ 
--~ create table edget3 as select distinct on (e.split_id) e.*,l.id as play_id, l.name as play_ground, l.geom as play_geom
				--~ from edget2 as e 
					--~ LEFT JOIN playgrounds as l ON st_dwithin(e.geom,l.geom,30)
				--~ order by e.split_id,st_distance(e.geom,l.geom);					
--~ 
--~ create table edget4 as select distinct on (e.split_id) e.*,l.id as fac_id, l.name as facility, l.geom as fac_geom
				--~ from edget3 as e 
					--~ LEFT JOIN "Facilities" as l ON st_dwithin(e.geom,l.geom,50)
				--~ order by e.split_id,st_distance(e.geom,l.geom);					
--~ 
--~ create table edget5 as select distinct on (e.split_id) e.*,l.gid as park_id, l.geom as park_geom
				--~ from edget4 as e 
					--~ LEFT JOIN "parks" as l ON st_dwithin(e.geom,l.geom,10)
				--~ order by e.split_id,st_distance(e.geom,l.geom);					
				
--~ create table edget6 as select distinct on (e.split_id) e.*,l.gid as fence_id, l.name as fence, l.geom as fence_geom
				--~ from edget4 as e 
					--~ LEFT JOIN "fences" as l ON st_dwithin(e.geom,l.geom,10)
				--~ order by e.split_id,st_distance(e.geom,l.geom);					

--Originally USED
-- create table edgelandmark as select foo.split_id as split_id,foo.lid as ref_id,foo.dist as dist from (select N.split_id as split_id ,L.id as lid,st_distance(N.geom,L.geom) as dist from network_extended as N JOIN salience as L ON st_dwithin(N.geom,L.geom,10)) foo;
	
create table edgelandmark as select row_number() OVER (ORDER BY foo.split_id)::integer as sno, foo.split_id as split_id,foo.lid as ref_id,foo.dist as dist 
from 
(select N.split_id as split_id ,L.id as lid,st_distance(N.geom,L.geom) as dist 
	from network_extended as N JOIN salience as L ON st_dwithin(N.geom,L.geom,10)) foo;	

alter table edgelandmark add column sno BIGSERIAL PRIMARY KEY;

insert into edgelandmark select foo.split_id as split_id,foo.lid as ref_id,foo.dist as dist from (select N.split_id as split_id ,L.id as lid,st_distance(N.geom,L.geom) as dist from network_extended as N JOIN salience as L ON st_dwithin(N.geom,L.geom,30) and not st_dwithin(N.geom,L.geom,10) and L.category='playground')  foo;	

insert into edgelandmark select foo.split_id as split_id,foo.lid as ref_id,foo.dist as dist from (select N.split_id as split_id ,L.id as lid,st_distance(N.geom,L.geom) as dist from network_extended as N JOIN salience as L ON st_dwithin(N.geom,L.geom,50) and not st_dwithin(N.geom,L.geom,10) and L.category='facility')  foo;	

alter table edgelandmark add column salience_geom geometry;

update edgelandmark set salience_geom=salience.geom from salience where salience.id=edgelandmark.ref_id;


-- for section wise landmarks

create table sectlandmark as select row_number() OVER (ORDER BY foo.dump_id)::integer as sno, foo.dump_id as dump_id,foo.lid as ref_id,foo.dist as dist 
from 
(select N.dump_id as dump_id ,L.id as lid,st_distance(N.geomline,L.geom) as dist 
	from network_dumppoints as N JOIN salience as L ON st_dwithin(N.geomline,L.geom,10)) foo;	

alter table sectlandmark add column sno BIGSERIAL PRIMARY KEY;

insert into sectlandmark select foo.dump_id as dump_id,foo.lid as ref_id,foo.dist as dist from (select N.dump_id as dump_id ,L.id as lid,st_distance(N.geomline,L.geom) as dist from network_dumppoints as N JOIN salience as L ON st_dwithin(N.geomline,L.geom,30) and not st_dwithin(N.geomline,L.geom,10) and L.category='playground')  foo;	

insert into sectlandmark select foo.dump_id as dump_id,foo.lid as ref_id,foo.dist as dist from (select N.dump_id as dump_id ,L.id as lid,st_distance(N.geomline,L.geom) as dist from network_dumppoints as N JOIN salience as L ON st_dwithin(N.geomline,L.geom,50) and not st_dwithin(N.geomline,L.geom,10) and L.category='facility')  foo;	

alter table sectlandmark add column salience_geom geometry;

update sectlandmark set salience_geom=salience.geom from salience where salience.id=sectlandmark.ref_id;

