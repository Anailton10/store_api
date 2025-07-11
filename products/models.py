from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Products(models.Model):

    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, default=''
    )
    price = models.DecimalField(decimal_places=2, max_digits=8)
    stock = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
