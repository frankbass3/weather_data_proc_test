CREATE EXTENSION postgis;

SELECT postgis_version();

CREATE TABLE weather_data (
	latitude float8 NOT NULL,
	longitude float8 NOT NULL,
	timezone varchar(50) NULL,
	offset_data float8 NULL,
	elevation int4 NULL,
	current_time_t timestamp NOT NULL,
	icon varchar(50) NULL,
	summary text NULL,
	precip_intensity float8 NULL,
	precip_accumulation float8 NULL,
	precip_type varchar(50) NULL,
	temperature float8 NULL,
	apparent_temperature float8 NULL,
	dew_point float8 NULL,
	pressure float8 NULL,
	wind_speed float8 NULL,
	wind_gust float8 NULL,
	wind_bearing float8 NULL,
	cloud_cover float8 NULL,
	snow_accumulation float8 NULL,
	CONSTRAINT weather_data_pkey PRIMARY KEY (latitude, longitude, current_time_t)
);


CREATE TABLE regions (
	region_name varchar(100),
	region_istat varchar(10),
	region_boundaries polygon NULL,
	CONSTRAINT regions_pkey PRIMARY KEY (region_istat)
);


CREATE TABLE IF NOT EXISTS provinces (
    province_name VARCHAR(100) NOT NULL,
    province_istat_code VARCHAR(10),
    province_boundaries MULTIPOLYGON,
    PRIMARY KEY (province_istat_code)
);

CREATE TABLE cities (
	sigla_provincia varchar(10) NULL,
	codice_istat varchar(10) NULL,
	denominazione_ita_altra varchar(255) NULL,
	denominazione_ita varchar(255) NULL,
	denominazione_altra varchar(255) NULL,
	flag_capoluogo varchar(2) NULL,
	codice_belfiore varchar(10) NULL,
	lat float8 NULL,
	lon float8 NULL,
	superficie_kmq float8 NULL,
	codice_sovracomunale varchar(10) NULL
);