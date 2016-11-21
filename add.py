#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import  ConversationHandler
from log import *
from item import Item


#add item conversation
NAME, DESCRIPTION, PHOTO, PUBLISH = range(4)

def pre_publish(bot, update):
    '''check item before publish'''
    user = update.message.from_user
    reply_keyboard = [['/добавить', '/отмена',]]
    update.message.reply_text('Все верно?\n' + str(Item.items[user.id]), reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def add(bot, update):
    user = update.message.from_user
    update.message.reply_text('Что бы добавить товар на продажу, напишите его название. Если передумали в любой момент можно написать /отмена', reply_markup=ReplyKeyboardHide())
    Item(user.id)

    return NAME

def name(bot, update):
    '''add item name'''
    user = update.message.from_user
    itemName = update.message.text
    logger.info("Item name: %s" % (itemName))
    Item.items[user.id].add_name(itemName)

    update.message.reply_text('Отлично! Теперь напишите описание товара', reply_markup=ReplyKeyboardHide())

    return DESCRIPTION

def description(bot, update):
    '''add item description'''
    reply_keyboard = [['пропустить',]]

    user = update.message.from_user
    itemDescription = update.message.text
    logger.info("Item description: %s" % (itemDescription))
    Item.items[user.id].add_description(itemDescription)

    update.message.reply_text('Последний шаг. Отправте фото товара или нажмите "пропустить"', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PHOTO

def photo(bot, update):
    '''add item photo'''
    user = update.message.from_user
    photo_id = update.message.photo[-1].file_id
    logger.info("Item photo id from %s: %s" % (user.first_name, photo_file))
    Item.items[user.id].add_photo(photo_id)

    pre_publish(bot, update)

    return PUBLISH

def skip_photo(bot, update):
    '''if item without photo'''
    user = update.message.from_user
    logger.info("User %s doesnt add item photo :(" % (user.first_name,))

    pre_publish(bot, update)

    return PUBLISH

def cancel(bot, update):
    '''interupt adding'''
    user = update.message.from_user
    logger.info("User %s cancel :(" % (user.first_name,))
    Item.items[user.id].del_item()

    return ConversationHandler.END

def publish(bot, update):
    '''publish item'''
    user = update.message.from_user

    update.message.reply_text('Товар добавлен!', reply_markup=ReplyKeyboardHide())
    Item.items[user.id].del_item()

    return ConversationHandler.END