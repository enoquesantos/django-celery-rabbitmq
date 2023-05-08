CREATE DATABASE django_app CHARACTER SET utf8;
CREATE USER 'django'@'%' IDENTIFIED WITH mysql_native_password BY 'c*kqx^&%8LCXd3m&';
GRANT ALL ON django_app.* TO 'django'@'%';
FLUSH PRIVILEGES;