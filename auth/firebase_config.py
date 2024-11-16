import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from functools import wraps
import azure.functions as func
import json

def firebase_config():
    cred = credentials.Certificate("book2ball-6687d-firebase-adminsdk-xmhqo-728c024f44.json")
    firebase_admin.initialize_app(cred)


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