from rest_framework.views import APIView
from rest_framework.generics import (RetrieveAPIView, ListAPIView)

from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import (
    CreateUniversalSerializer,
    ListSerializer,
    DetailSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
	IsAuthenticated,
	AllowAny,
)

from .permissions import (
    IsOwnerOrReadOnly,
)

from .models import Group, CategoryForCar, ItemType, Area, CarType, Item, ItemImage, ThumbnailsImage

from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from restaccounts.models import ExtendedUser

from .pagination import PostPageNumberPagination
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from django.shortcuts import get_object_or_404
from django.db.models import Q

def create_db():

    slug = slugify("osh")
    new_area = Area(slug=slug, title="Osh")
    new_area.save()

    slug_group = slugify("auto")
    new_group = Group(slug=slug_group, title="Авто")
    new_group.save()

    new_car_type = CarType(name="Honda")
    new_car_type.save()


    article = ItemType.objects.create(name="Универсал")
    tags = [ContentType.objects.get(id=1),]
    article.category.set(tags)



def test_create_post():
    user = ExtendedUser.objects.get(pk=1)
    area_my = Area.objects.get(pk=1)
    group_my = Group.objects.get(pk=1)

    new_item = Item(
        area=area_my,
        group=group_my,
        title="1",
        description="1",
        price=100,
        is_active=True,
        user=user
    )

    new_item.save()

    item_type_id = 1


    car_type_ser = 1
    car_type_my = CarType.objects.get(pk=car_type_ser)
    year_ser = 1993
    cat_for_car = CategoryForCar(car_type=car_type_my, year=year_ser, item=new_item)
    cat_for_car.save()

    my_type = ItemType.objects.get(pk=item_type_id)
    new_car = ItemMy(item=new_item, item_type=my_type)
    new_car.save()

    article = ItemType.objects.create(name="Универсал")
    tags = [ContentType.objects.get(id=1),]
    article.category.set(tags)


