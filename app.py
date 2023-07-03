from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return "Index for Game/Review/User API"


@app.route('/games')
def games():

#this is how we get our data from the database to display on the browser
    games = []

    games_by_title = Game.query.order_by(Game.title).all() #queries in alphabetical order
    # first_10_games = Game.query.limit(10).all() #returns the first ten games
    for game in games_by_title:
        game_dict = {
            'title': game.title,
            'genre': game.genre,
            'platform': game.platform,
            'price':game.price,
        }
    # for game in Game.query.all(): Queries for all the games
    #     game_dict = {
    #         'title': game.title,
    #         'genre': game.genre,
    #         'platform': game.platform,
    #         'price':game.price,
    #     } #we get our Game data
        print(games_by_title)
        games.append(game_dict) 

    response = make_response(
            jsonify(games), #turn the data into json so it can be returned to the client
            200,
            {"Content-type": "application/json"} #since our server is used to send JSON data, we change the response header
    )
        
    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first() #use unique attributes in your dynamic URLs. This helps to retrieve the ONE , correct result for your filter statement, use a unique attribute.

    #getting data from the database
    # game_dict = {
    #     "title": game.title,
    #     "genre": game.genre,
    #     "platform": game.platform,
    #     "price": game.price,
    # } EASIER STRATEGY BELOW
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

    #OR
@app.route('/game/<int:game_id>')
def get_game(game_id):
    game = Game.query.get(game_id)
    if game is None:
        return jsonify({'error': 'Game not found'}), 404
    # return jsonify(game.to_dict()) #or
    game_dict = game.to_dict() 
    title = game_dict['title']
    return jsonify(title) #we have to turn the dictionary representation into json
#here, game.to_dict() returns a dictionary representation of the Game object, and game_dict['title'] accesses the value of the title attribute from that dictionary. 

if __name__ == '__main__':
    app.run(port=5555, debug=True)