from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^balance_transaction/', views.balance_transaction, name='balance_transaction'),
]