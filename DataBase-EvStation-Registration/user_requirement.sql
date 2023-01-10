USE EVMUTHU;

create table EV_user_list(
 id int(10) NOT NULL auto_increment,
 address VARCHAR(100) NOT NULL,
 charger_type varchar(100) NOT NULL,
 charging_price VARCHAR(50) NOT NULL,
 PRIMARY KEY(id)
) engine=InnoDB auto_increment=2 default charset=utf8;
