import azure.functions as func
import json

bp_users = func.Blueprint()
@bp_users.route('users', methods=['GET', 'POST'])
@bp_users.generic_input_binding(arg_name="Users", type="sql", CommandText="SELECT * FROM dbo.[User]",
                                ConnectionStringSetting="SqlConnectionString")
@bp_users.generic_output_binding(arg_name="UsersPost", type="sql", CommandText="dbo.[User]",
                                 ConnectionStringSetting="SqlConnectionString")
@bp_users.generic_input_binding(arg_name="Cities", type="sql", CommandText="SELECT * FROM dbo.City",
                                  ConnectionStringSetting="SqlConnectionString")
def user(req: func.HttpRequest, Users: func.SqlRowList, UsersPost: func.Out[func.SqlRow], Cities: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    if method == 'GET':
        # Handle GET request
        return handle_get(Users)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, UsersPost, Cities)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(Users: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling GET request
    # Retrieve users from database
    users = list(map(lambda r: json.loads(r.to_json()), Users))
    return func.HttpResponse(
        body=json.dumps(users),
        mimetype="application/json",
        status_code=200
    )

def handle_post(req: func.HttpRequest, UsersPost: func.Out[func.SqlRow], Cities: func.SqlRowList) -> func.HttpResponse:
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
        if 'Email' not in req_body:
            return func.HttpResponse(
                "Missing required field: Email",
                status_code=400
            )
        if 'Phone' not in req_body:
            return func.HttpResponse(
                "Missing required field: Phone",
                status_code=400
            )
        if 'Address' not in req_body:
            return func.HttpResponse(
                "Missing required field: Address",
                status_code=400
            )
        if 'CityId' not in req_body:
            return func.HttpResponse(
                "Missing required field: CityId",
                status_code=400
            )
        if not any(city['Id'] == req_body['CityId'] for city in Cities):
            return func.HttpResponse(
                "Invalid CityId",
                status_code=400
            )
        # Save the new user to the database
        new_user = UsersPost.set(func.SqlRow(req_body))
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