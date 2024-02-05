CREATE DATABASE IF NOT EXISTS news_data_db;
USE news_data_db;
CREATE table news_articles (tittle varchar(200), content varchar(500) , sentiment varchar(20) , published_at date);