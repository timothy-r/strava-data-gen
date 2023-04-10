from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route("/activity", methods=['POST'])
def update():
    # get a new activity
#     Example request for a new activity
# {
#     "aspect_type": "update",
#     "event_time": 1516126040,
#     "object_id": 1360128428,
#     "object_type": "activity",
#     "owner_id": 134815,
#     "subscription_id": 120475,
#     "updates": {
#         "title": "Messy"
#     }
# }
    pass
    # return jsonify(message='Hello from root!')

@app.route("/activity", methods=['GET'])
def subscribe():
    # Example request to confirm subscription
    # GET https://mycallbackurl.com?hub.verify_token=STRAVA&hub.challenge=15f7d1a91c1f40f8a748fd134752feb3&hub.mode=subscribe

    pass
    # return jsonify(message='Hello from root!')


@app.route("/populate")
def hello():
    # get all activities
    pass
    # return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found'), 404)