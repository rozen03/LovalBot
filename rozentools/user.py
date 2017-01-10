#from telegram.ext import User
from pony.orm import *
import datetime

db = Database()

# class User(telegram.ext.User):


class Group(db.Entity):
    id_group = PrimaryKey(int, size=64)
    users = Set("User")
    name = Optional(str)
    chatalias = Optional(str)
    chatname = Optional(str)
    games = Set("Game")
    reminds=Set("Remind")

class User(db.Entity):
    classtype = Discriminator(str)
    _discriminator_ = "User"
    id_user = PrimaryKey(int, size=64)
    first_name = Required(str)
    last_name = Optional(str)
    username = Optional(str, unique=True)
    calls = Required(int, default=1)
    last_online = Required(datetime.datetime, default=datetime.datetime.now())
    no_joder = Optional(datetime.datetime, default=datetime.datetime.now())
    cumple = Optional(datetime.date)
    groups = Set("Group")
    Field9 = Optional(int)
    sugerencias = Set("Sugerencia")
    insultos = Set("Insulto")
    played = Set("Player")
    reminds=Set("Remind")

class Persona(User):
    dni = Optional(int)
    _discriminator_ = "Persona"


class CommandPerGroup(db.Entity):
    command = Required(str)
    group = Required(int, size=64)
    last_call = Required(datetime.datetime)


class Game(db.Entity):
    id_game = PrimaryKey(int, size=64, auto=True)
    group = Required(Group)
    players = Set("Player")
    classtype = Discriminator(str)
    _discriminator_ = "Game"


class Player(db.Entity):
    user = Required(User)
    role = Optional(str, default="")
    game = Required(Game)
    classtype = Discriminator(str)
    _discriminator_ = "Player"


class Sugerencia(db.Entity):
    user = Required(User)
    text = Required(str)
    date = Required(datetime.date, default=datetime.date.today())
    opened = Required(bool, default=True)


class Insulto(db.Entity):
    user = Required(User)
    text = Required(str)
    date = Required(datetime.date, default=datetime.date.today())
    validado = Required(bool, default=False)


class PateaElBoton(Game):
    proba = Required(float)
    _discriminator_ = "Patea el Boton"


class Pateador(Player):
    points = Required(int, default=0)
    drunk_until = Required(datetime.datetime, default=datetime.datetime.now())
    _discriminator_ = "Pateador"


class Panda(Player):
    bamboo = Required(int, default=0)
    powerup_until = Required(
        datetime.datetime,
        default=datetime.datetime.now())
    _discriminator_ = "Panda"


class Lata(db.Entity):
    nombre = Required(str)
    cantidad = Required(int, default=0)


class Bambu(db.Entity):
    clase = Required(str)
    cantidad = Required(int, default=0)


class AdivinaAdivinador(Game):
    _discriminator_ = "AdivinaAdivinador"


class PateaAlJugador(PateaElBoton):
    _discriminator_ = "Patea al Jugador"

class Remind(db.Entity):
	user = Required(User)
	group= Optional(Group)
	start= Required(datetime.datetime)
	last = Required(datetime.datetime,default=datetime.datetime.now())
	repeat=Required(datetime.timedelta,default=datetime.timedelta())
	text = Required(str)
	enabled = Required(bool, default=False)

class Jugador(db.Entity):
    nombre = Required(str)
    cantidad = Required(int, default=0)
class File(db.Entity):
    pathName=Required(str)
    file_id=Required(str)
    botId=Required(int)

db.bind('sqlite', '../../bots.sqlite3')  # , create_db=True)
db.generate_mapping(create_tables=True)
