from rozentools.commontools import *
def llamargente(bot, update):
	try:
		registrar(bot, update)
		grupo = getGroup(update)
		if(not registrarComandoPorCinco(bot, update, "llamargente")):
			responder(bot,update,text="Espera un poco que recien los llame!")
			return
		estoyEscribiendo(bot, update)
		last_compare = ahoraMasHoras(-3)
		result = "Llamando a los que estuvieron activos desde hace...3 horas\n"
		with db_session:
			gente = select(
				(u.username,
				u.last_online,
				u.no_joder) for u in User for g in u.groups if (
					(g.id_group == grupo.id))).filter(
				lambda user,
				last_online,
				no_joder: last_online > last_compare and user and (
					datetime.datetime.now() > no_joder))
			if not gente:
				result=""
			else:
				result += "@" + \
					str.join(' @', (username for username, _, _ in gente))
		if not result:
			responder(bot, update, text="No hay gente activa desde hace 3 horas")
		else:
			responder(bot, update, text=result)
	except Exception as inst:
		printearError(bot, inst)

def nomejodasPor(bot, update, groups):
    registrar(bot, update)
    user = update.message.from_user
    estoyEscribiendo(bot, update)
    try:
        val = int(groups[1])
    except Exception as inst:
        responder(
            bot,
            update,
            text=user.first_name +
            " pone bien el numero o no pongas nada. \n Si, soy re bardero... y que?")
        return
    try:
        with db_session:
            usuario = User.get(id_user=user.id)
            usuario.no_joder = datetime.datetime.now() + datetime.timedelta(hours=val)
        responder(
            bot,
            update,
            text=user.first_name +
            " el bot no te va a llamar durante " +
            str(val) +
            " hora/s")
    except Exception as inst:
        printearError(bot, inst)


def noMeJodas(bot, update):
    groups = {}
    groups[1] = 1
    nomejodasPor(bot, update, groups)

