import azure.functions as func
import json
from crud.review import *
from services.firebase_config import firebase_auth


bp_reviews = func.Blueprint()
@bp_reviews.route('reviews', methods=['GET'])
@firebase_auth
def reviews(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling GET request
    reviews = get_all_reviews()
    reviews = [review.to_dict() for review in reviews]
    return func.HttpResponse(
        body=json.dumps(reviews),
        mimetype="application/json",
        status_code=200
    )

@bp_reviews.route('reviews/{review_id}', methods=['GET'])
@firebase_auth
def review(req: func.HttpRequest) -> func.HttpResponse:
    review_id = req.route_params.get('review_id')
    # Logic for handling GET request
    review = get_review_by_id(review_id)
    if not review:
        return func.HttpResponse(
            "Review not found",
            status_code=404
        )
    return func.HttpResponse(
        body=json.dumps(review.to_dict()),
        mimetype="application/json",
        status_code=200
    )
    