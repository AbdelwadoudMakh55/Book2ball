import azure.functions as func
import logging
from routers.Pitch import bp_pitches
from routers.Reservation import bp_reservations
from routers.User import bp_users
from routers.Review import bp_reviews
from routers.PitchOwner import bp_pitch_owners
from routers.City import bp_cities
from auth.email_verification import bp_auth
from auth.firebase_config import firebase_config
from models.database import create_database_tables, engine


app = func.FunctionApp()
app.register_blueprint(bp_pitches)
app.register_blueprint(bp_reservations)
app.register_blueprint(bp_users)
app.register_blueprint(bp_reviews)
app.register_blueprint(bp_pitch_owners)
app.register_blueprint(bp_cities)
app.register_blueprint(bp_auth)


create_database_tables(engine)
firebase_config()

@app.route(route="status", auth_level=func.AuthLevel.ANONYMOUS)
def API(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        "API is running",
        status_code=200
    )