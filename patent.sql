CREATE DATABASE IF NOT EXISTS yourdbname DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

CREATE TABLE company
(
id int NOT NULL AUTO_INCREMENT,
cname varchar(255) NOT NULL,
cnumber varchar(255),
PRIMARY KEY (P_Id)
);