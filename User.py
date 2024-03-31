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

@bp_users.route('users/{user_id}', methods=['GET', 'DELETE'])
def user_by_id(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    user_id = req.route_params.get('user_id')
    user = storage.get(User, user_id)
    if not user:
        return func.HttpResponse(
            "User not found",
            status_code=404
        )
    if method == 'GET':
        return func.HttpResponse(
            body=json.dumps(user.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    storage.delete(user)
    storage.save()
    return func.HttpResponse(
        "User deleted successfully",
        status_code=200
    )


@bp_users.route('users/{user_id}/reservations', methods=['GET'])
def user_reservations(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')
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
def user_reservation(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')
    reservation_id = req.route_params.get('reservation_id')
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