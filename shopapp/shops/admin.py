from string import Template

from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Category, Shop, Product, Tag, User
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.urls import path
from shops import dao


class ShopAppAdminSite(admin.AdminSite):
    site_header = 'iShop'


    def get_urls(self):
        return [
            path('shop-stats/', self.stats_view)
        ] +  super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_shops_by_cate()
        })




admin_site = ShopAppAdminSite(name='admin_shopapp')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk','name']
    search_fields = ['name']
    list_filter =['id', 'name']


class ShopForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Shop
        fields = '__all__'


class TagInlineAdmin(admin.StackedInline):
    model = Shop.tags.through




class ShopAdmin(admin.ModelAdmin):
    list_display = ['pk','shop_name','created_date','updated_date','category','active',]
    readonly_fields = ['img']
    inlines = [TagInlineAdmin]
    form = ShopForm

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



admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Product)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Shop, ShopAdmin)
admin_site.register(Product)
admin_site.register(Tag)
admin_site.register(User)




