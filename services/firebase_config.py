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
        if not firebase_config_str:
            logging.error("FIREBASE_CONFIG environment variable is not set")
        
        logging.info(f"FIREBASE_CONFIG: {firebase_config_str}")
        
        firebase_config = json.loads(firebase_config_str)
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        logging.info("Firebase initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing Firebase: {e}")


def firebase_auth(f):
    @wraps(f)
    def wrapper(req: func.HttpRequest, *args, **kwargs):
        if 'Authorization' not in req.headers:
            return func.HttpResponse(
                body=json.dumps({"error": "Unauthorized"}),
                status_code=403
            )
        try:
            auth_token = req.headers.get('Authorization').split(' ')[1]
            user = auth.verify_id_token(auth_token)
            return f(*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}, 403
    return wrapper