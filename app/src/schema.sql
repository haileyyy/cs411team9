create database userInfo; 
use userInfo;

create table user (
user_ID int(10) auto_increment,
user_name varchar(50),
birthdate date, 
password varchar(10),
primary key (user_ID)
); 

create table service(
service_ID int (10) auto_increment,
service_name varchar(50),
primary key (service_ID)
);

create table userService(
user_ID int (10),
service_ID int (10),
primary key (user_ID, service_ID),
foreign key (service_ID) references service(service_ID),
foreign key (user_ID) references user(user_ID)
) ;

create table genre(
genre_ID int(10) auto_increment,
genre_name varchar(50),
primary key (genre_ID)
);

create table userScore(
user_ID int(10),
genre_ID int(10),
user_score int(10),
primary key (user_ID, genre_ID),
foreign key (genre_ID) references genre(genre_ID),
foreign key (user_ID) references user(user_ID)
);

create table watchedMovies(
user_ID int(10),
movie_ID varchar(50),
liked boolean,
primary key (user_ID, movie_ID),
foreign key (user_ID) references user(user_ID)
);




