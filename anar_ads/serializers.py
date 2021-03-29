from rest_framework import serializers
from rest_framework.fields import CreateOnlyDefault, CurrentUserDefault
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)

from .models import Item, Area, Group, CarType, ItemType, ItemImage, ThumbnailsImage, CategoryForCar
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist


class CreateUniversalSerializer(ModelSerializer):
    area = serializers.IntegerField(source='area.id')
    group = serializers.IntegerField(source='group.id')
    item_type = serializers.IntegerField(source='item_type.id')
    year = serializers.IntegerField(write_only=True, required=False)
    car_type = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Item
        fields = [
            'area',
            'group',
            'title',
            'description',
            'price',
            'is_active',
            'item_type',
            'year',
            'car_type',
        ]

    def validate_area(self, value):
        area_qs = Area.objects.filter(id=value)
        if not area_qs.exists():
            raise ValidationError("Area does  not exist")
        return value

    def validate_group(self, value):
        area_qs = Group.objects.filter(id=value)
        if not area_qs.exists():
            raise ValidationError("Group does  not exist")
        return value

    def validate_item_type(self, value):
        item_type_id = value
        item_type_qs = ItemType.objects.filter(id=item_type_id)
        if not item_type_qs.exists():
            raise ValidationError("ItemType does  not exist")
        return value

    def validate_car_type(self, value):
        car_type_id = value
        user_qs = CarType.objects.filter(id=car_type_id)
        if not user_qs.exists():
            raise ValidationError("CarType does  not exist")
        return value


class ListSerializer(ModelSerializer):
    image_has = serializers.SerializerMethodField('get_has_image')
    image_first = serializers.SerializerMethodField('get_image_main')

    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'description',
            'price',
            'is_active',
            'image_has',
            'image_first',
            'item_type',
        ]

    def get_has_image(self, obj):
        all_images = ItemImage.objects.filter(item=obj.id)
        if all_images.exists():
            big_image = ItemImage.objects.filter(item=obj.id).first()
            if big_image:
                sub = ThumbnailsImage.objects.filter(image=big_image).first()
                if sub:
                    return True
            return False
        else:
            return False

    def get_image_main(self, obj):
        all_images = ItemImage.objects.filter(item=obj.id)

        if all_images.exists():
            big_image = ItemImage.objects.filter(item=obj.id).first()
            if big_image:
                sub = ThumbnailsImage.objects.filter(image=big_image).first()
                if sub:
                    return sub.avatar_thumbnail.url
            return "/media/none/no-img.jpg"
        else:
            return "/media/none/no-img.jpg"


class DetailSerializer(ModelSerializer):
    image_first = serializers.SerializerMethodField('get_image_main')
    image_has = serializers.SerializerMethodField('get_has_image')
    year = serializers.SerializerMethodField()
    car_type_name = serializers.SerializerMethodField()
    images_slider = serializers.SerializerMethodField()
    area = serializers.IntegerField(source='area.id')
    group = serializers.IntegerField(source='group.id')
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'description',
            'price',
            'is_active',
            'image_first',
            'image_has',
            'year',
            'car_type_name',
            'images_slider',
            'item_type',
            'area',
            'group'
        ]

    def get_image_main(self, obj):
        all_images = ItemImage.objects.filter(item=obj.id)

        if all_images.exists():
            big_image = ItemImage.objects.filter(item=obj.id).first()
            if big_image:
                # sub = ThumbnailsImage.objects.filter(image=big_image).first()
                # if sub:
                return big_image.photo.url
        else:
            return "/media/none/no-img.jpg"

        # if all_images.exists():
        #     big_image = ItemImage.objects.filter(item=obj.id).first()
        #     if big_image:
        #         sub = ThumbnailsImage.objects.filter(image=big_image).first()
        #         if sub:
        #             return sub.avatar_thumbnail.url
        #     return "/media/none/no-img.jpg"
        # else:
        #     return "/media/none/no-img.jpg"


    def get_has_image(self, obj):
        all_images = ItemImage.objects.filter(item=obj.id)
        if all_images.exists():
            big_image = ItemImage.objects.filter(item=obj.id).first()
            if big_image:
                sub = ThumbnailsImage.objects.filter(image=big_image).first()
                if sub:
                    return True
            return False
        else:
            return False


    def get_year(self, obj):
        if (obj.item_type.id == 2):
            try:
                cat_for_car = CategoryForCar.objects.get(item=obj.id)
            except ObjectDoesNotExist:
                return None
            else:
                return cat_for_car.year

        if (obj.item_type != 2):
            return None

    def get_car_type_name(self, obj):
        if (obj.item_type.id == 2):
            try:
                cat_for_car = CategoryForCar.objects.get(item=obj.id)
            except ObjectDoesNotExist:
                return None
            else:
                return cat_for_car.car_type.name
        if (obj.item_type.id != 2):
            return None

    def get_images_slider(self, obj):
        view = self.context.get('view')
        item_r_getted_id = view.kwargs['id'] if view else None

        item_r_getted = Item.objects.filter(pk=item_r_getted_id)
        if item_r_getted.exists():
            item_r_getted = Item.objects.filter(pk=item_r_getted_id).first()

            all_pics = ItemImage.objects.filter(item=item_r_getted)
            model2_serializer = ImageSliderSerializer(all_pics, many=True)

            return model2_serializer.data
        else:
            return None


class ImageSliderSerializer(ModelSerializer):
    original = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ItemImage
        fields = [
            'original',
            'thumbnail',
            'id'
        ]

    def get_original(self, obj):
        all_images = ItemImage.objects.filter(pk=obj.id)
        if all_images.exists():
            big_image = ItemImage.objects.filter(pk=obj.id).first()
            final_image_url = settings.SITE_URL_FOR_IMAGE + big_image.photo.url
            return final_image_url
        else:
            return "/media/none/no-img.jpg"

    def get_thumbnail(self, obj):
        all_images = ItemImage.objects.filter(pk=obj.id)
        if all_images.exists():
            big_image = ItemImage.objects.filter(pk=obj.id).first()

            sub = ThumbnailsImage.objects.filter(image=big_image).first()

            if sub is not None:
                final_image_url = settings.SITE_URL_FOR_IMAGE + sub.avatar_thumbnail.url
                return final_image_url
            else:
                final_no_image = settings.SITE_URL_FOR_IMAGE + "/media/none/no-img.jpg"
                return final_no_image    
        else:
            final_no_image = settings.SITE_URL_FOR_IMAGE + "/media/none/no-img.jpg"
            return final_no_image
