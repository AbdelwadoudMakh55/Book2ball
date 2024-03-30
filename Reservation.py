import azure.functions as func
import json
from models import storage
from models.reservation import Reservation

bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET'])
def reservation(req: func.HttpRequest) -> func.HttpResponse:
    method = req.method
    reservations = storage.all(Reservation).values()
    reservations = [reservation.to_dict() for reservation in reservations]
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

@bp_reservations.route('reservations/{reservation_id}', methods=['GET'])
def reservation(req: func.HttpRequest, reservation_id: str) -> func.HttpResponse:
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
    