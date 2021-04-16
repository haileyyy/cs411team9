create database userInfo;
use userInfo;

create table user (
user_ID int(10) auto increment,
user_name varchar(50),
birthdate date, 
password varchar(10),
primary key (user_ID)
); 

create table userService(
user_ID int (10),
service_ID int (10),
primary key (user_ID, service_ID),
foreign key (service_ID) references service(service_ID),
foreign key (user_ID) references user(user_ID)
) ;

create table service(
service_ID int (10) auto increment,
service_name varchar(50),
primary key (service_ID)
)
