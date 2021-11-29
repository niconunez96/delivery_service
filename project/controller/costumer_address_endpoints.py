from flask import Blueprint, jsonify, request
from project.costumer_address.application.constumer_address_updater import (
    CostumerAddressInfo,
    CostumerAddressUpdater,
)
from project.costumer_address.application.costumer_address_creator import (
    CostumerAddressAlreadyExists,
    CostumerAddressCreator,
)
from project.costumer_address.application.costumer_address_finder import (
    CostumerAddressFinder,
)
from project.costumer_address.domain.costumer_address_id import CostumerAddressId
from project.costumer_address.infrastructure.costumer_address_mongo_repo import (
    CostumerAddressMongoRepo,
)
from project.shared.domain.errors import EntityNotFound

from .response import INVALID_RESPONSE, NOT_FOUND_RESPONSE, Response

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
        return Response(
            jsonify({"uri": f"/api/costumer_addresses/{costumer_address_id}/"}), 200
        )
    except KeyError:
        return INVALID_RESPONSE("Invalid costumer address data")
    except ValueError:
        return INVALID_RESPONSE("Invalid costumer address id")
    except CostumerAddressAlreadyExists:
        return INVALID_RESPONSE("Costumer address already exists")


@costumer_address.route("/<string:id>/", methods=["PUT"])
def update_costumer_address(id: str):
    updater = CostumerAddressUpdater(repo)
    try:
        costumer_address_id = CostumerAddressId(id)
        updater.update(
            costumer_address_id,
            CostumerAddressInfo.from_dict(request.get_json()),
        )
        return Response(
            jsonify({"uri": f"/api/costumer_addresses/{costumer_address_id}/"}), 200
        )
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
    except KeyError:
        return INVALID_RESPONSE("Invalid costumer address data")
    except ValueError:
        return INVALID_RESPONSE("Invalid costumer address id")


@costumer_address.route("/user/<string:user_id>/", methods=["GET"])
def get_costumer_address(user_id: str):
    finder = CostumerAddressFinder(repo)
    try:
        costumer_address = finder.find_by_user_id(user_id)
        return Response(jsonify(costumer_address), 200)
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
