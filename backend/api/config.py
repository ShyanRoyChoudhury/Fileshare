# import firebase_admin
# from firebase_admin import credentials
# import os
# print("path",os.getcwd())

# service_account_path = os.path.abspath("./api/service-account.json")
# cred = credentials.Certificate(service_account_path)

# firebase_admin.initialize_app(cred)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth  # Add this import
import os

print("path", os.getcwd())
service_account_path = os.path.abspath("./api/service-account.json")
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)