-- connect to source_db as postgres superuser
CREATE ROLE debezium WITH REPLICATION LOGIN PASSWORD 'debezium';

GRANT CONNECT ON DATABASE source_db TO debezium;
GRANT USAGE ON SCHEMA public TO debezium;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;

-- Postgres logical decoding needs a publication
CREATE PUBLICATION dbz_publication FOR ALL TABLES;