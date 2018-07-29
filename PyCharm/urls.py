"""PyCharm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import django
import mysite1.views
from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from PyCharm import settings

urlpatterns = [
    #url(r'$', mysite1.views.index),
    #url(r'^admin', admin.site.urls),
    url(r'^test', mysite1.views.test),
    url(r'^index$', mysite1.views.index,name='index'),
    url(r'^generic', mysite1.views.generic,name='generic'),
    url(r'^login$', mysite1.views.login, name='login'),
    url(r'^toLogin$', mysite1.views.toLogin, name='toLogin'),
    url(r'^articles$',mysite1.views.articles,name='ariticles'),
    url(r'^articles/(\d+)$', mysite1.views.articleid, name='ariticleid'),
    url(r'^write$', mysite1.views.write, name='write'),
    url(r'^center$', mysite1.views.center, name='center'),
    url(r'^$', mysite1.views.index),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)