import os
import tempfile
from flask_restful import Api
from flask import Flask,jsonify,request
from Route.routes import initialize_routes
from config import initialize_db_test
import pytest

app=Flask(__name__)
api = Api(app)
initialize_db_test(app)
initialize_routes(api)

# @pytest.fixture
# def client():
#     pass

def test_1(self):
    client=app.test_client()
    url =  ''
    response = client.post(url,json=
        {
	
})
    response=response.get_json()
    assert response['statusCode']==201

def test_2(self):
    client=app.test_client()
    url =  '/'
    response = client.get(url)
    response=response.get_json()
    assert response['statusCode']==200

def test_3(self):
    client=app.test_client()
    url =  '/'
    response = client.get(url)
    response=response.get_json()
    assert response['statusCode']==200



