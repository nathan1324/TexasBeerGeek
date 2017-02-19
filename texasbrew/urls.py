from django.conf.urls import url
from . import views

app_name = 'texasbrew'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<brewery_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<beer_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.beers, name='songs'),
    url(r'^create_brewery/$', views.create_brew, name='create_album'),
    url(r'^(?P<brewery_id>[0-9]+)/create_song/$', views.create_beer, name='create_song'),
    url(r'^(?P<brewery_id>[0-9]+)/delete_song/(?P<beer_id>[0-9]+)/$', views.delete_beer, name='delete_song'),
    url(r'^(?P<brewery_id>[0-9]+)/favorite_album/$', views.favorite_brewery, name='favorite_album'),
    url(r'^(?P<brewery_id>[0-9]+)/delete_album/$', views.delete_brewery, name='delete_album'),
]
