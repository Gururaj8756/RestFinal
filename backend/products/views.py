from urllib import request
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
from api.mixins import StaffEditorPermissionMixin,UserQuerySetMixin
from api.authentication import TokenAuthentication
# Use the correct import for Http404


from api.permissions import IsStaffEditorPermission

class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
#     authentication_classes=[authentication.SessionAuthentication,
#    TokenAuthentication,]
   

    def perform_create(self, serializer):
       # email = serializer.validated_data.pop('email')
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', title)  # Use default value if content is None
        serializer.save(user=self.request.user,content=content)
        # send a Django signal
    
    # def get_queryset(self,*args, **kwargs):        
    #     qs=super().get_queryset(*args,**kwargs)
    #     request=self.request
    #     user=request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)



product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
     UserQuerySetMixin,
    StaffEditorPermissionMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Set the lookup field to 'pk'
   
product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
     UserQuerySetMixin,
    StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
   
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
   
    # The default perform_destroy method already handles deletion, no need to override it.

product_destroy_view = ProductDestroyAPIView.as_view()


class ProductMixinView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', 'COOL')  # Use default value if content is None
        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    if request.method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        else:
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)
    
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content', title)  # Use default value if content is None
            serializer.save(content=content)
            return Response(serializer.data, status=201)  # Return 201 Created status
        return Response(serializer.errors, status=400)  # Return 400 Bad Request if data is invalid
