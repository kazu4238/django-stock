from django.contrib import admin
from .models import Stock

# Modelを登録する際には、ここへの記述とmigrateを忘れないこと！

admin.site.register(Stock)
