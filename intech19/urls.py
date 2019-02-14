from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import homelog.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homelog.views.home,name='home'),
    path('login/',homelog.views.login,name='login'),
    path('signup/',homelog.views.signup,name='signup'),
    path('login/signup',homelog.views.signup,name='signup'),
    path('logout',homelog.views.logout,name='logout'),
    path('login/signup/home',homelog.views.home,name='home'),
    path('signup/home',homelog.views.home,name='home'),
    path('activate/<slug:uidb64>/<slug:token>/', homelog.views.activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/login/', homelog.views.conf_login, name='login'),
    path('cart', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('shop/', include('shop.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
