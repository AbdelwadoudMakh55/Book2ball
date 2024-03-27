import azure.functions as func
import json

bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET', 'POST'])
@bp_reservations.generic_input_binding(arg_name="Reservations", type="sql", CommandText="SELECT * FROM dbo.Reservation",
                                       ConnectionStringSetting="SqlConnectionString")
@bp_reservations.generic_output_binding(arg_name="ReservationsPost", type="sql", CommandText="dbo.Reservation",
                                        ConnectionStringSetting="SqlConnectionString")
def reservation(req: func.HttpRequest, Reservations: func.SqlRowList, ReservationsPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Reservations)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, ReservationsPost)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(req: func.HttpRequest, Reservations: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve reservations from database
    reservations = list(map(lambda r: json.loads(r.to_json()), Reservations))
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, ReservationsPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        # Save the new reservation to the database
        new_reservation = ReservationsPost.set(func.SqlRow(req_body))
        return func.HttpResponse(
            body=json.dumps(req_body),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
    