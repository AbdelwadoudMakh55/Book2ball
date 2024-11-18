import azure.functions as func
import requests
from crud.user import *
from crud.reservation import *
from models.reservation import Status
import json
import os


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

        api_key = os.environ['FIREBASE_API_KEY']
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
        
        
@bp_auth.route('verify-reservation', methods=['GET'])
def verify_reservation(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get('user_id')
    reservation_id = req.params.get('reservation_id')
    
    if not user_id or not reservation_id:
        return func.HttpResponse(
            "Missing required query parameters: user_id and reservation_id",
            status_code=400
        )
    reservation = get_reservation_by_id(reservation_id)
    if not reservation or reservation.user_id != user_id:
        return func.HttpResponse(
            "Reservation not found",
            status_code=404
        )
    update_reservation(reservation.id, status=Status.CONFIRMED)
    return func.HttpResponse(
        "Reservation verified successfully",
        status_code=200
    )