class CreateUniversal(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = [IsAuthenticated, ]


    def post(self, request):
        serializer = CreateUniversalSerializer(data=request.data)

        if serializer.is_valid():

            user = self.request.user
            area_id = serializer.data['area']
            area_my = Area.objects.get(pk=area_id)

            group_id = serializer.data['group']
            group_my = Group.objects.get(pk=group_id)
            slug = slugify("osh")


            item_type_id = serializer.data['item_type']
            my_type = ItemType.objects.get(pk=item_type_id)


            new_item = Item(
                slug=slug,
                area=area_my,
                group=group_my,
                title=serializer.data['title'],
                description=serializer.data['description'],
                price=serializer.data['price'],
                is_active=serializer.data['is_active'],
                user=user,
                item_type=my_type,
            )
            new_item.save()


            if item_type_id == 2:
                car_type_ser = request.data.get('car_type', 1)
                car_type_my = CarType.objects.get(pk=car_type_ser)
                year_ser = request.data.get('year', 1)
                cat_for_car = CategoryForCar(car_type=car_type_my, year=year_ser, item=new_item)
                cat_for_car.save()



            if (request.data.getlist('files')):
                for f in request.data.getlist('files'):
                    mf = ItemImage.objects.create(item=new_item, author=user, photo=f)
                    ThumbnailsImage.objects.create(image=mf, avatar_thumbnail=f)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateImage(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = [AllowAny, ]


    def post(self, request):
        # serializer = CreateUniversalSerializer(data=request.data)

        # if serializer.is_valid():

            # user = self.request.user
        user = ExtendedUser.objects.get(pk=1)
        area_id = 1
        area_my = Area.objects.get(pk=area_id)

        group_id = 1
        group_my = Group.objects.get(pk=group_id)
        slug = slugify("osh")


        item_type_id = 1
        my_type = ItemType.objects.get(pk=item_type_id)


        new_item = Item(
            slug=slug,
            area=area_my,
            group=group_my,
            title="1",
            description="1",
            price="1",
            is_active=True,
            user=user,
            item_type=my_type,
        )
        new_item.save()


            # if item_type_id == 2:
            #     car_type_ser = request.data.get('car_type', 1)
            #     car_type_my = CarType.objects.get(pk=car_type_ser)
            #     year_ser = request.data.get('year', 1)
            #     cat_for_car = CategoryForCar(car_type=car_type_my, year=year_ser, item=new_item)
            #     cat_for_car.save()



        if (request.data.getlist('files')):
            for f in request.data.getlist('files'):
                mf = ItemImage.objects.create(item=new_item, author=user, photo=f)
                ThumbnailsImage.objects.create(image=mf, avatar_thumbnail=f)

            return Response("a", status=status.HTTP_201_CREATED)
        return Response("error", status=status.HTTP_400_BAD_REQUEST)



class ListPostsAPIView(ListAPIView):
    serializer_class = ListSerializer
    pagination_class = PostPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    permission_classes = [AllowAny, ]

    
    def get_queryset(self, *args, **kwargs):
        queryset_list = Item.objects.all().filter(is_active=True).order_by('-id')
        query = self.request.GET.get("area", False)
        brand = self.request.GET.get("brand", False)
        post_type = self.request.GET.get("post_type", False)
        if query:
            queryset_list = queryset_list.filter(
                Q(area__id__icontains=query)
            ).distinct()

        # search brand and ItemMy, if item is equal show all ItemMy
        if brand:

            brand_sort = (f.id for f in CategoryForCar.objects.all().filter(car_type_id=brand))
            queryset_list = queryset_list.filter(
                Q(id__in=brand_sort)
            ).distinct()

            print(queryset_list)

        # query_string_to_int
        if post_type:
            post_type_query = self.request.GET.get('post_type')
            post_type_converted = int(post_type_query)

            queryset_list = queryset_list.filter(
                Q(item_type__id__icontains=post_type)
            ).distinct()


        return queryset_list


class DetailApiView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = DetailSerializer
    lookup_field = 'id'


class ProfileListAPIView(ListAPIView):
    serializer_class = ListSerializer
    pagination_class = PostPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        queryset_list = Item.objects.all().filter(is_active=True, user=current_user).order_by('-id')
        query = self.request.GET.get("area")
        brand = self.request.GET.get("brand")
        post_type = self.request.GET.get("post_type", False)
        if query:
            queryset_list = queryset_list.filter(
                Q(area__id__icontains=query)
            ).distinct()
        if brand:

            brand_sort = (f.id for f in CategoryForCar.objects.all().filter(car_type_id=brand))
            queryset_list = queryset_list.filter(
                Q(id__in=brand_sort)
            ).distinct()

            print(queryset_list)


        if post_type:
            post_type_query = self.request.GET.get('post_type')
            post_type_converted = int(post_type_query)

            queryset_list = queryset_list.filter(
                Q(item_type__id__icontains=post_type)
            ).distinct()
        return queryset_list


class EditPost(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsOwnerOrReadOnly, ]

    def put(self, request, **kwargs):
        item_r_getted_id = kwargs.get('id', 'Default Value if not there')
        item_r_getted = Item.objects.get(pk=item_r_getted_id)
        item_getted = item_r_getted

        serializer = CreateUniversalSerializer(data=request.data)

        if serializer.is_valid():

            user = self.request.user
            area_id = serializer.data['area']
            area_my = Area.objects.get(pk=area_id)

            group_id = serializer.data['group']
            group_my = Group.objects.get(pk=group_id)

            item_type_id = serializer.data['item_type']
            item_type_my = ItemType.objects.get(pk=item_type_id)
                
            item_getted.area = area_my
            item_getted.group = group_my
            item_getted.title = serializer.data['title']
            item_getted.description = serializer.data['description']
            item_getted.price = serializer.data['price']
            item_getted.is_active = serializer.data['is_active']
            item_getted.user = user
            item_getted.item_type = item_type_my
            item_getted.save()

            
            if item_type_id == 2:
                car_type_id = request.data.get('car_type', 1)
                print(car_type_id)
                car_type_my = CarType.objects.get(pk=car_type_id)
                year_my = request.data.get('year', 1)

                item_r_getted.item = item_getted
                item_r_getted.car_type = car_type_my
                item_r_getted.year = year_my
                item_r_getted.save()

            # for f in request.data.getlist('files'):
            #     mf = Image.objects.create(item=item_getted, file=f)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, **kwargs):
        item_r_getted_id = kwargs.get('id', '0')
        item_react = Item.objects.get(pk=item_r_getted_id)
        serializer = DetailSerializer(item_react)
        return Response(serializer.data)

    def delete(self, request, id):
        article = get_object_or_404(Item.objects.all(), pk=id)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(id)
        }, status=204)   




# class TestSite(APIView):
#     authentication_classes = (TokenAuthentication, SessionAuthentication, JSONWebTokenAuthentication)
#     permission_classes = [AllowAny, ]

#     def get(self, request, *args, **kwargs):
#         create_db()
#         test_create_post()
#         return Response({"message": "Got some data!"})    