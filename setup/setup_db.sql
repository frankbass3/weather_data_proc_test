CREATE EXTENSION postgis;

SELECT postgis_version();
    
CREATE TABLE IF NOT EXISTS weather_data (
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    timezone VARCHAR(50),
    offset_data FLOAT,
    elevation INT,
    current_time BIGINT NOT NULL,
    icon VARCHAR(50),
    summary TEXT,
    precip_intensity FLOAT,
    precip_accumulation FLOAT,
    precip_type VARCHAR(50),
    temperature FLOAT,
    apparent_temperature FLOAT
    dew_point FLOAT,
    pressure FLOAT,
    wind_speed FLOAT,
    wind_gust FLOAT,
    wind_bearing FLOAT
    cloud_cover FLOAT,
    snow_accumulation FLOAT,
    PRIMARY KEY (latitude, longitude, current_time)
);

CREATE TABLE IF NOT EXISTS regions (
    region_name VARCHAR(100) NOT NULL,
    region_istat VARCHAR(10),
    region_boundaries POLYGON,
    PRIMARY KEY (region_istat)
);


CREATE TABLE IF NOT EXISTS provinces (
    province_name VARCHAR(100) NOT NULL,
    province_istat_code VARCHAR(10),
    province_boundaries MULTIPOLYGON,
    PRIMARY KEY (province_istat_code)
);

CREATE TABLE IF NOT EXISTS cities (
    sigla_provincia VARCHAR(2),
    codice_istat VARCHAR(10) NOT NULL,
    denominazione_ita VARCHAR(100),
    lat FLOAT,
    lon FLOAT,
    superficie_kmq FLOAT,
    PRIMARY KEY (codice_istat)
);
