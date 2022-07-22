drop table if exists adamsczrental_db.position;

-- here I am creating a table with district names and their geological position in case I decided to visualize the data
-- using a map
create table adamsczrental_db.position (district varchar(255), lat float(10,6), lon float(10,6));

insert into adamsczrental_db.position (district, lat, lon) values 
	('Holešovice', 50.102535, 14.440558),
	('Karlín', 50.092748, 14.452123),
	('Malá Strana', 50.086992, 14.404281),
	('Nové Město', 50.078994, 14.423653),
	('Nusle', 50.058259, 14.437786),
	('Smíchov', 50.071319, 14.406027),
	('Staré Město', 50.087539, 14.419768),
	('Vinohrady', 50.075163, 14.447463),
	('Vršovice', 50.067248, 14.458034),
	('Žižkov', 50.085814, 14.461004);

-- sometimes I make a union with a table, before I make a view. The tabes are data collected before using the code of this project
-- the union can be deleted, but then it will take some time, until enough data is collected 

-- this is a view, which shows a percentage share of apartment types on the market
create or replace view adamsczrental_db.layout_share as 
select LAYOUT, round(count(*)*100/(select * from adamsczrental_db.total),2) as lshare from
	(select LISTED_BEFORE, LAYOUT 
	from adamsczrental_db.processed_ads
	where LISTED_BEFORE > date_add(curdate(), interval -12 month) and LAYOUT like "%+%") lay
group by LAYOUT;

-- this is a view, which shows progression of the average rent in the whole area per each month
create or replace view adamsczrental_db.avg_rent as
select lday, avg_r from
((select lday, round(avg(ar.rpm), 0) as avg_r
from

(select last_day(DELISTED_BEFORE) as lday, DELISTED_BEFORE, RENT/SIZE as rpm 
from adamsczrental_db.processed_ads 
where DELISTED_BEFORE is not null) ar

group by lday)
union
(select last_day(avg_date), avg_rent from adamsczrental_db.prev_arpm)
order by 1 desc limit 12) lim
order by 1;

-- this view shows average rent per meter per district for 3 months back
create or replace view adamsczrental_db.arpd as
select pos.district as district, arpd2.rpm as rpm, pos.lat as lat, pos.lon as lon from adamsczrental_db.position pos join 
(select DISTRICT, round(avg(rpm),0) as rpm from

(select DISTRICT, RENT/SIZE as rpm 
from adamsczrental_db.processed_ads 
where LISTED_BEFORE is not null and LISTED_BEFORE > date_add((select LISTED_BEFORE from adamsczrental_db.processed_ads order by LISTED_BEFORE desc limit 1), interval -3 month)
) arpd

group by DISTRICT) arpd2
on pos.district = arpd2.DISTRICT
order by arpd2.rpm;

-- this view shows a progression of listed and delisted ads for each month
create or replace view adamsczrental_db.lvd as

select * from
(select delisted.lday, listed.l, delisted.d from
(select lday, count(*) as d from
(select last_day(DELISTED_BEFORE) as lday, DELISTED_BEFORE 
from adamsczrental_db.processed_ads 
where DELISTED_BEFORE is not null) de 
group by lday) as delisted
join
(select lday, count(*) as l from
(select last_day(LISTED_BEFORE) as lday, LISTED_BEFORE 
from adamsczrental_db.processed_ads 
where LISTED_BEFORE is not null) li 
group by lday) as listed
on delisted.lday = listed.lday
union
(select last_day(sd_date), supply_amount, demand_amount from adamsczrental_db.prev_lvd)
order by 1 desc
limit 12) lim order by 1;

-- this view I created just as a counter of how many ads were processed till today
create or replace view adamsczrental_db.total as 
select count(*) from adamsczrental_db.processed_ads;







