# Registering the Source Connector


```
"tasks.max": "1" in 'debezium-postgres-source.json'

`tasks.max` = how many workers can do the job in parallel — but for Postgres, only 1 worker can ever read the WAL at a time, so it's always 1.
````



Creates the Debezium source connector so it can read the WAL logs of `source_db`.

**REST API:** `http://localhost:8083/connectors`

## Register

```bash
curl -X POST -H "Content-Type: application/json" \
  --data @connectors/debezium-postgres-source.json \
  http://localhost:8083/connectors
```

**Response:**
```json
{
  "name": "source-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "source-db",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "debezium",
    "database.dbname": "source_db",
    "topic.prefix": "source",
    "plugin.name": "pgoutput",
    "publication.name": "dbz_publication",
    "slot.name": "debezium_slot",
    "table.include.list": "public.orders_order,public.orders_distributor,public.orders_city",
    "name": "source-connector"
  },
  "tasks": [],
  "type": "source"
}
```

## Check status

```bash
curl -H "Accept:application/json" localhost:8083/connectors/source-connector/status
```

**Response:**
```json
{
  "name": "source-connector",
  "connector": { "state": "RUNNING", "worker_id": "172.20.0.7:8083", "version": "3.6.3.Final" },
  "tasks": [
    { "id": 0, "state": "RUNNING", "worker_id": "172.20.0.7:8083", "version": "3.6.3.Final" }
  ],
  "type": "source"
}
```

Both `connector.state` and `tasks[].state` show `RUNNING` — connector is live and streaming.

---

## Adding or removing a table later

1. Edit `table.include.list` in `connectors/debezium-postgres-source.json`.
2. Push it with `PUT` (not `POST` — connector already exists):

```bash
curl -X PUT -H "Content-Type: application/json" \
  --data @connectors/debezium-postgres-source.json \
  http://localhost:8083/connectors/source-connector/config
```

**Note:** existing rows in a newly added table won't backfill — only new changes stream in. To backfill, delete and re-create the connector instead:

```bash
curl -X DELETE http://localhost:8083/connectors/source-connector

curl -X POST -H "Content-Type: application/json" \
  --data @connectors/debezium-postgres-source.json \
  http://localhost:8083/connectors
```