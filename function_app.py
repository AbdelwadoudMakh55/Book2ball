import azure.functions as func
import datetime
import json
import logging
from Pitch import bp_pitches
from Reservation import bp_reservations
from User import bp_users
from Review import bp_reviews
from PitchOwner import bp_pitch_owners
from City import bp_cities
app = func.FunctionApp()

app.register_blueprint(bp_pitches)
app.register_blueprint(bp_reservations)
app.register_blueprint(bp_users)
app.register_blueprint(bp_reviews)
app.register_blueprint(bp_pitch_owners)
app.register_blueprint(bp_cities)

@app.route(route="status", auth_level=func.AuthLevel.ANONYMOUS)
def API(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        "API is running",
        status_code=200
    )

