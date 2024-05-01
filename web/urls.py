from django.urls import  path , register_converter
from .converters import DateConverter
from .views import index  , save , detail

register_converter(DateConverter , "date")
urlpatterns = [
	path("",index,name="index"),
	path("save",save , name="save_report"),
    path("detail/<date:timerange>",detail, name="detail_view"),
]