from flask import Flask, request ,jsonify

app = Flask(__name__)
#app.config["DEBUG"] =True

@app.route('/', methods=["GET"])
def application():
	return "Hello world!"

app.run()