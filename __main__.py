
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyromod.helpers import ikb, array_chunk

import pyromod

language = []
plugins = dict(root="plugins")
app = Client("ARS_DL", 
             api_id=11111111,
             plugins=plugins,
             api_hash="JUSTCHANGEIT",
             bot_token="6489326673:AAF20M8j0FHspx1NyyMms4SHKrSYO3G3hGQ")





app.run()
