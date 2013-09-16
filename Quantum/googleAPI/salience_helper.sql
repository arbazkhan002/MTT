--~ insert into salience_helper select a.id,quote_ident('academic area building'),a.name,a.geom,0 from "Academic_area" as a;
--~ insert into salience_helper select a.id,quote_ident('playground'),a.name,a.geom,0 from "playgrounds" as a;
--~ insert into salience_helper select a.id,quote_ident('facility'),a.name,a.geom,0 from "Facilities" as a;
--~ insert into salience_helper select a.id,quote_ident('facility'),a.name,a.geom,0 from "Facilities" as a;
--~ insert into salience_helper select a.id,quote_ident('hostel building'),a.name,a.geom,0 from "Hostel" as a;
--~ insert into salience_helper select a.gid,quote_ident('park'),quote_ident('park'),a.geom,0 from "parks" as a;
--~ insert into salience_helper select a.gid,quote_ident('poi'),a.name,a.geom,0 from "landmarks" as a;
--~ insert into salience_helper select a.gid,quote_ident('pond'),quote_ident('park'),a.geom,0 from "ponds" as a;
--~ insert into salience_helper select a.gid,quote_ident('fence'),a.name,a.geom,0 from "fences" as a;
--~ insert into salience_helper select a.gid,quote_ident('fence'),a.door_no,a.geom,0 from "residential" as a;
--~ 
--~ alter table salience_helper rename to temp;
--~ 
--~ create table salience_helper as select old_salience.id as id, old_salience.category as category, old_salience.geom as geom, old_salience.name as name,poi.counter as wiki from (select a.id as id, count(*) as counter from temp as a, poi as p where (p.geom @ a.geom)=true group by a.id) as poi RIGHT JOIN temp as old_salience ON poi.id=old_salience.id;

alter table salience_helper add column google integer;

update salience_helper set google=1000;
drop table temp;
alter table salience_helper rename to temp;

create table salience_helper as select old_salience.id as id, old_salience.category as category, old_salience.geom as geom, old_salience.name as name, old_salience.wiki as wiki,poidata.pos as google from (select a.id as id, min(p.rank) as pos from temp as a, poigoogle as p where (p.geom @ a.geom)=true group by a.id) as poidata RIGHT JOIN temp as old_salience ON poidata.id=old_salience.id;
