CREATE DATABASE word_clouds;

CREATE TABLE word_cloud (
    id SERIAL PRIMARY KEY,
    text text NOT NULL,
    s3_path varchar(255) NULL,
    is_generated bool NOT NULL
);