import azure.functions as func
import json
from models import storage
from models.user import User
from models.reservation import Reservation

bp_users = func.Blueprint()
@bp_users.route('users', methods=['GET'])
def user(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return func.HttpResponse(
        body=json.dumps(users),
        mimetype="application/json",
        status_code=200
    )

@bp_users.route('users/{user_id}', methods=['GET'])
def user(req: func.HttpRequest, user_id: str) -> func.HttpResponse:
    user = storage.get(User, user_id)
    if not user:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(user.to_dict()),
        mimetype="application/json",
        status_code=200
    )

@bp_users.route('users/{user_id}', methods=['DELETE'])
def user(req: func.HttpRequest, user_id: str) -> func.HttpResponse:
    user = storage.get(User, user_id)
    if not user:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    storage.delete(user)
    storage.save()
    return func.HttpResponse(
        body=json.dumps({}),
        mimetype="application/json",
        status_code=200
    )

@bp_users.route('users/{user_id}/reservations', methods=['GET'])
def user_reservations(req: func.HttpRequest, user_id: str) -> func.HttpResponse:
    user = storage.get(User, user_id)
    if not user:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    reservations = user.reservations
    reservations = [reservation.to_dict() for reservation in reservations]
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

@bp_users.route('users/{user_id}/reservations/{reservation_id}', methods=['GET'])
def user_reservation(req: func.HttpRequest, user_id: str, reservation_id: str) -> func.HttpResponse:
    user = storage.get(User, user_id)
    if not user:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    reservation = storage.get(Reservation, reservation_id)
    if not reservation:
        return func.HttpResponse(
            "Reservation not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(reservation.to_dict()),
        mimetype="application/json",
        status_code=200
    )