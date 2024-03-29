import azure.functions as func
import json

bp_reviews = func.Blueprint()
@bp_reviews.route('reviews', methods=['GET', 'POST'])
@bp_reviews.generic_input_binding(arg_name="Reviews", type="sql", CommandText="SELECT * FROM dbo.Review",
                                  ConnectionStringSetting="SqlConnectionString")
@bp_reviews.generic_output_binding(arg_name="ReviewsPost", type="sql", CommandText="dbo.Review",
                                   ConnectionStringSetting="SqlConnectionString")
@bp_reviews.generic_input_binding(arg_name="Reservations", type="sql", CommandText="SELECT * FROM dbo.Reservation",
                                  ConnectionStringSetting="SqlConnectionString")                           
def review(req: func.HttpRequest, Reviews: func.SqlRowList, ReviewsPost: func.Out[func.SqlRow], Reservations: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(Reviews)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, ReviewsPost, Reservations)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(Reviews: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve reviews from database
    reviews = list(map(lambda r: json.loads(r.to_json()), Reviews))
    return func.HttpResponse(
        body=json.dumps(reviews),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, ReviewsPost: func.Out[func.SqlRow], Reservations: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'RerservationID' not in req_body:
            return func.HttpResponse(
                "Missing required field: ReservationID",
                status_code=400
            )
        if 'Rating' not in req_body:
            return func.HttpResponse(
                "Missing required field: Rating",
                status_code=400
            )
        if 'Comment' not in req_body:
            return func.HttpResponse(
                "Missing required field: Comment",
                status_code=400
            )
        if 'Date' not in req_body:
            return func.HttpResponse(
                "Missing required field: Date",
                status_code=400
            )
        if not any(reservation['ReservationID'] == req_body['ReservationID'] for reservation in Reservations):
            return func.HttpResponse(
                "Invalid ReservationID",
                status_code=400
            )
        # Save the new review to the database
        new_review = ReviewsPost.set(func.SqlRow(req_body))
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