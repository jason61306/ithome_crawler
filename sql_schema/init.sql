CREATE USER 'ithome_user'@'localhost' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER; 
GRANT ALL ON crawler.* TO 'ithome_user'@'localhost';
USE crawler;

CREATE TABLE ithome_log (
    id 	CHAR(36) PRIMARY KEY NOT NULL,
    url TEXT NOT NULL,
    title CHAR(140) NOT NULL,
    crawled_time   INT NOT NULL
) CHARACTER SET utf8mb4;
