import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

## ROUTES
@app.route("/drinks")
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({"success": True, "drinks": [drink.short() for drink in drinks]})


@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    return jsonify({"success": True, "drinks": [drink.long() for drink in drinks]})


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    body = request.get_json()

    try:
        title = body.get("title")
        recipe = body.get("recipe")

        if (title is None) or (recipe is None):
            abort(400)

        if type(recipe) != list:
            recipe = [recipe]

        drink = Drink(title=title, recipe=json.dumps(recipe))

        drink.insert()

        return jsonify({"success": True, "drinks": [drink.long()]})
    except:
        abort(400)


@app.route("/drinks/<int:drink_id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(payload, drink_id):
    body = request.get_json()
    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404)

    try:
        title = body.get("title")
        recipe = body.get("recipe")

        if title:
            drink.title = title

        if type(recipe) != list and recipe:
            recipe = [recipe]
            drink.recipe = json.dumps(recipe)

        drink.update()

        return jsonify({"success": True, "drinks": [drink.long()]})
    except:
        print(sys.exc_info())
        abort(400)


@app.route("/drinks/<int:drink_id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, drink_id):
    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404)

    try:
        drink.delete()

        return jsonify({"success": True, "delete": drink.id})
    except:
        abort(400)


## Error Handling


@app.errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error["description"],
            }
        ),
        error.status_code,
    )


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400


@app.errorhandler(401)
def not_found(error):
    return (
        jsonify({"success": False, "error": 401, "message": "Unauthorized"}),
        401,
    )


@app.errorhandler(403)
def forbidden(error):
    return (
        jsonify({"success": False, "error": 403, "message": "Forbidden"}),
        403,
    )


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422


@app.errorhandler(500)
def internal_server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
        500,
    )
