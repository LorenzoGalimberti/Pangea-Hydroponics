from django.contrib import admin
from store.models import Catalogo, Price,Cart
# Register your models here.
from .models import Catalogo,RecensionePostModel


class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]


admin.site.register(Catalogo,ProductAdmin)
admin.site.register(RecensionePostModel)
admin.site.register(Cart)