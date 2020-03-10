--
-- Contains SQL statements to set up the database.
--

-- noinspection SqlNoDataSourceInspectionForFile

CREATE TABLE pothole
(
    id          uuid                     NOT NULL PRIMARY KEY,
    device_name character varying(255)   NOT NULL,
    created_on  timestamp with time zone NOT NULL,
    recorded_on timestamp with time zone NOT NULL,
    confidence  double precision         NOT NULL,
    latitude    double precision         NOT NULL,
    longitude   double precision         NOT NULL,
    geohash     character(12)            NOT NULL
);

CREATE INDEX CONCURRENTLY geohash_index ON pothole (geohash ASC NULLS LAST);
CREATE INDEX CONCURRENTLY recorded_on_index ON pothole (recorded_on DESC NULLS LAST);
