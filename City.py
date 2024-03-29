import azure.functions as func
import json

bp_cities = func.Blueprint()
@bp_cities.route('cities', methods=['GET', 'POST'])
@bp_cities.generic_input_binding(arg_name="Cities", type="sql", CommandText="SELECT * FROM dbo.City",
                                 ConnectionStringSetting="SqlConnectionString")
@bp_cities.generic_output_binding(arg_name="CitiesPost", type="sql", CommandText="dbo.City",
                                  ConnectionStringSetting="SqlConnectionString")
def city(req: func.HttpRequest, Cities: func.SqlRowList, CitiesPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(req, Cities)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, CitiesPost)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(req: func.HttpRequest, Cities: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve cities from database
    cities = list(map(lambda r: json.loads(r.to_json()), Cities))
    return func.HttpResponse(
        body=json.dumps(cities),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, CitiesPost: func.Out[func.SqlRow]) -> func.HttpResponse:
    # Logic for handling POST request
    # Parse the request body
    try:
        req_body = req.get_json()
        # Validate and process the request body
        if 'Name' not in req_body:
            return func.HttpResponse(
                "Missing required field: Name",
                status_code=400
            )
        # Insert the city into the database
        new_city = CitiesPost.set(func.SqlRow(req_body))
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