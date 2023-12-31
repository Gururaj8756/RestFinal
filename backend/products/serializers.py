from importlib.util import source_hash
from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer
from .validators import validate_title_no_again,unique_product_title

class ProductInlineSerializer(serializers.ModelSerializer):
   
    url=serializers.HyperlinkedIdentityField(
        view_name='product-detail',lookup_field='pk',
        )
    title=serializers.CharField(validators=[validate_title_no_again,unique_product_title])


class ProductSerializer(serializers.ModelSerializer):
    owner=UserPublicSerializer(source='user',read_only=True)
    edit_url=serializers.SerializerMethodField(read_only=True)
    url=serializers.HyperlinkedIdentityField(
        view_name='product-detail',lookup_field='pk',
        )
    title=serializers.CharField(validators=[validate_title_no_again,unique_product_title])
    body= serializers.CharField(source='content')
    
    #email=serializers.EmailField(source='user.email',read_only=True)
    
    class Meta:
       model=Product
       fields=[
           'owner', 
           'url', 
           'edit_url',
           'pk',
           'title',
           'body',
           'price',
           'sale_price',
           'public',
           'path',
        ]

    def get_my_user_data(self,obj):
        return{
            'username':obj.user.username
        }

    def get_edit_url(self,obj):
        request=self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit",kwargs={'pk':obj.pk},request=request)
        

    def get_my_discount(self,obj):
        if not hasattr(obj,'id'):
            return None
        if not isinstance(obj,Product):
            return None
        return obj.get_discount()