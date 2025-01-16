import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
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


def firebase_auth():
    def middleware(req: func.HttpRequest) -> func.HttpResponse:
        # Extract the Authorization header
        auth_header = req.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return func.HttpResponse(
                "Missing or invalid Authorization header",
                status_code=401
            )
        try:
            # Extract the token and verify it
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
            # If no response is returned, the request proceeds
        except auth.InvalidIdTokenError:
            return func.HttpResponse("Invalid token", status_code=401)
        except auth.ExpiredIdTokenError:
            return func.HttpResponse("Expired token", status_code=401)
        except Exception as e:
            return func.HttpResponse(f"Authentication failed: {str(e)}", status_code=401)
    return middleware