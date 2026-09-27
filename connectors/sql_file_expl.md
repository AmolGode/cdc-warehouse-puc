# Debezium Postgres User Setup — Explained

```sql
CREATE ROLE debezium WITH REPLICATION LOGIN PASSWORD 'debezium';

GRANT CONNECT ON DATABASE source_db TO debezium;
GRANT USAGE ON SCHEMA public TO debezium;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;

CREATE PUBLICATION dbz_publication FOR ALL TABLES;
```

## `CREATE ROLE debezium WITH REPLICATION LOGIN PASSWORD 'debezium';`

Creates a Postgres user named `debezium` that Kafka Connect will log in as.

- `LOGIN` — this role is allowed to log in (some roles are just permission groups, not login users).
- `REPLICATION` — a special Postgres privilege. Without it, a user can only run normal `SELECT`/`INSERT` queries. With it, the user is also allowed to open a **replication connection** — a different kind of connection Postgres uses to stream the write-ahead log (WAL) instead of running regular queries. Debezium needs this to tail the WAL.

## `GRANT CONNECT / USAGE / SELECT`

Standard permission grants so `debezium` can actually reach the `source_db` database, see the `public` schema, and read (`SELECT`) every table in it. This read access is what Debezium uses for the **initial snapshot** — copying existing rows before it switches to streaming new changes.

## `CREATE PUBLICATION dbz_publication FOR ALL TABLES;`

This is the Postgres-specific part.

Postgres's logical replication works like a subscription model: you first define a **publication** — a named group of tables whose changes should be exposed for streaming. Nothing streams by default; you have to explicitly say "expose these tables."

- `dbz_publication` — just a name you choose for this publication (Debezium's connector config will reference it by this name).
- `FOR ALL TABLES` — includes every table in the database automatically (so `Order`, `Distributor`, `City` are all covered without listing them one by one). You could instead do `FOR TABLE orders_order, orders_distributor, orders_city` to be selective.

Debezium's Postgres connector connects using the `debezium` role, opens a replication connection, and reads whatever this publication exposes.






# Table Schema
                   List of relations
 Schema |            Name            | Type  |  Owner   
--------+----------------------------+-------+----------
 public | auth_group                 | table | postgres
 public | auth_group_permissions     | table | postgres
 public | auth_permission            | table | postgres
 public | auth_user                  | table | postgres
 public | auth_user_groups           | table | postgres
 public | auth_user_user_permissions | table | postgres
 public | django_admin_log           | table | postgres
 public | django_content_type        | table | postgres
 public | django_migrations          | table | postgres
 public | django_session             | table | postgres
 public | orders_city                | table | postgres
 public | orders_distributor         | table | postgres
 public | orders_order               | table | postgres
(13 rows)