
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyromod.helpers import ikb, array_chunk

import pyromod

language = []
plugins = dict(root="plugins")
app = Client("ARS_DL", 
             api_id=27920385,
             plugins=plugins,
             api_hash="6ef7b57f85f5d96dfbde6b4fd36412be",
             bot_token="6489326673:AAF20M8j0FHspx1NyyMms4SHKrSYO3G3hGQ")





app.run()
