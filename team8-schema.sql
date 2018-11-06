drop database if exists team8;
create database team8;
use team8;

create table user(
    f_name varchar(254),
    l_name varchar(254),
    email varchar(254),
    password varchar(254),
    is_admin boolean,
    is_suspend boolean,
    is_current boolean,
    primary key(email)
);

create table address(
    address_num varchar(16),
    street varchar(254),
    city varchar(16),
    state varchar(95),
    zip int,
    country varchar(16),
    email varchar(254) not null,

    foreign key (email) references user(email)
        on update cascade
        on delete cascade,
    primary key(address_num, street, city, state, zip, country)
);

create table trip(
    trip_id int primary key auto_increment,
    city varchar(35),
    start_date_time datetime,
    end_date_time datetime,
    booked boolean,
    email varchar(254) not null,
    foreign key (email) references user(email)
        on update cascade
        on delete cascade
);

create table public_transportation(
    trans_no int primary key,
    trans_name varchar(254),
    trans_type varchar(64),
    trans_id varchar(254)
);

create table attraction(
    attraction_name varchar(200) primary key,
    description varchar(2000),
    address varchar(500),
    trans_no int not null,
    res_needed boolean,
    foreign key (trans_no) REFERENCES public_transportation(trans_no)
);

create table activity(
    attraction_name varchar(200),
    start_date_time datetime not null,
    end_time_time datetime not null,
    city varchar(35) not null,
    cost double(10, 2),
    trip_id int not null,
    foreign key (trip_id) references trip(trip_id)
        on update cascade
        on delete cascade,
    foreign key (attraction_name) references attraction(attraction_name)
        on update cascade
        on delete cascade,
    primary key (attraction_name, start_date_time, trip_id)
);

create table reservation(
    res_num int primary key,
    attraction_name varchar(200),
    party_size int,
    trip_id int not null,
    start_date_time datetime not null,
    foreign key (attraction_name, start_date_time, trip_id) references activity(attraction_name, start_date_time, trip_id)
        on update cascade
        on delete cascade
);

create table credit_card(
    ccnumber bigint primary key,
    expiry date,
    cvv int,

    email varchar(254) not null,
    foreign key (email) references user(email)
        on update cascade
        on delete cascade
);


create table review(
    rev_id int primary key auto_increment,
    title varchar(30),
    body varchar(500),
    review_date date,
    attraction_name varchar(200),
    email varchar(254) not null,
    foreign key (email) references user(email)
        on update cascade
        on delete cascade,
    foreign key (attraction_name) references attraction(attraction_name)
        on update cascade
        on delete cascade
);

create table HoursOfOperation(
    day_of_week varchar(9),
    opening_time time,
    closing_time time,
    attraction_name varchar(200) not null,
    foreign key(attraction_name) references attraction(attraction_name)
        on update cascade
        on delete cascade,
    primary key(attraction_name, day_of_week)
);

create table paid_attraction(
    price double(10, 2),
    attraction_name varchar(200) not null,
    foreign key(attraction_name) references attraction(attraction_name)
        on update cascade
        on delete cascade,
    primary key(price, attraction_name)
);

create table time_slot(
    attraction_name varchar(200),
    start_date_time datetime,
    end_date_time datetime,
    quantity int,
    res_num int not null,
    foreign key (res_num) references reservation(res_num)
        on update cascade
        on delete cascade,
    foreign key (attraction_name) references attraction(attraction_name)
        on update cascade
        on delete cascade,
    primary key(start_date_time, end_date_time, attraction_name)
);

create table activities(
    list_name varchar(2000),
    acts_id int primary key,
    email varchar(254) not null,
    foreign key (email) references user(email)
        on update cascade
        on delete cascade
);

