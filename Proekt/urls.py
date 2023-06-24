"""
URL configuration for Proekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from EShop.views import index, register, profile, product, developerTransition, cart, gameList, checkout, addGame, \
    finishCheckout, download, search, developerGames, postTag

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name="index"),
                  path('accounts/register', register, name="register"),
                  path('profile/', profile, name="profile"),

                  path('profile/u/<str:username>', profile, name="profile"),
                  path('profile/developer', developerTransition, name="devtrans"),
                  path('profile/developer/games', developerGames, name="devList"),

                  path('games/<str:developer>/<int:id>', product, name="product"),

                  path('addGame/', addGame, name="addGame"),

                  path('list/', gameList, name='gameList'),
                  path('search/', search, name="search"),

                  path('posttag/', postTag, name="posttag"),

                  path('ratings/', include('star_ratings.urls', namespace='ratings')),

                  path('cart/', cart, name="cart"),
                  path('checkout/', checkout, name="checkout"),
                  path('finishCheckout/', finishCheckout, name="fCheckout"),

                  path('download/<int:id>', download, name="download"),

                  path("accounts/", include("django.contrib.auth.urls"))

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL,
                                                                                          document_root=settings.MEDIA_ROOT)
