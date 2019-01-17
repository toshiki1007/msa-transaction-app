from django.http.response import JsonResponse
from .models import *
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import sys

import json

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

#xray_recorder.configure(aws_xray_tracing_name='msa app')
plugins = ('ECSPlugin', 'EC2Plugin')
xray_recorder.configure(plugins=plugins)
patch_all()

def response(status_code, body, error_msg):
	return {
		'statusCode': status_code,
		'body': body,
		'errorMessage': error_msg,
	}

#勘定取引履歴照会
@csrf_exempt
def balance_transaction(request):
	xray_recorder.begin_segment('balance_transaction')
	if request.method != 'POST':
		return JsonResponse(response(400, None, '不正アクセスエラー'))

	params = json.loads(request.body.decode())

	user_id = params['userId']

	wallet = Wallet.objects.get(user_id = user_id)

	xray_recorder.begin_subsegment('get Transaction')
	transaction_objects = Transaction.objects.\
		filter(wallet_id = wallet.wallet_id).\
		select_related('wallet_id').\
		select_related('trading_wallet_id').\
		order_by('transaction_date').\
		reverse()
	xray_recorder.end_subsegment()

	l = list()

	transactions = {}
	transactions['transactions'] = []

	for obj in transaction_objects:
		transactions['transactions'].append(Transaction.to_dict(obj))

	xray_recorder.end_segment()
	return JsonResponse(response(200, transactions, None))