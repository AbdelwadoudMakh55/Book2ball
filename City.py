import azure.functions as func
import json
import os
import pyodbc

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
        return handle_get(Cities)
    elif method == 'POST':
        # Handle POST request
        return handle_post(req, CitiesPost)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )
    
def handle_get(Cities: func.SqlRowList) -> func.HttpResponse:
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
    
@bp_cities.route('cities/{city_id}', methods=['GET', 'DELETE'])
@bp_cities.generic_input_binding(arg_name="Cities", type="sql", CommandText="SELECT * FROM dbo.City",
                                 ConnectionStringSetting="SqlConnectionString")
def city_by_id(req: func.HttpRequest, Cities: func.SqlRowList) -> func.HttpResponse:
    method = req.method
    city_id = req.route_params.get('city_id')
    cities = list(map(lambda r: json.loads(r.to_json()), Cities))
    city = list(city for city in cities if city['CityID'] == city_id)
    if len(city) == 0:
        return func.HttpResponse(
            "City not found",
            status_code=404
        )
    if method == 'GET':
        # Handle GET request
        return func.HttpResponse(
            body=json.dumps(city),
            mimetype="application/json",
            status_code=200
        )
    elif method == 'DELETE':
        # Handle DELETE request
        return handle_delete(city_id, Cities)
    else:
        return func.HttpResponse(
            "Method not allowed",
            status_code=405
        )

def handle_delete(city_id: str, Cities: func.SqlRowList) -> func.HttpResponse:
    # Logic for handling DELETE request
    # Delete the city from the database
    conn_str = os.getenv("ODBCConnectionString")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.City WHERE CityID = ?", city_id)
    conn.commit()
    return func.HttpResponse(
        "City deleted successfully",
        status_code=200
    )
