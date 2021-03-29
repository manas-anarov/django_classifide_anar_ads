from django.db import models
from restaccounts.models import ExtendedUser
from django.utils.translation import ugettext as _


from django.contrib.contenttypes.models import ContentType
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class Area(models.Model):
    slug = models.SlugField()
    title = models.CharField(_('title'), max_length=100)


class Group(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)


class Item(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_('group'), on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_('area'), on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_('active'), default=False, db_index=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, db_index=True)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)
    item_type = models.ForeignKey('ItemType', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CarType(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name


class ItemType(models.Model):
    category = models.ManyToManyField(ContentType)
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name


class CategoryForCar(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/images/', height_field=None, width_field=None, max_length=100)
    posted = models.DateTimeField(_('posted'), auto_now_add=True)

    def __str__(self):
        return self.item.title

class ThumbnailsImage(models.Model):
    image = models.ForeignKey(ItemImage, on_delete=models.CASCADE)
    avatar_thumbnail = ProcessedImageField(upload_to='avatars',
                                           processors=[ResizeToFill(250, 150)],
                                           format='JPEG',
                                           options={'quality': 60})