import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from functools import wraps
import azure.functions as func
import os
import json
import logging


def firebase_config():
    try:
        firebase_config_str = os.getenv("FIREBASE_CONFIG")
        firebase_config = json.loads(firebase_config_str)
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        logging.error(f"Error initializing Firebase: {str(e)}")

def firebase_auth(f) -> func.HttpResponse:
    @wraps(f)
    def wrapper(req: func.HttpRequest, *args, **kwargs):
        auth_header = req.headers.get('Authorization')
        if not auth_header:
            return func.HttpResponse(
                body=json.dumps({"error": "Authorization header is missing"}),
                mimetype="application/json",
                status_code=401
            )
        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
        except auth.InvalidIdTokenError:
            return func.HttpResponse(
                body=json.dumps({"error": "Invalid token"}),
                mimetype="application/json",
                status_code=401
            )
        except auth.ExpiredIdTokenError:
            return func.HttpResponse(
                body=json.dumps({"error": "Token expired"}),
                mimetype="application/json",
                status_code=401
            )
        except Exception as e:
            return func.HttpResponse(
                body=json.dumps({"error": str(e)}),
                mimetype="application/json",
                status_code=401
            )
        return f(req, *args, **kwargs)
    return wrapper