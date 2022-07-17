import json
from bson import ObjectId, json_util
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost/libreria"
app.config['JSON_AS_ASCII'] = False
mongo = PyMongo(app)
CORS(app)

@app.route('/libreria/crear', methods=["POST"])
def add_book():

    image = request.json['image']
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    genero = request.json['genero']

    if (image and title and author and description and genero) and (image.isspace() == False and title.isspace() == False and author.isspace() == False and description.isspace() == False and genero.isspace() == False):
        
        mongo.db.libros.insert_one({
            'title':title,
            'author': author,
            'description': description,
            'image': image,
            'genero': genero,
        })

        response = {
            'title':title,
            'author': author,
            'description': description,
            'image': image,
            'genero': genero,
        }

        return f"Se agrego: {response}"
    else:
        return not_accepted()

@app.route('/libreria', methods = ['GET'])
@cross_origin()
def get_books():
    books = mongo.db.libros.find()

    response = json_util.dumps(books)

    return Response(response, mimetype='application/json')

@app.route('/libreria/<genero>', methods = ['GET'])
@cross_origin()
def get_books_by_genero(genero):

    books = mongo.db.libros.find({"genero" : genero})

    response = json_util.dumps(books)

    return Response(response, mimetype='application/json')

@app.route('/libreria/<id>', methods=['DELETE'])
def delete_book(id):
    mongo.db.libros.delete_one({"_id": ObjectId(id)})

    response = f"{id} was deleted"

    return response

@app.route('/libreria/generos', methods=['GET'])
@cross_origin()
def get_all_generos():
    books = mongo.db.libros.distinct("genero")

    response = json_util.dumps(books)

    return Response(response, mimetype='application/json')

@app.errorhandler(406)
def not_accepted(error=None):

    response = jsonify({
        'message': "I cant add this book because there is a problem",
        'status': 406
    })

    response.status_code = 406

    return response


if __name__ == "__main__":
    app.run(debug = True)