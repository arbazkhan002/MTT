CREATE OR REPLACE FUNCTION splitN (line geometry,  xs geometry[]) 
	RETURNS geometry[] AS
$$

DECLARE
    row record;
    num integer := 1;
    i integer;
    geom geometry[] := '{}';
    res geometry[];
    points integer[];
    
BEGIN
	

	--~ RAISE NOTICE 'iTS in (LINE:% POINT:% \n %)',st_astext(line),st_astext(xs[1]),st_intersects(line,xs[1]);
	--~ PERFORM pg_sleep(5);
	
	DELETE FROM dummy1;
	--~ Split the line only by the first point, rest splits would be taken care of in the recursion
	INSERT INTO dummy1 (id, g1,g2) VALUES (num, line, xs[num]);
	
	WHILE st_intersects(line,xs[num])=FALSE LOOP
		num := num+1;
		--~ PERFORM pg_sleep(1);
		--~ RAISE NOTICE 'DoESNT INTERSECT. \n NOW iTS in (LINE:% POINT:% \n %)',st_astext(line),st_astext(xs[num]),st_intersects(line,xs[num]);
		DELETE FROM dummy1;
		--~ Split the line only by the first point, rest splits would be taken care of in the recursion
		INSERT INTO dummy1 (id, g1,g2) VALUES (num, line, xs[num]);
		--~ PERFORM  pg_sleep(1);
		--~ select * from d;

	END LOOP;

	num := num+1;
		
	FOR row in EXECUTE 'select  ST_GeomFromEWKB((ST_Dump(st_split(g1,g2))).geom) as sp from dummy1 where st_intersects(g1,g2)=TRUE' LOOP
		
		--~ Next split would be from the 2nd point in the list

		--~ RAISE NOTICE 'i am srsly in (%)',st_astext(row.sp);
						
		IF array_upper(xs,1)<=1 then	
			--~ RAISE NOTICE ' EXIT';
			geom := array_prepend(row.sp,geom);
			CONTINUE;	
		
		ELSE
			--~ PERFORM pg_sleep(1);	
			res := splitN(row.sp, xs[num:array_upper(xs,1)]);		
		END IF;	
		
		--~ RAISE NOTICE 'DIDNT EXIT %',array_upper(res,1);
		--~ If the line dint get split by any other point, it needs to be included
		IF array_upper(res,1) is NULL THEN
			geom := array_prepend(row.sp,geom);			
			CONTINUE;
		END IF;		
		--~ 
		--~ Include all the splits of the line
		FOR i in 1..array_upper(res,1) LOOP
			geom := array_prepend(res[i],geom);
		END LOOP;
		--~ 
	END LOOP;		
	RETURN geom;	
	

END;
$$

LANGUAGE 'plpgsql' VOLATILE STRICT;

--~ 
CREATE OR REPLACE FUNCTION splitter()
	RETURNS VOID AS
$$

DECLARE
    row record;
    row2 record;
	init geometry[] := '{}';
	res geometry[];
	line geometry;
    i integer;
    j integer;
	

BEGIN
	DELETE FROM dummy;
	FOR row2 in EXECUTE 'select distinct geom from split_points2' LOOP
		init := array_append(init,row2.geom);
		--~ RAISE NOTICE ' POINTS geom :  %', st_astext(row2.geom);				
	END LOOP;
--~ 
	--~ FOR row2 in EXECUTE 'select st_geomfromtext(''POINT(5 5)'') as geom' LOOP
		--~ init := array_append(init,row2.geom);				
	--~ END LOOP;
	--~ 
	--~ FOR row2 in EXECUTE 'select st_geomfromtext(''POINT(3 3)'') as geom' LOOP
		--~ init := array_append(init,row2.geom);				
	--~ END LOOP;
--~ 
	--~ FOR row2 in EXECUTE 'select st_geomfromtext(''POINT(1 1)'') as geom' LOOP
		--~ init := array_append(init,row2.geom);				
	--~ END LOOP;

	
	FOR row in EXECUTE 'select distinct * from dumped_roads' LOOP
	--~ FOR row in EXECUTE 'select st_geomfromtext(''LINESTRING(0 0,10 10)'') as geom' LOOP
		--RAISE NOTICE ' LINE geom :  %', st_astext(row.geom);
		res := splitN(row.geom, init);
		--~ RAISE NOTICE ' RES %', array_upper(res,1);		
		IF array_upper(res,1) is NULL THEN
			CONTINUE;
		END IF;		
		FOR i in 1..array_upper(res,1) LOOP
			--~ RAISE NOTICE 'IN OUTER LOOP (%)',st_astext(res[i]);
			INSERT INTO dummy (gid,type_id,type_road,name,geom) VALUES (row.gid,row.type_id,row.type_road,row.name,res[i]);
		END LOOP;
		
	END LOOP;
END;

$$

LANGUAGE 'plpgsql' VOLATILE STRICT;
