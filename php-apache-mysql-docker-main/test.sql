-- Create test database
CREATE DATABASE IF NOT EXISTS test;

-- Use test database
USE test;

-- Create countrecords_counttray table
CREATE TABLE IF NOT EXISTS countrecords_counttray (
    count_id INT AUTO_INCREMENT PRIMARY KEY,
    Lot_id VARCHAR(50),
    Direction VARCHAR(50),
    Timestamp VARCHAR(50),
    Machine_ID INT,
    Substrate INT,
    TTL INT,
    badmark INT,
    ASSY_input INT,
    NG INT,
    Good INT,
    Business_id INT,
    Judgement VARCHAR(50),
    FOREIGN KEY (Machine_ID) REFERENCES station(Machine_ID),
    FOREIGN KEY (Business_id) REFERENCES business(Business_id)
);

-- Create business table
CREATE TABLE IF NOT EXISTS business (
    Business_id INT PRIMARY KEY,
    Business_name VARCHAR(50)
);

-- Create station table
CREATE TABLE IF NOT EXISTS station (
    Machine_ID INT PRIMARY KEY,
    Machine_name VARCHAR(50),
    Business_id INT,
    FOREIGN KEY (Business_id) REFERENCES business(Business_id)
);
