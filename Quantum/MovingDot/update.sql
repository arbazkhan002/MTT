WITH updates as (SELECT edge1 as x, sum(0.01*probability) as adds
						FROM probabtable where (edge1=167 and inpath=false and edge2!=348)
					GROUP BY x) 
update probabtable as p set probability = CASE
								WHEN edge1=167 and edge2=348 and inpath=true
								THEN probability + (select adds from updates)
								
								WHEN edge1=167 and edge2!=348 and inpath!=true
								THEN 0.99*probability
							
								ELSE
								probability
								
								END
					
--~ Change this to a general sql query where 167 and 348 are the pair which were in update with true inpath value
