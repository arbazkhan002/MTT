CREATE OR REPLACE FUNCTION flip (deg float) 
	RETURNS FLOAT AS
$$

DECLARE
    temp float;
BEGIN
	temp := deg + 180;
	IF temp >= 360 THEN
		temp := temp-360;
	END IF;
	RETURN temp;

END
$$

LANGUAGE 'plpgsql' VOLATILE STRICT;



CREATE OR REPLACE FUNCTION discourse () 
	RETURNS VOID AS
$$

DECLARE
    row record;
    col record;
    deg float;
    prev_deg float;
    x float;
    orientation bool;
    geom geometry[] := '{}';
    ans text;
    points integer[];
    
BEGIN
	
	prev_deg:=-360;
	
	

	FOR row in EXECUTE 'SELECT * FROM network_extended JOIN (SELECT * FROM shortest_path($1, 260, 261, false, false)) AS route ON network_extended.split_id = route.edge_id' USING 'SELECT split_id AS id, start_id::int4 AS source, end_id::int4 AS target, length::float8 AS cost FROM network_extended' LOOP
		--RAISE NOTICE '%',row.split_id;
		

		
		-- If vertex in route is start point, store the end angle for future use
		IF row.vertex_id = row.start_id THEN 		
			orientation := TRUE; --Going in the same direction as the edge
			
			IF prev_deg=-360 THEN
				prev_deg := row.end_angle;
				CONTINUE;
			END IF;
			
			deg := row.start_angle;
			x := deg - prev_deg;	
			prev_deg := row.end_angle;
			
		-- else store the start angle	
		ELSE
			orientation := FALSE; --Going in the opp direction as the edge (endid to startid)
			
			IF prev_deg=-360 THEN
				prev_deg := flip(row.start_angle);
				CONTINUE;
			END IF;
			
			deg := flip(row.end_angle);
			x := deg - prev_deg;
			prev_deg := flip(row.start_angle);
		END IF;		
		
		--~ RAISE NOTICE 'ID:% ORIENTATION % StartConnections % and ANGLE %',row.vertex_id,orientation,row.start_connections,x;
		
		IF (orientation=TRUE and row.start_connections=TRUE) or  (orientation=FALSE and row.end_connections=TRUE) THEN 
			RAISE NOTICE 'On %',row.vertex_id;
			CASE 		
				WHEN x BETWEEN 45 AND 135 THEN
					FOR col in EXECUTE 'SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=' || row.split_id || ' ;' LOOP 
						RAISE NOTICE 'fence:% building:%',col.fence,col.facility;
					END LOOP;	
					RAISE NOTICE 'GO RIGHT';

				WHEN x BETWEEN 225 AND 315 THEN
					FOR col in EXECUTE 'SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=' || row.split_id || ' ;' LOOP 
						RAISE NOTICE 'fence:% building:%',col.fence,col.facility;
					END LOOP;				
					RAISE NOTICE 'GO LEFT';	

				WHEN x BETWEEN -135 AND -45 THEN
					FOR col in EXECUTE 'SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=' || row.split_id || ' ;' LOOP 
						RAISE NOTICE 'fence:% building:%',col.fence,col.facility;
					END LOOP;	
					RAISE NOTICE 'GO LEFT';

				WHEN x BETWEEN -315 AND -225 THEN
					FOR col in EXECUTE 'SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=' || row.split_id || ' ;' LOOP 
						RAISE NOTICE 'fence:% building:%',col.fence,col.facility;
					END LOOP;	
					RAISE NOTICE 'GO RIGHT';	
					
				ELSE
					FOR col in EXECUTE 'SELECT n.split_id,acad_building,facility,fence FROM network_extended as n,edget6  WHERE edget6.split_id=n.split_id AND n.split_id=' || row.split_id || ' ;' LOOP 
						RAISE NOTICE 'fence:% building:%',col.fence,col.facility;
					END LOOP;	
					RAISE NOTICE 'GO STRAIGHT';			 	
			END CASE;
		END IF;	
	END LOOP;
	
		
END

$$

LANGUAGE 'plpgsql' VOLATILE STRICT;
	
