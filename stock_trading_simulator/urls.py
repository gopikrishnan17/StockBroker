"""
URL configuration for stock_trading_simulator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from home.views import *
from buystocks.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', homepage, name = 'homepage'),
    path('dashboard/indexdisplay/', indexdisplay, name = 'indexdisplay'),
    path('dashboard/allstockdisplay/', allstockdisplay, name = 'allstockdisplay'),
    path('stock/<symbol>', stockdisplay, name = 'stockdisplay'),
    path('dashboard/stockreturn/', stockreturn, name = 'stockreturn'),
    path('testpage', stockdisplay, name = 'stockdisplay'),
    path("login/", login_page, name='login_page'),
    path("register/", register_page, name='register_page'),
    path("logout/", logout_page, name='logout_page'),
    path('funds/', fundspage, name = 'fundspage'),
    path('api/add_funds/', add_funds, name = 'add_funds'),
    path('api/withdraw_funds/', withdraw_funds, name = 'withdraw_funds'),
    path('stock/<symbol>/buy/', buyorderpage, name = 'buyorderpage'),
    path('api/buystock/', placebuyorder, name = 'placebuyorder'),
    path('orders/', displayorders, name='displayorders'),
    path('api/cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('portfolio/', displayportfolio, name = 'displayportfolio'),
]
