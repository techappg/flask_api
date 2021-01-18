from flask import Flask
from flask_restful import Resource, Api
from requests.auth import HTTPBasicAuth
import requests
import json

app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return {
            "page": "index page"
        }

class GetToken(Resource):
    def get(self):
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        payload = {}


        auth = HTTPBasicAuth(
            "rSyOG6LPmjVM3PrrI1qlNDnOkAGOVipE", "2eKoVSm1yHBkqrGh")

        response = requests.request(
            "GET", url, auth=auth, data=payload)

        return json.loads(response.text)


class B2CPayment(Resource):
    def get(self):
        token = GetToken().get()
        print("token : ", token.get("access_token"))
        url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"

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

api.add_resource(Index, '/')
api.add_resource(GetToken, '/token')
api.add_resource(B2CPayment, '/b2c-payment')

if __name__ == '__main__':
    app.run(debug=True)