def llamarTodos(bot, update):
	estoyEscribiendo(bot, update)
	try:
		user, group = registrar(bot, update)
		grupo = getGroup(update)
		if(user.id_user != getRozen()):
			responder(bot, update, "Esto sólo lo puede hacer Rozen!, bah pera, voy a ser bueno")
			tiempo=(datetime.datetime.now() - datetime.timedelta(hours=2))
			if(not registrarComando(bot, update, "llamartodos",tiempo)):
				bot.sendMessage(update.message.chat_id, text="No Che! Espera un poco que recien los llame!")
				return
		estoyEscribiendo(bot, update)
		result = "Llamando a.. todos por que Rozen es un forro\n"
		results = {}
		with db_session:
			gente = select(
				(u.username, u.no_joder) for u in User for g in u.groups if (
					(g.id_group == grupo.id))).filter(
				lambda user, no_joder: user and (
					datetime.datetime.now() > no_joder))
			for i in range((len(gente)//7) +1):
				results[i] = "@" + str.join(' @', (username for username, _ in gente[7*i:7*i+7]))
		responder(bot, update, result)
		for res in results.values():
			responder(bot, update, res)
		responder(bot, update, "Fede es mormon")
	except Exception as inst:
		printearError(bot, inst)

@db_session
def insultoRandom(bot):
    try:
        return select(i for i in Insulto if i.validado).random(1)[0].text
    except Exception as inst:
        printearError(bot, inst)

def bardearFede(bot, update):
    try:
        registrar(bot, update)
        estoyEscribiendo(bot, update)
        texto = insultoRandom(bot)
        responder(
            bot,
            update,
            text="che Fede ," + texto)
    except Exception as inst:
        printearError(bot, inst)

def sugerirInsulto(bot, update, groups):
    global activos
    registrar(bot, update)
    texto = groups[1]
    estoyEscribiendo(bot, update)
    if not texto:
        return
    try:
        with db_session:
            insulto = Insulto(
                user=User.get(
                    id_user=getUser(update).id),
                text=texto)
            commit()
            actual = dameNuevoIndice()
            activos[actual] = "insulto"
            actual = str(actual)
            keyboard = [[InlineKeyboardButton("Aceptar",
                                              callback_data="insulto|" + actual + '|' + str(insulto.id) + '|1'),
                         InlineKeyboardButton("Rechazar",
                                              callback_data="insulto|" + actual + '|' + str(insulto.id) + '|0')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(
                getRozen(),
                text=str(
                    "Insulto:" + texto),
                reply_markup=reply_markup)
        responder(
            bot,
            update,
            text="Ok, se lo pregunto a @Rozzen")
    except Exception as inst:
        printearError(bot, inst)


reDados = re.compile("([0-9]*)?[d|D]([0-9]+|%)")
reInvalid = re.compile("([^0-9 dD+\-()*/]|[d|D][d|D]|\*\*)")

def evaluar(bot, update, groups):
    try:
        registrar(bot, update)
        estoyEscribiendo(bot, update)
        texto = groups[1]
        nuevoTexto = ""
        laststart = 0
        try:
            variable_al_reverendo_pedo = next(reInvalid.finditer(texto))
            responder(bot, update, "Dale pelotudo ponelo bien gil")
            return
        except:
            pass

        for matcheo in reDados.finditer(texto):
            if not matcheo.group(1):
                repeticiones = 1
            else:
                repeticiones = int(matcheo.group(1))
            if(repeticiones > 99999):
                responder(
                    bot,
                    update,
                    "Dale, seguro, te quiero ver a vos tirar a mano " +
                    str(repeticiones) +
                    " dados")
                return
            dado = int(matcheo.group(2))
            nuevoTexto += texto[laststart: int(matcheo.start())] + str(
                sum(randint(1, dado) for i in range(repeticiones)))
            laststart = int(matcheo.end())
        nuevoTexto += texto[laststart:]
        responder(bot, update, str(eval(nuevoTexto)))
    except Exception as inst:
        responder(bot, update, "Nope")
        printearError(bot, inst)
def broadcast(bot, update, groups):
	try:
		user, group = registrar(bot, update)
		if(user.id_user != getRozen()):
			responder(bot, update, "Esto sólo lo puede hacer Rozen!")
			return
		texto = groups[1]
		with db_session:
			for id in select(group.id_group for group in Group):
				try:
					mandarMensaje(bot,id,texto)
				except telegram.error.BadRequest as e:
					pass
	except Exception as inst:
		printearError(bot, inst)

def restartear(bot,update):
    groups={}
    groups[1]="Me voy a dormir, ya vuelvo :D"
    broadcast(bot, update, groups)



def chaina(bot,update):
    user,group=registrar(bot, update)
    bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_AUDIO)
    audio =choice(listdir("files/saychina"))
    responderVoz(bot,update,"files/saychina/"+audio)
    #mes = bot.sendVoice(update.message.chat_id,"AwADAQADBAADd0szDxGTrVKWWtfNAg")
    #responder(bot, update, "https://www.youtube.com/watch?v=RDrfE9I8_hs")

def handlearFun(dispatcher, botname):
    comandos = [('llamargente',llamargente),('noMeJodas',noMeJodas),
        ('llamarTodos',llamarTodos),('callpeople',llamargente),
        ('bardearFede',bardearFede), ('restartear',restartear),('chaina',chaina),('saychina',chaina),
        ('startchaos@werewolfbot',llamargente),('startchaos@werewolfIIbot',llamargente),
        ('startgame@werewolfbot',llamargente),('startgame@werewolfIIbot',llamargente)]
    comandosArg = [('sugerirInsulto', sugerirInsulto),
                   ('noMeJodas', nomejodasPor), ('evaluar', evaluar),
                   ('broadcast',broadcast)]
    for c in comandosArg:
        handlearUpperLowerArgs(c[0], c[1], dispatcher, botname)
    for c in comandos:
        handlearUpperLower(c[0], c[1], dispatcher, botname)
