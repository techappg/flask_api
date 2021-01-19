from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from requests.auth import HTTPBasicAuth
import requests
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Safaricom API',
    description='List of safaricom apis',
)

name_space = api.namespace('api', description='v1 Apis')


class Index(Resource):
    def get(self):
        return {
            "page": "index page"
        }

@name_space.route("/token")
class GetToken(Resource):
    def get(self):
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        payload = {}


        auth = HTTPBasicAuth(
            "rSyOG6LPmjVM3PrrI1qlNDnOkAGOVipE", "2eKoVSm1yHBkqrGh")

        response = requests.request(
            "GET", url, auth=auth, data=payload)

        return json.loads(response.text)

@name_space.route("/b2c-payment")
class B2CPayment(Resource):
    def get(self):
        token = GetToken().get()
        print("token : ", token.get("access_token"))
        url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

        payload = {
            "InitiatorName": "apiop37",
            "SecurityCredential": "bgTn7e054OhXe6zoP5pUhKRjrnZ69AWgVnhjU7n5SPU9loNw7vGgGqB5X0TZN6LzQGpSIDFsCHOh6CzsCdcnzj1AlDouzqydU1xBaH1z+ak1BZKq7LsHc69r+qtyZ/VAxOS+PQRBUVBXUAtPQRMTzeDq3q87TIRpzZdqA8eJYL3QpfoD4Rteg4iYH4+iMgR7AVTDuYQgLpQNx6SQSIZVFKI5RqeaHH/FMdjbqaJ6mCuT2EC6XlcBu49RWSHtLP3Y5oScwmuFXV8oQp+1bz5NXm/llJvQsL6npmRyzXB69S3TZZnUNHk4OsJkZ9cfpWAaGdrrt8uqIn9o2SNIR0mZnQ==",
            "CommandID": "BusinessPayment",
            "Amount": "100",
            "PartyA": "603021",
            "PartyB": "254708374149",
            "Remarks": "Testing Request",
            "QueueTimeOutURL": "https://webhook.site/20d56f33-eafa-4ca8-8084-17e749e09d5d",
            "ResultURL": "https://webhook.site/20d56f33-eafa-4ca8-8084-17e749e09d5d"
        }
        headers = {
            'Authorization': f'Bearer {token.get("access_token")}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

@name_space.route("/transaction-status")
class MpaisaTransactionStatus(Resource):
    def get(self):
        token = GetToken().get()
        print("token : ", token.get("access_token"))
        url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"

        payload = {
            "Initiator": "apiop37",
            "SecurityCredential": "bgTn7e054OhXe6zoP5pUhKRjrnZ69AWgVnhjU7n5SPU9loNw7vGgGqB5X0TZN6LzQGpSIDFsCHOh6CzsCdcnzj1AlDouzqydU1xBaH1z+ak1BZKq7LsHc69r+qtyZ/VAxOS+PQRBUVBXUAtPQRMTzeDq3q87TIRpzZdqA8eJYL3QpfoD4Rteg4iYH4+iMgR7AVTDuYQgLpQNx6SQSIZVFKI5RqeaHH/FMdjbqaJ6mCuT2EC6XlcBu49RWSHtLP3Y5oScwmuFXV8oQp+1bz5NXm/llJvQsL6npmRyzXB69S3TZZnUNHk4OsJkZ9cfpWAaGdrrt8uqIn9o2SNIR0mZnQ==",
            "CommandID": "TransactionStatusQuery",
            "TransactionID": "PA671HI7SL",
            "PartyA": "603021",
            "IdentifierType": "4",
            "ResultURL": "https://webhook.site/20d56f33-eafa-4ca8-8084-17e749e09d5d",
            "QueueTimeOutURL": "https://webhook.site/20d56f33-eafa-4ca8-8084-17e749e09d5d",
            "Remarks": "test"
        }
        headers = {
            'Authorization': f'Bearer {token.get("access_token")}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

@name_space.route("/c2b-stimulate")
class C2BStimulate(Resource):
    def get(self):
        token = GetToken().get()
        print("token : ", token.get("access_token"))
        url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

        payload = {
            "ShortCode":"603021",
            "CommandID":"CustomerPayBillOnline",
            "Amount":"100",
            "Msisdn":"254708374149",
            "BillRefNumber":"Ref23453234"
        }
        headers = {
            'Authorization': f'Bearer {token.get("access_token")}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

@name_space.route("/c2b-register-url")
class C2BRegisterUrl(Resource):
    def get(self):
        token = GetToken().get()
        print("token : ", token.get("access_token"))
        url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"

        payload = {
            "ShortCode": "603021",
            "ResponseType": "CustomerPayBillOnline",
            "ConfirmationURL": "https://webhook.site/2119d78f-8cad-4718-b9d4-3b91bb1f5df7",
            "ValidationURL": "https://webhook.site/2119d78f-8cad-4718-b9d4-3b91bb1f5df7"
        }
        headers = {
            'Authorization': f'Bearer {token.get("access_token")}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return json.loads(response.text)

if __name__ == '__main__':
    app.run(debug=True)