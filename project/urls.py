
from django.contrib import admin
from django.urls import path,include
from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('rest/fbv/',views.FBV_List),
    path('rest/fbv/<int:pk>',views.FBV_pk),

    path('rest/cbv/',views.CBV_List.as_view()),
    path('rest/cbv/<int:pk>',views.CBV_pk.as_view()),

    path("rest/mixins/", views.mixins_List.as_view()),
    path("rest/mixins/<int:pk>" , views.mixins_pk.as_view()),

    path("rest/generics/", views.generics_list.as_view()),
    path("rest/generics/<int:pk>" , views.generics_pk.as_view())


]
