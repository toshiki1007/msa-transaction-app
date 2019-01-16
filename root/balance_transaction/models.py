from django.db import models
from django.forms.models import model_to_dict

class Wallet(models.Model):
	class Meta:
		managed = False
		db_table = 'balance_wallet'

	wallet_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=10)
	balance = models.IntegerField(default=3000)

	def __str__(self):
		return str(self.wallet_id)

	def to_dict(self):
		return model_to_dict(self)

class Transaction(models.Model):
	class Meta:
		unique_together = (('wallet_id', 'serial_number'),)
		managed = False
		db_table = 'balance_transaction'

	transaction_id = models.AutoField(primary_key=True)
	wallet_id = models.ForeignKey('Wallet', related_name='r_wallet', on_delete=models.CASCADE)
	serial_number = models.IntegerField(
            default=0,
            blank=False,
            null=False
		)
	trading_wallet_id = models.ForeignKey('Wallet', related_name='r_trading_wallet', on_delete=models.CASCADE)
	transaction_type = models.ForeignKey('TransactionType', related_name='r_transaction_type', on_delete=models.CASCADE)
	transaction_amount = models.IntegerField(default=0)
	transaction_date = models.DateTimeField(
            auto_now=True,
            blank=False,
            null=False
		)

	def __str__(self):
		return str(self.wallet_id) + ' : ' + str(self.serial_number)

	def to_dict(self):
		return {
			'transactionId': self.transaction_id,
			'serialNumber': self.serial_number,
			'transactionAmount': self.transaction_amount,
			'transactionDate': '{0:%Y-%m-%d %H:%M:%S}'.format(self.transaction_date),
			'transactionType': self.transaction_type.type_name,
			'tradingWalletId': self.trading_wallet_id.wallet_id,
			'tradingUserId': self.trading_wallet_id.user_id,
			'walletId': self.wallet_id.wallet_id,
		}

class TransactionType(models.Model):
	class Meta:
		managed = False
		db_table = 'balance_transactiontype'

	type_name = models.CharField(max_length=2)

	def __str__(self):
		return str(self.type_name)

	def to_dict(self):
		return model_to_dict(self)