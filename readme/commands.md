# Docker Commands — IMPORTANT

```bash
# run from data_warehouse_puc/, where docker-compose.yml lives

docker compose build            # build images
docker compose up -d            # start in background
docker compose up -d --build    # build + start in one go
docker compose ps               # check running containers
docker compose logs -f          # logs, all services
docker compose logs -f source-app
docker compose logs -f warehouse-app
docker compose down             # stop everything
docker compose down -v          # stop + wipe DB volumes
```

**Shell into a Django app container:**
```bash
docker compose exec source-app bash
docker compose exec warehouse-app bash
```

**Run Django management commands directly:**
```bash
docker compose exec source-app python manage.py migrate
docker compose exec source-app python manage.py makemigrations
docker compose exec source-app python manage.py createsuperuser

docker compose exec warehouse-app python manage.py migrate
docker compose exec warehouse-app python manage.py run_consumer
```

**Shell into a DB container (psql):**
```bash
docker compose exec source-db psql -U postgres -d source_db
docker compose exec warehouse-db psql -U postgres -d warehouse_db
```



**Running SQL File in Source DB:**
```bash
docker compose exec -T source-db psql -U postgres -d source_db < connectors/init-debezium-user.sql
```


**List All Topics**
```bash
docker compose exec kafka /kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list
```

**See event in kafka topic**
```bash
docker compose exec kafka /kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --topic source.public.orders_city \
  --from-beginning
```