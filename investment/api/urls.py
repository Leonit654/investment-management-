
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
