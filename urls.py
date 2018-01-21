from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/(?P<category_id>\w+)', views.CategoriesView.as_view()),
    url(r'^categories', views.CategoriesView.as_view())
]
