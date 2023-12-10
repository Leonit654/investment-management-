"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path, include
from investment.api.views import UploadFileView, GetRealizedAmountView, GetRemainingAmountView, GetGrossExpectedAmount, \
    GetClosingDateView, GetCashFlowsView

urlpatterns = [

    path("upload/", UploadFileView.as_view(), name="upload-files"),
    path("realized-amount/<str:pk>/<str:referencedate>/", GetRealizedAmountView.as_view(), name="realized-amount"),
    path("remaining-amount/<str:pk>/<str:referencedate>/", GetRemainingAmountView.as_view(), name="remaining-amount"),
    path("gross-expected-amount/<str:pk>/<str:referencedate>/", GetGrossExpectedAmount.as_view(),
         name="gross-expected-amount"),
    path("get-closing-date/<str:pk>/", GetClosingDateView.as_view(), name="closing-date"),
    path("get-cashflows/<str:pk>/", GetCashFlowsView.as_view(), name="cashflow-details"),
]
