from decimal import Decimal

from django.db import transaction
from warehouse.models import DimCity, DimDistributor, FactDistributorCitySales

WAREHOUSE_DB = "warehouse"


def handle_city_event(event):
    payload = event["payload"]
    op = payload["op"]
    after = payload["after"]

    print(f"[city] op={op} before={payload.get('before')} after={after}")

    if op == "d":
        DimCity.objects.using(WAREHOUSE_DB).filter(id=payload["before"]["id"]).delete()
        print(f"[city] deleted id={payload['before']['id']}")
        return

    DimCity.objects.using(WAREHOUSE_DB).update_or_create(
        id=after["id"],
        defaults={"name": after["name"], "state": after["state"]},
    )
    print(f"[city] upserted id={after['id']} name={after['name']} state={after['state']}")


def handle_distributor_event(event):
    payload = event["payload"]
    op = payload["op"]
    after = payload["after"]

    print(f"[distributor] op={op} before={payload.get('before')} after={after}")

    if op == "d":
        DimDistributor.objects.using(WAREHOUSE_DB).filter(id=payload["before"]["id"]).delete()
        print(f"[distributor] deleted id={payload['before']['id']}")
        return

    DimDistributor.objects.using(WAREHOUSE_DB).update_or_create(
        id=after["id"],
        defaults={"name": after["name"], "code": after["code"]},
    )
    print(f"[distributor] upserted id={after['id']} name={after['name']} code={after['code']}")


def handle_order_event(event):
    payload = event["payload"]
    op = payload["op"]

    print(f"[order] op={op} before={payload.get('before')} after={payload.get('after')}")

    if op == "c":
        after = payload["after"]
        distributor_id = after["distributor_id"]
        city_id = after["city_id"]
        amount = Decimal(after["amount"])

        with transaction.atomic(using=WAREHOUSE_DB):
            row, created = FactDistributorCitySales.objects.using(WAREHOUSE_DB).select_for_update().get_or_create(
                distributor_id=distributor_id,
                city_id=city_id,
                defaults={"total_amount": amount},
            )
            if not created:
                row.total_amount += amount
                row.save(update_fields=["total_amount"])

        print(f"[order] create applied: distributor={distributor_id} city={city_id} +{amount}")

    elif op == "u":
        before = payload["before"]
        after = payload["after"]

        old_distributor_id = before["distributor_id"]
        old_city_id = before["city_id"]
        old_amount = Decimal(before["amount"])

        new_distributor_id = after["distributor_id"]
        new_city_id = after["city_id"]
        new_amount = Decimal(after["amount"])

        with transaction.atomic(using=WAREHOUSE_DB):
            old_row = FactDistributorCitySales.objects.using(WAREHOUSE_DB).select_for_update().filter(
                distributor_id=old_distributor_id, city_id=old_city_id,
            ).first()
            if old_row:
                old_row.total_amount -= old_amount
                old_row.save(update_fields=["total_amount"])

            new_row, created = FactDistributorCitySales.objects.using(WAREHOUSE_DB).select_for_update().get_or_create(
                distributor_id=new_distributor_id,
                city_id=new_city_id,
                defaults={"total_amount": new_amount},
            )
            if not created:
                new_row.total_amount += new_amount
                new_row.save(update_fields=["total_amount"])

        print(
            f"[order] update applied: removed {old_amount} from "
            f"(distributor={old_distributor_id}, city={old_city_id}), added {new_amount} to "
            f"(distributor={new_distributor_id}, city={new_city_id})"
        )

    else:
        print(f"[order] ignored op={op}")


def handle_event(topic, event):
    print(f"[event] topic={topic}")

    if topic.endswith("orders_city"):
        handle_city_event(event)
    elif topic.endswith("orders_distributor"):
        handle_distributor_event(event)
    elif topic.endswith("orders_order"):
        handle_order_event(event)