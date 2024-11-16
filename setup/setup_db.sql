CREATE EXTENSION postgis;

SELECT postgis_version();

CREATE TABLE IF NOT EXISTS weather_data (
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    offset FLOAT NOT NULL,
    elevation INT NOT NULL,
    current_time BIGINT NOT NULL,
    icon VARCHAR(50),
    summary TEXT,
    precip_intensity FLOAT,
    temperature FLOAT,
    PRIMARY KEY (latitude, longitude, current_time)
);

CREATE TABLE IF NOT EXISTS regions (
    region_name VARCHAR(100) NOT NULL,
    region_istat VARCHAR(10) NOT NULL UNIQUE,
    region_boundaries POLYGON NOT NULL,
    PRIMARY KEY (region_istat)
);


CREATE TABLE IF NOT EXISTS provinces (
    province_name VARCHAR(100) NOT NULL,
    province_istat_code VARCHAR(10) NOT NULL UNIQUE,
    province_boundaries MULTIPOLYGON NOT NULL,
    PRIMARY KEY (province_istat_code)
);

CREATE TABLE IF NOT EXISTS cities (
    sigla_provincia VARCHAR(2) NOT NULL,
    codice_istat VARCHAR(10) NOT NULL UNIQUE,
    denominazione_ita VARCHAR(100) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    superficie_kmq FLOAT NOT NULL,
    PRIMARY KEY (codice_istat)
);
