# system
from uuid import uuid1
from PIL import Image

# 3rd parties
from flask_restful import Resource, Api
from flask import jsonify, request

# project
from core.server import ClassifierServer


server = ClassifierServer()
app = server.create()
api = Api(app)


class Classifier(Resource):
    def get(self):
        return jsonify(status='OK')

    def post(self):
        uid = uuid1()

        try:
            server.log(f"{uid} -> {request.method} on '{request.path}' "
                       f"from {request.remote_addr}, "
                       f"size={request.content_length}")

            image = request.files["img"]
            image = Image.open(image)
            result = server.process(uid, image)

            server.log(f"{uid} -> OK")

            return jsonify(status="OK",
                           result=result)
        except Exception as ex:
            server.log(f"{uid} -> ERROR\n{str(ex)}")
            return jsonify(status="ERROR")


api.add_resource(Classifier, '/classify')


if __name__ == "__main__":
    server.run()
