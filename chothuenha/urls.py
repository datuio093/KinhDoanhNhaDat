"""chothuenha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from home import views as home
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home.get_home,name="home"),
    path('home/' , home.get_home,name="home"),
    path('login/' ,  home.get_login, name="login"),
    path('register/', home.get_register, name="register"),
    path('logout/',home.logout_user,name="logout"),
    path('properties/', home.get_all_properties,name="properties"),
    path('posts/', home.post,name="post"),
    path('posts/<event_id>/' , home.show_post, name="post_properties"), 
    path('profile/',home.profile , name='profile' ),
    path('review/',home.review , name='review' ),
    path('send-email/<event_id>/', home.send_email, name='send_email'),
    path('add_favorite/', home.add_favorite, name='add_favorite'),
    path('remove_favorite/',home.remove_favorite , name="remove_favorite"),
    path('favorites/', home.show_favorite, name='show_favorite'),
    path('becomeahost/',home.becomeahost, name='becomeahost'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-success/', home.payment_success, name='payment-success'),
    path('payment-failed/', home.payment_failed, name='payment-failed'),
    path('activate/<uidb64>/<token>' , home.get_activate, name="activate")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 