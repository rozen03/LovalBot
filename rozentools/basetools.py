#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import telegram
import sqlite3
import datetime
from typing import *
from telegram.ext.dispatcher import run_async


def getText(bot, update) -> str:
    try:
        text = update.message.text
    except Exception as inst:
        text = update.callback_query.message.text
    return text


def getUser(update):
    user = ""
    try:
        user = update.message.from_user
    except Exception as inst:
        user = getattr(update.callback_query, "from_user")
    return user


def getGroup(update):
    chat = ""
    try:
        chat = update.message.chat
    except Exception as inst:
        chat = update.callback_query.message.chat
    return chat
