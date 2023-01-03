import threading
from flask import Flask, request# request put için
from flask_restful import Api, Resource, abort, reqparse #reqparse request yerine kullanılacak
from getJson2 import start_threading
from learningModels.convlstm2d import predict


app = Flask(__name__)
api = Api(app)

mac_put_args = reqparse.RequestParser() #Request yerine.//verdiğimiz kurallara göre veriyi kabul eder veya etmez.
mac_put_args.add_argument("mac", type=str, help="Sadece mac girebilirsin", required = True)



Macs = {}

def abort_if_mac_doesnt_exist(mac):
    if mac not in Macs:
        abort(404, message = "mac is not valid")

def abort_if_mac_exist(mac):
    if mac in Macs:
        abort(409, message = "mac already eist with that id")


class Mac(Resource):
    
    def get(self, mac):
        predicts = predict()
        return predicts
    
    def put(self, mac):
        abort_if_mac_exist(mac)
        args = mac_put_args.parse_args()
        Macs[mac] = args
        return Macs[mac], 201

    def delete(self, mac):
        abort_if_mac_doesnt_exist(mac)
        del Macs[mac]
        return "", 204

    def post(self, mac):
        args = mac_put_args.parse_args()  
        Macs[mac] = args
        t = threading.Thread(target = start_threading(Macs[mac]), args = (Macs[mac], ))
        t.start()

        predicts = predict()

        return predicts, 200 

api.add_resource(Mac, "/mac/<string:mac>")

if __name__ == "__main__":
    app.run(debug = True)

    """
      ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    args= vars(ap.parse_args())
    
    app.run(host=args["ip"], port=args["port"], debug=True)
    
    """