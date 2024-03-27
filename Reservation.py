import azure.functions as func
import json

bp_reservations = func.Blueprint()
@bp_reservations.route('reservations', methods=['GET', 'POST'])
@bp_reservations.generic_input_binding(arg_name="Reservations", type="sql", CommandText="SELECT * FROM dbo.Reservation",
                                       ConnectionStringSetting="SqlConnectionString")
def reservation(req: func.HttpRequest, Reservations: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Reservations)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(req: func.HttpRequest, Reservations: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve reservations from database or any other data source
    reservations = list(map(lambda r: json.loads(r.to_json()), Reservations))
    return func.HttpResponse(
        body=json.dumps(reservations),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        # Save the new reservation to the database or any other data source
        new_reservation = {"id": 4, "name": "Reservation 4"}
        return func.HttpResponse(
            body=json.dumps(new_reservation),
            mimetype="application/json",
            status_code=201
        )
    except ValueError:
        return func.HttpResponse(
            "Invalid request body",
            status_code=400
        )
    