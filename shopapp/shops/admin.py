from django.contrib import admin
from .models import Category, Shop, Product, Tag
from django.utils.html import mark_safe

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk','name']
    search_fields = ['name']
    list_filter =['id', 'name']


class ShopAdmin(admin.ModelAdmin):
    readonly_fields = ['img']

    def img(self, shops):
        if shops:
            return mark_safe(
                '<img src="/static/{url}" = width="120" />' \
                .format(url=shops.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product)
admin.site.register(Tag)

