from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.views import Voivodeships, Powiats, Gminas, Constituencies, ConstituencyView


urlpatterns = patterns('',
                       url(r'^$', Voivodeships.as_view(), name='voivodeships'),
                       url(r'^voivodeship/([0-9]+)$', Powiats.as_view(), name='powiats'),
                       url(r'^powiat/([0-9]+)$', Gminas.as_view(), name='gminas'),
                       url(r'^gmina/([0-9]+)$', Constituencies.as_view(), name='constituencies'),
                       url(r'^constituency/([0-9]+)$', ConstituencyView.as_view(), name='constituency'),
                       url(r'^admin/', include(admin.site.urls)),
                       )



