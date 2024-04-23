from django.urls import  path
from .views import index  , save
urlpatterns = [
	path("",index,name="index"),
	path("save",save , name="save_report")
]