CREATE OR REPLACE FUNCTION noiseCorrect () 
	RETURNS geometry[] AS
$$

DECLARE
    row record;
    point record;
    dist float;
    temp float;
    num integer := 1;
    i integer;
    geoms geometry[] := '{}';
    res geometry[];
    points integer[];
    
BEGIN

	FOR row in EXECUTE 'select a.geom as geom1,a.gid as g1,b.geom as geom2,b.gid as g2 from noded_roads as a, noded_roads as b' LOOP
		--RAISE NOTICE '%',st_distance(row.geom1,row.geom2);
		IF st_distance(row.geom1,row.geom2) > 0  AND st_distance(row.geom1,row.geom2) < 1 THEN
				dist := 1;
				FOR point in EXECUTE 'select st_dumppoints($1) as dp' USING row.geom1 LOOP
					--RAISE NOTICE 'H';
					temp := st_distance((point.dp).geom,row.geom2);
					IF temp <= dist THEN
						dist := temp;
						num := (point.dp).path[1];
					END IF;
				END LOOP;	
				UPDATE noded_roads SET geom = st_addpoint(row.geom1,st_pointN(row.geom1,num),num-1) where geom = row.geom1;
				RAISE NOTICE 'gid1:%, gid2:%',row.g1,row.g2;	
				
		--ELSE 		
		--	--
		END IF;	
		
	END LOOP;

END;

$$

LANGUAGE 'plpgsql' VOLATILE STRICT;
