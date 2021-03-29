from . import views
from django.urls import path

urlpatterns = [
	path('add/universal/', views.CreateUniversal.as_view(), name='create-universal-new'),
	# path('add/universal/', views.CreateImage.as_view(), name='create-universal-new'),
	# path('test/', views.TestSite.as_view(), name='test-photo'),
	path('list/', views.ListPostsAPIView.as_view(), name='list'),
	path('detail/<id>/', views.DetailApiView.as_view(), name='detail'),
	path('profile/list/', views.ProfileListAPIView.as_view(), name='profile-list'),
	path('edit/<id>/', views.EditPost.as_view(), name='edit'),
	# path('upload/image/', views.CreatePhoto.as_view(), name='upload-photo'),
]
