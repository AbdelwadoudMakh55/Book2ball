import azure.functions as func
import logging
from routers.Pitch import bp_pitches
from routers.Reservation import bp_reservations
from routers.User import bp_users
from routers.Review import bp_reviews
from routers.PitchOwner import bp_pitch_owners
from routers.City import bp_cities
from services.time_trigger_reservations import bp_time_trigger
from routers.auth.email_verification import bp_auth
from models.database import create_database_tables, engine
from services.firebase_config import firebase_config


# firebase_config()
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


app.register_blueprint(bp_pitches)
app.register_blueprint(bp_reservations)
app.register_blueprint(bp_users)
app.register_blueprint(bp_reviews)
app.register_blueprint(bp_pitch_owners)
app.register_blueprint(bp_cities)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_time_trigger)

create_database_tables(engine)

@app.function_name("book2ball")
@app.route(route="status")
def API(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        "API is running",
        status_code=200
    )