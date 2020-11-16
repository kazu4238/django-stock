from django.db import models

# 株式のシンボルを登録するモデル
class Stock(models.Model):
    target_stock = models.CharField(max_length=10)

    def __str__(self):
        return self.target_stock
