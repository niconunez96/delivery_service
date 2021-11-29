from flask import Blueprint, jsonify, request
from project.costumer_address.application.constumer_address_updater import (
    CostumerAddressInfo, CostumerAddressUpdater)
from project.costumer_address.application.costumer_address_creator import (
    CostumerAddressAlreadyExists, CostumerAddressCreator)
from project.costumer_address.application.costumer_address_finder import \
    CostumerAddressFinder
from project.costumer_address.domain.costumer_address_id import \
    CostumerAddressId
from project.costumer_address.infrastructure.costumer_address_mongo_repo import \
    CostumerAddressMongoRepo  # noqa
from project.shared.errors import EntityNotFound

from .response import NOT_FOUND_RESPONSE, Response

costumer_address = Blueprint(
    "costumer_address", __name__, url_prefix="/api/costumer_addresses"
)


repo = CostumerAddressMongoRepo()


@costumer_address.route("/", methods=["POST"])
def create_costumer_address():
    creator = CostumerAddressCreator(repo)
    try:
        costumer_address_id = CostumerAddressId()
        creator.create(
            costumer_address_id,
            CostumerAddressInfo.from_dict(request.get_json()),
        )
        return Response(jsonify("Success"), 200)
    except KeyError:
        return Response(jsonify("Invalid costumer address data"), 400)
    except ValueError:
        return Response(jsonify("Invalid costumer address id"), 400)
    except CostumerAddressAlreadyExists:
        return Response(jsonify("Costumer address already exists"), 400)


@costumer_address.route("/<string:id>/", methods=["PUT"])
def update_costumer_address(id: str):
    updater = CostumerAddressUpdater(repo)
    try:
        costumer_address_id = CostumerAddressId(id)
        updater.update(
            costumer_address_id,
            CostumerAddressInfo.from_dict(request.get_json()),
        )
        return Response(jsonify("Success"), 200)
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
    except KeyError:
        return Response(jsonify("Invalid costumer address data"), 400)
    except ValueError:
        return Response(jsonify("Invalid costumer address id"), 400)


@costumer_address.route("/user/<string:user_id>/", methods=["GET"])
def get_costumer_address(user_id: str):
    finder = CostumerAddressFinder(repo)
    try:
        costumer_address = finder.find_by_user_id(user_id)
        return Response(jsonify(costumer_address), 200)
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
