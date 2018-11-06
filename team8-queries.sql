MYSQL Queries

(done)Given a username or email address, is that user in the database?
select 'u' in (select email from user);  --swap 'u' for any user email

(done)Given a username or email address, is that user an admin user?
select email, is_admin from user where email = 'a'; --swap 'a' for any user email

(done)Which attractions are open right now in Paris?
select attraction_name from (HoursOfOperation join attraction using(attraction_name)) where opening_time <= CURRENT_TIME() and CURRENT_TIME() < closing_time and address like "%Paris%";

(done)Which attractions in Paris don’t require reservations?
select attraction_name from attraction where res_needed=FALSE and address like "%Paris%";

(done)Which attractions in Metz are free?
select a.attraction_name from (paid_attraction pa join attraction a on a.attraction_name=pa.attraction_name) where price=0 and address like "%Metz%";


(done) Show the details for one attraction?
select * from (attraction a join paid_attraction pa on a.attraction_name=pa.attraction_name) join review r on a.attraction_name=r.attraction_name where a.attraction_name = 'Pont Alexandre III';
--swap 'Pont Alexandre III' for any attracation name in database


(done) List all the reviews for an attraction.
select * from review where attraction_name='Notre Dame Cathedral'; --swap 'Notre Dame Cathedral' for any attraction name

(done) List all the reviews written by a particular user.
select * from review where email = 'a'; --swap 'a' for the email of any user that has written a review

(done) Show the details of one review.
select * from review where rev_id=1; --swap (1) for any review ID 1 through 18

(done) List the trips in the database for a particular user.
select trip_id, city, start_date_time, end_date_time, booked, t.email from (user u join trip t on t.email=u.email) where t.email='u'; --swap 'u' for the amil of any user with a trip

(done)For an attraction that requires reservations and already has some reservations for a time slot, how many spots remain for that time slot?
select quantity-sum(party_size) from (reservation r join time_slot ts on ts.res_num = r.res_num) where ts.attraction_name = 'Metz Cathedral' and ts.start_date_time = '2019-01-01 08:00:00';

(done)For one of the trips in the database that has two more more paid activities, what is the total cost of the trip?
select sum(cost) from trip t join activity a on t.trip_id = a.trip_id where t.trip_id = 1; --swap 1 for any trip ID

(done)For one of the public transportation locations in your database, which attractions are nearest to that location (list it as the nearest public transportation)?
select B.attraction_name from public_transportation as A join attraction as B on A.trans_no = B.trans_no where A.trans_no = 5; --swap (5) for any transit ID 1 through 8
