import azure.functions as func
import json

bp_reviews = func.Blueprint()
@bp_reviews.route('reviews', methods=['GET', 'POST'])
@bp_reviews.generic_input_binding(arg_name="Reviews", type="sql", CommandText="SELECT * FROM dbo.Review",
                                  ConnectionStringSetting="SqlConnectionString")
@bp_reviews.generic_output_binding(arg_name="ReviewsPost", type="sql", CommandText="dbo.Review",
                                   ConnectionStringSetting="SqlConnectionString")                           
def review(req: func.HttpRequest, Reviews: func.SqlRowList, ReviewsPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Reviews)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, ReviewsPost)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(req: func.HttpRequest, Reviews: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve reviews from database
    reviews = list(map(lambda r: json.loads(r.to_json()), Reviews))
    return func.HttpResponse(
        body=json.dumps(reviews),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, ReviewsPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
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