from shops.models import Category, Shop, Tag, Product, User,Comment, Like, Order, Rating
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

        def create(self, validated_data):
            data = validated_data.copy()
            tags = data.pop('tags')
            shop = Shop(**data)
            shop.save()
            shop.tags.set(tags)
            return shop


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','price', 'image', 'tags']

        def create(self, validated_data):
            data = validated_data.copy()
            tags = data.pop('tags')
            product = Product(**data)
            product.save()
            product.tags.set(tags)
            return product





class ProductDetailSerializer(ProductSerializer):

    liked = serializers.SerializerMethodField()


    def get_liked(self, product):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return product.like_set.filter(active = True).exists()
    class Meta:
        model= ProductSerializer.Meta.model
        fields = ProductSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'role','is_verified']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified' : {'read_only': True}
        }

    def create(self, validated_data):
        data= validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'product']
        extra_kwargs = {
            'user': {'read_only': True},

        }


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'active', 'user', 'product']
        extra_kwargs = {
            'user': {'read_only': True},

        }

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rate']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'payment_method', 'created_date']
        extra_kwargs = {
            'user': {'read_only': True},
            'total_price': {'read_only': True},
            'created_date': {'read_only': True},
        }




