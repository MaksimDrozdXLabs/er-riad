from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

class Generator(OpenAPISchemaGenerator):
    pass

schema_view = get_schema_view(
   openapi.Info(
      title="Football Riyadh Demo API",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   patterns=[
       re_path(
           r'participant/',
           include('python.io_atomgroup.soccer.participant.urls'),
           name='participant',
       ),
       re_path(
           r'socket.io/',
           include('python.io_atomgroup.soccer.estimator.openapi.sio'),
           name='socketio',
       ),
       re_path(
           r'mqtt/',
           include('python.io_atomgroup.soccer.estimator.openapi.mqtt'),
           name='mqtt',
       ),
   ],
   public=True,
   permission_classes=[permissions.AllowAny,],
   generator_class=Generator,
)

urlpatterns = [
    #re_path(
    #    r'leaderboard/',
    #    include('python.io_atomgroup.soccer.leaderboard.urls'),
    #    name='leaderboard',
    #),
    re_path(
        r'participant/',
        include('python.io_atomgroup.soccer.participant.urls'),
        name='participant',
    ),
    # path(r'swagger<format>/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
