CREATE DATABASE app CHARACTER SET utf8;
CREATE USER 'app'@'%' IDENTIFIED WITH mysql_native_password BY 'c*kqx^&%8LCXd3m&';
GRANT ALL ON app.* TO 'app'@'%';
FLUSH PRIVILEGES;