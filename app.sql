CREATE DATABASE word_clouds;

CREATE TABLE word_cloud (
    id SERIAL PRIMARY KEY,
    s3_path varchar(255) NULL,
    is_generated bool NOT NULL,
    error_msg varchar(255) NULL,
    title varchar(255) NOT NULL,
    text text NOT NULL,
    created timestamp NOT NULL DEFAULT NOW(),
    updated timestamp NOT NULL DEFAULT NOW() ON UPDATE NOW()
);