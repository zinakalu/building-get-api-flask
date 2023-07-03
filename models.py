from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Game(db.Model, SerializerMixin): #parent to review class
    __tablename__ = 'games'

    serialize_rules = ('-reviews.game',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now()) #created_at and updated_at are used to track the creation and modification timestamps of the records in the table. Allowing us to keep track of when the records were created and last modified
    updated_at = db.Column(db.DateTime, onupdate=db.func.now()) #db.func.now() =  current time it is

    reviews = db.relationship('Review', backref='game')

    def __repr__(self):
        return f'<Game {self.title} for {self.platform}>'


class Review(db.Model, SerializerMixin): #child
    __tablename__ = 'reviews'

    serialize_rules = ('-game.reviews', '-user.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    comment = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now()) 
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(db.Model, SerializerMixin): #parent to review class
    __tablename__ = 'users'

    serialize_rules = ('-reviews.user',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    reviews = db.relationship('Review', backref='user')


#IN THE TERMINAL
#flask shell
#game = Game.query.first()
#game.to_dict()
#This fetches a Game object from the databse using Game.query.first() and then calls the to_dict() method on it. 
#the resulting dictionary represents the serialized version of the Game object, including its attributes and realted reviews