from rozentools.commontools import *
def error_callback(bot, update, error):
	try:
		raise error
	except Unauthorized:
		# remove update.message.chat_id from conversation list
		mandarARozen(bot, "Unauthorized tu vieja")
	except BadRequest:
		mandarARozen(bot, "bad ricuest")
		# handle malformed requests - read more below!
	except TimedOut:
		mandarARozen(bot, "taimed aut")
		# handle slow connection problems
	except NetworkError:
		pass
		#mandarARozen(bot, "wetwork error")
		# handle other connection problems
	except ChatMigrated as e:
		mandarARozen(bot, "gato migrado")
		# the chat_id of a group has changed, use e.new_chat_id instead
	except TelegramError:
		mandarARozen(bot, "memegram error")
		# handle all other telegram related errors
	except Exception as inst:
		printearError(bot, inst)
		mandarARozen(bot,str(inst))

def handlearErrors(dispatcher, botname):
	dispatcher.add_error_handler(error_callback)
