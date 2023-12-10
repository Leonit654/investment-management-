import pandas as pd
from django.forms import DecimalField
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from investment.models import Cash_flows, Trades
from decimal import Decimal
from investment.api.serializers import CashFlowSerializer, TradeSerializer


class UploadFileView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('cash_flows')
        trade_file = request.FILES.get('trades')

        if trade_file:
            df_trades = pd.read_excel(trade_file)
            df_trades['investment_date'] = pd.to_datetime(df_trades['investment_date'], format='%d/%m/%Y').dt.strftime(
                '%Y-%m-%d')
            df_trades['maturity_date'] = pd.to_datetime(df_trades['maturity_date'], format='%d/%m/%Y').dt.strftime(
                '%Y-%m-%d')

            for index, row in df_trades.iterrows():
                trade = Trades(
                    loan_id=row['loan_id'],
                    investment_date=row['investment_date'],
                    maturity_date=row['maturity_date'],
                    interest_rate=row['interest_rate']
                )
                trade.save()

            return Response("Trades uploaded successfully", status=200)
        elif cashflow_file:
            df_cashflows = pd.read_excel(cashflow_file)
            df_cashflows['cashflow_date'] = pd.to_datetime(df_cashflows['cashflow_date'],
                                                           format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            for index, row in df_cashflows.iterrows():
                try:
                    trade = Trades.objects.get(loan_id=row['loan_id'])
                    amount = Decimal(row['amount'].replace(',', '').strip())
                    cashflow = Cash_flows(
                        cashflow_id=row['cashflow_id'],
                        trade=trade,
                        cashflow_date=row['cashflow_date'],
                        cashflow_currency=row['cashflow_currency'],
                        cashflow_type=row['cashflow_type'],
                        amount=amount
                    )
                    cashflow.save()
                except Trades.DoesNotExist:
                    pass
            return Response("Cash flows uploaded successfully", status=200)
        else:
            return Response("Please upload the trades file", status=400)


class GetRealizedAmountView(APIView):
    def get(self, request, pk, referencedate):
        try:
            trade = Trades.objects.get(pk=pk)
            realized_amount = trade.realized_amount(referencedate)

            serialized_trade = TradeSerializer(trade)
            serialized_data = serialized_trade.data
            serialized_data['realized_amount'] = realized_amount

            return Response(serialized_data, status=200)
        except Trades.DoesNotExist:
            return Response("Trade does not exist", status=404)


class GetRemainingAmountView(APIView):
    def get(self, request, pk, referencedate):
        try:
            trade = Trades.objects.get(pk=pk)
            remaining_invested_amount = trade.remaining_invested_amount(referencedate)

            serialized_trade = TradeSerializer(trade)
            serialized_data = serialized_trade.data
            serialized_data['remaining_invested_amount'] = remaining_invested_amount

            return Response(serialized_data, status=200)
        except Trades.DoesNotExist:
            return Response("Trade does not exist", status=404)


class GetGrossExpectedAmount(APIView):
    def get(self, request, pk, referencedate):
        try:
            trade = Trades.objects.get(pk=pk)
            gross_expected_amount = trade.gross_expected_amount(referencedate)

            serialized_trade = TradeSerializer(trade)
            serialized_data = serialized_trade.data
            serialized_data['gross_expected_amount'] = gross_expected_amount

            return Response(serialized_data, status=200)
        except Trades.DoesNotExist:
            return Response("Trade does not exist", status=404)


class GetClosingDateView(APIView):
    def get(self, request, pk):
        try:
            trade = Trades.objects.get(pk=pk)
            closing_date = trade.get_closing_date()

            serialized_trade = TradeSerializer(trade)
            serialized_data = serialized_trade.data
            serialized_data['Closing date'] = closing_date

            return Response(serialized_data, status=200)
        except Trades.DoesNotExist:
            return Response("Trade does not exist", status=404)


class GetCashFlowsView(APIView):
    def get(self, request, pk):
        try:
            trade = Trades.objects.get(pk=pk)
            cash_flows = trade.cashflows.all()
            serializer = CashFlowSerializer(cash_flows, many=True)
            return Response(serializer.data, status=200)
        except Trades.DoesNotExist:
            return Response("Trade does not exist", status=404)
