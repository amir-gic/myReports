from django.urls import  path , register_converter
from .converters import DateConverter
from .views import index  , save , detail , add_task , delete_task , delete_reprot

register_converter(DateConverter , "date")
urlpatterns = [
	path("",index,name="index"),
	path("save",save , name="save_report"),
    path("detail/<date:timerange>",detail, name="detail_view"),
    path("new",add_task,name="add_task"),
    path("delete" , delete_task , name="delete_task"),
    path("delrepo/<int:pk>" , delete_reprot , name="delete_reprot")
]