from .models import Category, Shop
from django.db.models import Count


def load_shops(params=()):
    q = Shop.objects.filter(active=True)

    kw = params.get('kw')
    if kw:
        q = q.filter(shop_name__icontains=kw)

    cate_id = params.get('cate_id')

    if cate_id:
        q = q.filter(category_id=cate_id)

    return q

def count_shops_by_cate():
    return Category.objects.annotate(count= Count('shops__id')).values("id","name","count").order_by('-count')
