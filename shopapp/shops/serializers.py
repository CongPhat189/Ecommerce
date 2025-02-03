from shops.models import Category, Shop, Tag, Product, User
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)
    def get_image(self, shop):

        if shop.image:
            requests = self.context.get('request')
            if requests:
                return requests.build_absolute_uri('/static/%s' % shop.image.name)
            return '/static/%s' % shop.image.name


class ShopSerializer(BaseSerializer):



    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','price', 'image', 'tags']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data= validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


