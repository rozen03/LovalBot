#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from telegram.ext import Updater
from telegram.error import (TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError)
import itertools
import sqlite3
import datetime
from rozentools.logs import *
from rozentools.user import *
from random import random, seed, randint,choice
import datetime
import re
from ctypes import cdll
from os import listdir
from os.path import isfile, join
from functools import wraps
actual = datetime.datetime.now().timestamp() * 100
seed(actual)

def reply_decorator(f):
	@wraps(f)
	def wrapper(bot, update, **kwds):
		def reply(*reply_args, **reply_kwargs):
			return update.message.reply_text(*reply_args, **reply_kwargs)
		f.__globals__['reply'] = reply
		f.__globals__['responder'] = responder
		return f(bot, update, **kwds)
	return wrapper

def ahoraMasHoras(horas):
	return datetime.datetime.now() + datetime.timedelta(hours=horas)
def ahoraMasMinutos(minutos):
	return datetime.datetime.now() + datetime.timedelta(minutes=minutos)
def ahoraMasSegundos(segundos):
	return datetime.datetime.now() + datetime.timedelta(seconds=segundos)

def responder(bot, update, text: str):
	update.message.reply_text(str(text),quote=False)

def responderVoz(bot,update,filePath):
    with db_session:
        audioFile= File.get(pathName=filePath, botId=bot.id)
    if not audioFile:
        bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_AUDIO)
        message = update.message.reply_voice(open(filePath,"rb"),quote=False)
        with db_session:
            newVoice= File(pathName=filePath,file_id=message.voice.file_id,botId=bot.id)
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_AUDIO)
        update.message.reply_voice(audioFile.file_id,quote=False)

def responderImagen(bot,update,filePath):
    with db_session:
        audioFile= File.get(pathName=filePath, botId=bot.id)
    if not audioFile:
        bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
        message = update.message.reply_photo(open(filePath,"rb"),quote=False)
        with db_session:
            newImage= File(pathName=filePath,file_id=message.voice.file_id,botId=bot.id)
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
        update.message.reply_photo(audioFile.file_id,quote=False)

def estasVivo(bot, update):
    try:
        responder(bot, update, "Si, estoy vivo")
    except Exception as inst:
        printearError(bot, inst)


def handlearUpperLower(texto, funcion, dispatcher, botname: str):
    handlr = RegexHandler(
        "^(?i)/" + texto + "(|@" + botname + ")($|\s)",
        funcion,
        pass_groups=False,
        pass_groupdict=False,
        pass_update_queue=False,
        pass_job_queue=False)
    dispatcher.add_handler(handlr)


def handlearUpperLowerArgs(texto, funcion, dispatcher, botname: str):
    handlr = RegexHandler(
        "^(?i)/" + texto + "(|@" + botname + ")\s(.*)",
        funcion,
        pass_groups=True,
        pass_groupdict=False,
        pass_update_queue=False,
        pass_job_queue=False)
    dispatcher.add_handler(handlr)


def sugerir(bot, update, groups):
    registrar(bot, update)
    estoyEscribiendo(bot, update)
    try:
        texto = groups[1]
        if not texto:
            return
        with db_session:
            sugerencia = Sugerencia(
                user=User.get(
                    id_user=getUser(update).id),
                text=texto)
        mandarARozen(bot, str("Sugerencia:" + texto))
        bot.sendMessage(
            update.message.chat_id,
            text="Ok, se lo mando a @Rozzen")
    except Exception as inst:
        printearError(bot, inst)


@run_async
def estoyEscribiendo(bot, update):
    bot.sendChatAction(
        chat_id=update.message.chat_id,
        action=telegram.ChatAction.TYPING)

def dameNuevoIndice():
    return int(datetime.datetime.now().timestamp() * 100)


def mandarMensaje(bot,id,texto):
    try:
        bot.sendMessage(id, text=texto)
    except Exception as inst:
        printearError(bot, inst)
def handlearCommons(dispatcher, botname):
    comandos = [('estasVivo',estasVivo)]
    comandosArg = [('sugerir', sugerir)]
    for c in comandosArg:
        handlearUpperLowerArgs(c[0], c[1], dispatcher, botname)
    for c in comandos:
        handlearUpperLower(c[0], c[1], dispatcher, botname)
    logging.basicConfig(
        level=logging.INFO,
		#level=logging.DEBUG,
        format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
        filename="bots.log")
