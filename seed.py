from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Game, Review, User

genres = [
    "Platformer",
    "Shooter",
    "Fighting",
    "Stealth",
    "Survival",
    "Rhythm",
    "Survival Horror",
    "Metroidvania",
    "Text-Based",
    "Visual Novel",
    "Tile-Matching",
    "Puzzle",
    "Action RPG",
    "MMORPG",
    "Tactical RPG",
    "JRPG",
    "Life Simulator",
    "Vehicle Simulator",
    "Tower Defense",
    "Turn-Based Strategy",
    "Racing",
    "Sports",
    "Party",
    "Trivia",
    "Sandbox"
]


platforms = [
    "NES",
    "SNES",
    "Nintendo 64",
    "GameCube",
    "Wii",
    "Wii U",
    "Nintendo Switch",
    "GameBoy",
    "GameBoy Advance",
    "Nintendo DS",
    "Nintendo 3DS",
    "XBox",
    "XBox 360",
    "XBox One",
    "XBox Series X/S",
    "PlayStation",
    "PlayStation 2",
    "PlayStation 3",
    "PlayStation 4",
    "PlayStation 5",
    "PSP",
    "PS Vita",
    "Genesis",
    "DreamCast",
    "PC",
]

fake = Faker()

with app.app_context(): 
    Review.query.delete()
    User.query.delete()
    Game.query.delete()

    users = []
    for i in range(100):
        u = User(name=fake.name(),)
        users.append(u)

    db.session.add_all(users)

    games = []
    for i in range(100):
        g = Game(
            title=fake.sentence(),
            genre=rc(genres),
            platform=rc(platforms),
            price=randint(5, 60),
        )
        games.append(g)

    db.session.add_all(games)

    reviews = []
    for u in users:
        for i in range(randint(1, 10)):
            r = Review(
                score=randint(0, 10),
                comment=fake.sentence(),
                user=u,
                game=rc(games))
            reviews.append(r)

    db.session.add_all(reviews)

    for g in games:
        r = rc(reviews)
        g.review = r
        reviews.remove(r)

    db.session.commit()
