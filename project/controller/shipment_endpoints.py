from flask import Blueprint, jsonify, request
from project.controller.response import NOT_FOUND_RESPONSE, Response
from project.shared.errors import EntityNotFound
from project.shared.rabbitmq_event_bus import RabbitMQEventBus
from project.shipment.application.shipment_deliver import (
    InvalidShipmentStatusToDeliver, ShipmentDeliver)
from project.shipment.application.shipment_finder import ShipmentFinder
from project.shipment.application.shipment_location_updater import (
    InvalidShipmentStatus, ShipmentLocationInfo, ShipmentLocationUpdater)
from project.shipment.application.shipment_starter import (ShipmentInfo,
                                                           ShipmentStarter)
from project.shipment.application.shipment_trip_resolver import \
    ShipmentTripResolver
from project.shipment.domain.shipment import ShipmentId
from project.shipment.infrastructure.shipment_event_mongo_store import \
    ShipmentEventMongoStore
from project.shipment.infrastructure.shipment_mongo_repo import \
    ShipmentMongoRepo

delivery = Blueprint("delivery", __name__, url_prefix="/api/deliveries")


repo = ShipmentMongoRepo()
event_store = ShipmentEventMongoStore()
event_bus = RabbitMQEventBus()


@delivery.route("/", methods=["POST"])
def start_shipment_test():
    shipment_id = ShipmentId()
    shipment_starter = ShipmentStarter(repo, event_bus)
    shipment_starter.start_shipment(shipment_id, ShipmentInfo("1", "1"))
    return Response(jsonify("Success"), 200)


# @delivery.route("/<string:shipment_id>/", methods=['GET'])
# def find_by_id(shipment_id: str):
#     finder = ShipmentFinder(repo)
#     try:
#         id = ShipmentId.from_string(shipment_id)
#         return Response(jsonify(finder.find(id)), 200)
#     except ValueError:
#         return Response(jsonify({"error": "Invalid shipment id"}), 400)
#     except EntityNotFound:
#         return NOT_FOUND_RESPONSE


@delivery.route("/<string:shipment_id>/move/", methods=['POST'])
def update_shipment_location(shipment_id: str):
    shipment_location_updater = ShipmentLocationUpdater(repo, event_bus)
    try:
        id = ShipmentId.from_string(shipment_id)
        new_location = ShipmentLocationInfo.from_dict(request.get_json())
        shipment_location_updater.move_shipment(id, new_location)
        return Response(jsonify("Success"), 200)
    except ValueError:
        return Response(jsonify({"error": "Invalid shipment id"}), 400)
    except KeyError:
        return Response(jsonify({"error": "Invalid location"}), 400)
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
    except InvalidShipmentStatus:
        return Response(jsonify({"error": "Invalid shipment status"}), 400)


@delivery.route("/<string:shipment_id>/deliver/", methods=['POST'])
def deliver_shipment(shipment_id: str):
    shipment_deliver = ShipmentDeliver(repo, event_bus)
    try:
        id = ShipmentId.from_string(shipment_id)
        shipment_deliver.deliver(id)
        return Response(jsonify("Success"), 200)
    except ValueError:
        return Response(jsonify({"error": "Invalid shipment id"}), 400)
    except EntityNotFound:
        return NOT_FOUND_RESPONSE
    except InvalidShipmentStatusToDeliver:
        return Response(jsonify({"error": "Invalid shipment status"}), 400)


@delivery.route("/<string:shipment_id>/", methods=['GET'])
def get_shipment_trip(shipment_id: str):
    trip_resolver = ShipmentTripResolver(event_store)
    trip = trip_resolver.execute(shipment_id)
    return Response(jsonify(trip), 200)