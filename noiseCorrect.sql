CREATE OR REPLACE FUNCTION noiseCorrect () 
	RETURNS TABLE(gid integer,type_id smallint,type_road character varying(15),name character varying(30),geom geometry) AS
$$

DECLARE
    row record;
    point record;
    str text;
    dist float;
    temp float;
    num integer := 1;
    i integer;
    geoms geometry[] := '{}';
    newpoint geometry;
    points integer[];
    
BEGIN
	FOR row in EXECUTE 'select a.geom as geom1,a.gid as g1,b.geom as geom2,b.gid as g2 from noded_roads as a, noded_roads as b' LOOP
		--RAISE NOTICE 'DISTANCE ---- gid1:%, gid2:% %',row.g1,row.g2,st_distance(row.geom1,row.geom2);
		IF st_distance(row.geom1,row.geom2) > 0  AND st_distance(row.geom1,row.geom2) < 1 THEN
			
			IF st_collect(row.geom1,row.geom2) = ANY(geoms) THEN
				RAISE NOTICE 'gid1:%, gid2:% ',row.g1,row.g2;
				CONTINUE;
			ELSE	
				dist := 1;
				
				--PERFORM 'SELECT st_astext((st_dumppoints(row.geom1)).geom)';
				FOR point in EXECUTE 'select st_dumppoints($1) as dp' USING row.geom1 LOOP			
					--RAISE NOTICE 'H %',st_distance((point.dp).geom,row.geom2); 
					temp := st_distance((point.dp).geom,row.geom2);
					IF temp < dist THEN
						dist := temp;
						num := (point.dp).path[1];
						RAISE NOTICE 'dist %, num %',dist,num;
					END IF;
				END LOOP;
	
				IF dist=1 THEN
					CONTINUE;
				END IF;		

				--RAISE NOTICE 'dist %, num %',dist,num;

				newpoint := st_line_interpolate_point(row.geom2,st_line_locate_point(row.geom2,st_pointN(row.geom1,num)));
				EXECUTE 'SELECT st_numpoints(geom) from noded_roads where geom=$1' USING row.geom1 INTO str;
				RAISE NOTICE '% %',str,st_numpoints(st_astext(st_addpoint(row.geom1,newpoint,num-1)));
				IF newpoint is NOT NULL THEN	
					EXECUTE 'UPDATE noded_roads SET geom = st_addpoint($1,$2,$3-1) where geom =$1' USING row.geom1,newpoint,num;
					geoms := array_prepend(st_collect(row.geom2,row.geom1),geoms);
					GET DIAGNOSTICS i=ROW_COUNT;
					--PERFORM 'SELECT st_astext(geom) from noded_roads where geom=st_addpoint(row.geom1,newpoint,num-1)';
					RAISE NOTICE 'gid1:%, gid2:% , intersects:%, num:%,i:%',row.g1,row.g2,st_intersects(st_addpoint(row.geom1,newpoint,num-1),row.geom2), num, i;	
					--EXIT;
				END IF;	
			END IF;
		--ELSE 						
		--	--
		END IF;	
	
	END LOOP;
	
	RETURN QUERY SELECT * FROM noded_roads;
	--~ FOR row in EXECUTE 'select * from noded_roads' LOOP
		--~ INSERT INTO noded_roads_updated (gid,type_id,type_road,name,geom) VALUES (row.gid,row.type_id,row.type_road,row.name,row.geom);
	--~ END LOOP;
END;

$$


LANGUAGE 'plpgsql' VOLATILE STRICT;
