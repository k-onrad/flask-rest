from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True)
    parser.add_argument("store_id", type=int, required=True)

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.to_json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {"message": "Item with name {} already exists".format(name)}, 400

        data = ItemResource.parser.parse_args()
        item = ItemModel(name, **data)
        item.insert()
        return item.to_json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": "Item not found"}, 404
        item.delete()
        return {"message": "Item deleted"}

    def put(self, name):
        data = ItemResource.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)
        item.insert()
        return item.to_json()


class ItemListResource(Resource):
    def get(self):
        return {"items": [item.to_json for item in ItemModel.query.all()]}, 200
