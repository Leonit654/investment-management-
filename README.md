To run the django server, first you need to run the command: **docker-compose up**

Then, to be able to access the different methods, first you need to upload two xlsx files,
one for trade and one for cashflows.

To upload the files, run a POST request in POSTMAN with this API: http://127.0.0.1:8000/investment/upload/

You need to pass the files in body/form-data part in POSTMAN. Preferably it's good to pass the file for trades first.

If you want to upload trades file, in the Key part in body/form-data you need to pass **trades** and then the file in Value section.

If you want to upload cashflow file, in the Key part in body/form-data you need to pass **cash_flows** and then the file in Value section.

After you've uploaded the files, now you can test different methods and endpoints. Below is a list with some examples that will show 
you how to write the endpoints :

**Note** : In all endpoints, the reference date needs to be in the format : **%Y-%m-%d**

* To get realized amount for a trade in reference date, you can use: http://127.0.0.1:8000/investment/realized-amount/<str:pk>/<str:referencedate>/

* To get remaining invested amount for a trade in reference date, u can use:
    http://127.0.0.1:8000/investment/remaining-amount/<str:pk>/<str:referencedate>/
* To get gross expected amount for a trade, you can use the API:
    http://127.0.0.1:8000/investment/gross-expected-amount/<str:pk>/<str:referencedate>/
* To get closing date for a trade you can use the API:
    http://127.0.0.1:8000/investment/get-closing-date/<str:pk>/
* To get all the cashflows for a trade, use can use the API:
    http://127.0.0.1:8000/investment/get-cashflows/<str:pk>/

**Replace <<str:pk>> with the loan id, and <<str:referencedate>> with a date in the format that is shown above**

