"""vikas_minesweeper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from myapp import views as myapp_views


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^draw/', myapp_views.draw, name='draw'),
    url(r'^draw_ajax/(?P<LengthX>\d+),(?P<LengthY>\d+),(?P<Total_Bombs>\d+)/$', myapp_views.draw_ajax, name='draw_ajax'),
    url(r'^checkStatus/(?P<index_id_x>\d+),(?P<index_id_y>\d+)/$', myapp_views.checkStatus, name='checkStatus'),

]
