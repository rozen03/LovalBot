from pony.orm import *
from rozentools.user import *
from rozentools.basetools import *

logger = logging.getLogger("Bots.log")


def loguear(texto):
    with open("logs.txt", "a") as myfile:
        myfile.write("[" +
                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                     "] " +
                     str(texto.encode('utf8')) +
                     "\n")
    logger.info(str(texto.encode('utf8')))

def usernameOrFullName(user):
    if not user.username:
        return user.first_name+" "+ user.last_name
    else:
        return user.username

@run_async
def loguearMensaje(bot, update):
    loguear(str(usernameOrFullName(getUser(update))) + ": " + getText(bot, update))


@db_session(retry=30)
def insertUser(user, usuario):
    if(not usuario):
        actual = datetime.datetime.now()
        usuario = User(id_user=user.id, first_name=user.first_name)
        if(user.last_name):
            usuario.last_name = user.last_name
    else:
        usuario.last_online = datetime.datetime.now()
        usuario.calls += 1
    if(user.username):
        usuario.username = user.username
    return usuario


def registrarUsuario(bot, user, usuario):
    try:
        with db_session:
            return insertUser(user, usuario)
    except Exception as inst:
        printearError(bot, inst)
        print("No se pudo registrar")
        mandarARozen(bot, "No se pudo registrar a " +
                     str(user.first_name) + " " + str(user.last_name))


def registrarGrupo(bot, group, grupo):
    try:
        with db_session:
            if(not grupo):
                grupo = Group(id_group=group.id, name=group.title)
            if(not group.username or grupo.chatname != group.username):
                grupo.chatname = group.username
            return grupo
    except Exception as inst:
        printearError(bot, inst)


def registrarEnGrupo(bot, usuario, grupo):
    try:
        with db_session:
            if(not usuario in grupo.users):
                grupo.users.add(usuario)
                usuario.groups.add(grupo)
    except Exception as inst:
        printearError(bot, inst)


def registrar(bot, update):
    user = getUser(update)
    grupo = getGroup(update)
    try:
        loguearMensaje(bot, update)
        with db_session:
            usuario = User.get(id_user=user.id)
            group = Group.get(id_group=grupo.id)
            usuario = registrarUsuario(bot, user, usuario)
            if(user.id != grupo.id):
                group = registrarGrupo(bot, grupo, group)
                registrarEnGrupo(bot, usuario, group)
            return usuario, group
    except Exception as inst:
        printearError(bot, inst)
        print("No se pudo registrar")
        mandarARozen(bot, "No se pudo registrar a " +
                     str(user.first_name) + " " + str(user.last_name))


@db_session
def registrarIO(bot, update):
    user = getUser(update)
    grupo = getGroup(update)
    try:
        usuario = User.get(id_user=user.id)
        group = Group.get(id_group=grupo.id)
        usuario = registrarUsuario(bot, user, usuario)
        if (user.id != grupo.id):
            group = registrarGrupo(bot, grupo, group)
            registrarEnGrupo(bot, usuario, group)
    except Exception as inst:
        printearError(bot, inst)


def registrarComando(bot, update, comando,tiempo):
    user = getUser(update)
    grupo = getGroup(update)
    try:
        bulsito = True
        with db_session:
            result = CommandPerGroup.get(command=comando, group=grupo.id)
            if(not result):
                c = CommandPerGroup(
                    command=str(comando),
                    group=grupo.id,
                    last_call=datetime.datetime.now())
            else:
                last_online = result.last_call
                if(last_online < tiempo):
                    result.last_call = datetime.datetime.now()
                else:
                    bulsito = False
        loguearMensaje(bot, update)
        return bulsito
    except Exception as inst:
        printearError(bot, inst)
        return False

def registrarComandoPorCinco(bot, update, comando):
	tiempo=(datetime.datetime.now() - datetime.timedelta(minutes=5))
	return registrarComando(bot, update, comando, tiempo)

def printearError(bot, inst):
    try:
        result = str(__name__) + "\n"
        result += str(type(inst)) + "\n"    	# the exception instance
        result += str(inst.args) + "\n"     # arguments stored in .args
        # __str__ allows args to be printed directly,
        result += str(inst) + "\n"
        # but may be overridden in exception subclasses
        loguear(result)
        mandarARozen(bot, result)
    except Exception:
        print("Explotamos mal")


def getRozen():
    return 137497264


def mandarARozen(bot, text):
    bot.sendMessage(137497264, text=str(text))


def mandarAMale(bot, text):
    bot.sendMessage(124535648, text=str(text))
