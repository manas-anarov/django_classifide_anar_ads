from django.contrib import admin
from .models import Area
from .models import Group
from .models import Item

from .models import CarType
from .models import ItemType
from .models import CategoryForCar

from .models import ItemImage
from .models import ThumbnailsImage


admin.site.register(Area)
admin.site.register(Group)
admin.site.register(Item)

admin.site.register(CarType)
admin.site.register(ItemType)
admin.site.register(CategoryForCar)
admin.site.register(ItemImage)
admin.site.register(ThumbnailsImage)