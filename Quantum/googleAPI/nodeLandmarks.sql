--~ Adding intrinsic landmarks:
--~ Create a table nodeLandmarks (See nodeLandmarks.sql)
--~ add all intersections to salience with id=-1
--~ reset all ids of the table salience with the code given in nodeLandmarks.sql  (starts with "with" command)
--~ now recreate sectlandmarks (as ids have changed)
--~ add all intrinsic landmarks in sectlandmarks (0.01 is the required distance)

CREATE TABLE nodeLandmarks AS SELECT X.geom as geom, count(*) as connections
FROM (
	SELECT row_number() OVER (ORDER BY foo.p)::integer AS id,
          foo.p AS geom
		FROM (
		  SELECT DISTINCT st_startpoint(geom) AS p FROM network_dumppoints
		  UNION
		  SELECT DISTINCT st_endpoint(geom) AS p FROM network_dumppoints
		) foo
	   GROUP BY foo.p
) X, network_dumppoints as N
where X.geom = st_startpoint(N.geom) or X.geom=st_endpoint(N.geom);

insert into salience select -1, 'intrinsic', geom, ' ', 0, 0, id from nodeLandmarks where connections>2;  
 
with X as (select row_number() over (order by geom)::integer as rnum, geom from salience) update salience set id=X.rnum from X where salience.geom=X.geom;		

--- before moving on next execute annotatedmap sql again on demo database

insert into sectlandmark select foo.dump_id as dump_id,foo.lid as ref_id,foo.dist as dist 
	from (select N.dump_id as dump_id ,L.id as lid,st_distance(N.geomline,L.geom) as dist 
			from network_dumppoints as N JOIN salience as L ON st_dwithin(N.geomline,L.geom,0.001) and L.category='intrinsic'
		  )
foo;	
