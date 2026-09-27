from django.db import models


class DimCity(models.Model):
    id = models.IntegerField(primary_key=True)  # same id as source_db's City
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DimDistributor(models.Model):
    id = models.IntegerField(primary_key=True)  # same id as source_db's Distributor
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FactDistributorCitySales(models.Model):
    distributor = models.ForeignKey(DimDistributor, on_delete=models.CASCADE)
    city = models.ForeignKey(DimCity, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("distributor", "city")  # one row per (distributor, city) pair

    def __str__(self):
        return f"{self.distributor.name} - {self.city.name}: {self.total_amount}"