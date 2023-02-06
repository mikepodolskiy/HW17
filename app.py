# app.py
import json

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


api = Api(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            director_movies = Movie.query.filter(Movie.director_id == director_id)
            return movies_schema.dump(director_movies), 200
        if genre_id:
            genre_movies = Movie.query.filter(Movie.genre_id == genre_id)
            return movies_schema.dump(genre_movies), 200

        movies = Movie.query.all()
        data_movies = movies_schema.dump(movies)
        return data_movies, 200


    def post(self):
        request_data = request.json
        new_movie = Movie(**request_data)
        db.session.add(new_movie)
        db.session.commit()
        return 'Element added', 201




@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        movie_data = movie_schema.dump(movie)
        return movie_data, 200



@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(255))
    # description = db.Column(db.String(255))
    # trailer = db.Column(db.String(255))
    # year = db.Column(db.Integer)
    # rating = db.Column(db.Float)
    # genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    # genre = db.relationship("Genre")
    # director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # director = db.relationship("Director")
    # def post(self, id):

    def post(self):
        request_data = request.json
        new_director = Director(**request_data)
        db.session.add(new_director)
        db.session.commit()
        return 'Element added', 201



@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = Director.query.get(id)
        director_data = director_schema.dump(director)
        return director_data, 200







@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        request_data = request.json
        new_genre = Genre(**request_data)
        db.session.add(new_genre)
        db.session.commit()
        return 'Element added', 201




@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        genre = Genre.query.get(id)
        genre_data = genre_schema.dump(genre)
        return genre_data, 200






if __name__ == '__main__':
    app.run(debug=True)
