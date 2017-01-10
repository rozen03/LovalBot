#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from telegram.ext import Job
from rozentools.commontools import *
from rozentools.errortools import *
from rozentools.funtools import *
from random import random, seed, randint
from tookns import LovalBotookn

def start(bot, update):
    user,group=registrar(bot, update)
    #bot.sendMessage(chat_id=update.message.chat_id,text="Hi! Let's Say China :D")
    responderVoz(bot,update,"files/saychina/1.mp3")

def graptoboy(bot,update):
	user,group=registrar(bot, update)
	bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
	randi = randint(1, 100)
	if(randi <61):
		image =choice(listdir("files/LovalBot/gato"))
		responderImagen(bot,update,"files/LovalBot/gato/"+image)
	elif(randi<91):
		image =choice(listdir("files/LovalBot/gera"))
		responderImagen(bot,update,"files/LovalBot/gera/"+image)
	else:
		image =choice(listdir("files/LovalBot/pajaros"))
		responderImagen(bot,update,"files/LovalBot/pajaros/"+image)
    #mes = bot.sendVoice(update.message.chat_id,"AwADAQADBAADd0szDxGTrVKWWtfNAg")
    #responder(bot, update, "https://www.youtube.com/watch?v=RDrfE9I8_hs")
def main():
	global update_id
	# Telegram Bot Authorization Token
	try:
		loguear("Iniciando LovalBot")
		updater = Updater(token=LovalBotookn)
		dispatcher = updater.dispatcher
		j = updater.job_queue
		start_handler = CommandHandler('start', start)
		dispatcher.add_handler(start_handler)
		comandos = [('graptoboy',graptoboy)]
		comandosArg = []
		botname = "LovalBot"
		for c in comandos:
			handlearUpperLower(c[0], c[1], dispatcher, botname)
		for c in comandosArg:
			handlearUpperLowerArgs(c[0], c[1], dispatcher, botname)
		handlearCommons(dispatcher, botname)
		handlearErrors(dispatcher, botname)
		handlearFun(dispatcher, botname)
		handler = MessageHandler(Filters.text | Filters.command, registrar)
		dispatcher.add_handler(handler)
		dispatcher.add_handler(MessageHandler(Filters.status_update,registrarIO))
		#job_minute = Job(callback_minute, 1800.0)
		#j.put(job_minute, next_t=0.0)
		#updater.start_polling()
		updater.start_polling(clean=True)
	except Exception as inst:
		loguear("ERROR AL INICIAR EL LetSSayChinaBot")
		result = str(type(inst)) + "\n"    	# the exception instance
		result += str(inst.args) + "\n"     # arguments stored in .args
		# __str__ allows args to be printed directly,
		result += str(inst) + "\n"
		loguear(result)

if __name__ == '__main__':
    main()
