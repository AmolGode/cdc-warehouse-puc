from django.contrib import admin

from warehouse.models import DimCity, DimDistributor, FactDistributorCitySales
from warehouse.upserts import WAREHOUSE_DB


class WarehouseDBAdminMixin:
    def get_queryset(self, request):
        return super().get_queryset(request).using(WAREHOUSE_DB)

    def save_model(self, request, obj, form, change):
        obj.save(using=WAREHOUSE_DB)

    def delete_model(self, request, obj):
        obj.delete(using=WAREHOUSE_DB)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["using"] = WAREHOUSE_DB
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DimCity)
class DimCityAdmin(WarehouseDBAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "state")
    search_fields = ("name", "state")


@admin.register(DimDistributor)
class DimDistributorAdmin(WarehouseDBAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name", "code")


@admin.register(FactDistributorCitySales)
class FactDistributorCitySalesAdmin(WarehouseDBAdminMixin, admin.ModelAdmin):
    list_display = ("id", "distributor", "city", "total_amount")
    list_filter = ("distributor", "city")
