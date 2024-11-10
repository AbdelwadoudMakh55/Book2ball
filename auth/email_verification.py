import azure.functions as func
import requests
from crud.user import *
import json


bp_auth = func.Blueprint()


@bp_auth.route('verify-email', methods=['GET'])
def email_verification(req: func.HttpRequest) -> func.HttpResponse:
    try:
        oob_code = req.params.get('oobCode')
        if not oob_code:
            return func.HttpResponse(
                json.dumps({"error": "Missing oobCode"}),
                mimetype="application/json",
                status_code=400
            )

        with open('local.settings.json') as f:
            settings = json.load(f)
        api_key = settings.get('Values').get('FIREBASE_API_KEY')
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:update?key={api_key}'
        payload = {
            'oobCode': oob_code
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return func.HttpResponse(
                json.dumps({"error": response.json()}),
                mimetype="application/json",
                status_code=response.status_code
            )

        email = response.json().get('email')
        user = get_user_by_email(email)
        user_id = user.id
        update_user(user_id, is_verified=True)
        return func.HttpResponse(
            json.dumps({"message": "Email verified and user updated in database"}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=400
        )