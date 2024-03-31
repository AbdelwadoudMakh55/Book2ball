import azure.functions as func
import json
from models import storage
from models.review import Review

bp_reviews = func.Blueprint()
@bp_reviews.route('reviews', methods=['GET'])                     
def reviews(req: func.HttpRequest) -> func.HttpResponse:
    # Logic for handling GET request
    reviews = storage.all(Review).values()
    reviews = [review.to_dict() for review in reviews]
    return func.HttpResponse(
        body=json.dumps(reviews),
        mimetype="application/json",
        status_code=200
    )

@bp_reviews.route('reviews/{review_id}', methods=['GET'])
def review(req: func.HttpRequest) -> func.HttpResponse:
    review_id = req.route_params.get('review_id')
    # Logic for handling GET request
    review = storage.get(Review, review_id)
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
    