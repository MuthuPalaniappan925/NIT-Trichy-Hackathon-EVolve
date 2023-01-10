CREATE DATABASE EVMUTHU;
USE EVMUTHU;

CREATE TABLE IF NOT exists EVStations_list (
	id int(10) NOT NULL auto_increment,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    PRIMARY KEY(ID)
) engine=InnoDB auto_increment=2 default charset=utf8;

