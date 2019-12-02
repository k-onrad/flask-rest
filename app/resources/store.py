from flask_restful import Resource
from models.store import StoreModel


class StoreResource(Resource):
    def get(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if store:
            return store.to_json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if store:
            return {"message": "Store already exists"}, 400
        try:
            store = StoreModel(name=name)
            store.insert()
            return store.to_json()
        except Exception:
            return {"message": "Internal error ocurred while creating store"}, 500

    def delete(self, name):
        store = StoreModel.query.filter_by(name=name).first()
        if store is None:
            return {"message": "Store not found"}, 404
        try:
            store.delete()
            return {"message": "Store deleted."}
        except Exception:
            return {"message": "Internal error ocurred while deleting store"}, 500


class StoreListResource(Resource):
    def get(self):
        return {"stores": [store.to_json() for store in StoreModel.query.all()]}
