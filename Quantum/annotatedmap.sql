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
				
create table edget6 as select distinct on (e.split_id) e.*,l.gid as fence_id, l.name as fence, l.geom as fence_geom
				from edget4 as e 
					LEFT JOIN "fences" as l ON st_dwithin(e.geom,l.geom,10)
				order by e.split_id,st_distance(e.geom,l.geom);					