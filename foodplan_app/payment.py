import json

from yookassa import Payment, Configuration
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt
from yookassa.domain.models.receipt_item import ReceiptItem
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from environs import Env

env = Env()
env.read_env()


def pay(price, phone, email, title, order_number):
    Configuration.account_id = env.int('ACCOUT_ID')
    Configuration.secret_key = env.str('U_KASSA_TOKEN')

    receipt = Receipt()
    receipt.customer = {"phone": phone, "email": email}
    receipt.tax_system_code = 1
    receipt.items = [
        ReceiptItem({
            "description": "Product 1",
            "quantity": 2.0,
            "amount": {
                "value": 250.0,
                "currency": Currency.RUB
            },
            "vat_code": 2
        }),
        {
            "description": "Product 2",
            "quantity": 1.0,
            "amount": {
                "value": 100.0,
                "currency": Currency.RUB
            },
            "vat_code": 2
        }
    ]

    builder = PaymentRequestBuilder()
    builder.set_amount({"value": price, "currency": Currency.RUB}) \
        .set_confirmation({"type": ConfirmationType.REDIRECT, "return_url": "http://195.80.50.84:8000/order/"}) \
        .set_capture(False) \
        .set_description(title) \
        .set_metadata({"orderNumber": order_number}) \
        .set_receipt(receipt)

    request = builder.build()
    # Можно что-то поменять, если нужно
    request.client_ip = '1.2.3.4'
    res = Payment.create(request)
    result = json.loads(res.json())

    return result


def check_pay(pay_id):
    res = Payment.find_one(pay_id)
    print(res)


if __name__ == '__main__':
    Configuration.account_id = env.int('ACCOUT_ID')
    Configuration.secret_key = env.str('U_KASSA_TOKEN')
    check_pay('2cac7e17-000f-5000-a000-1289c1ea9df2')
