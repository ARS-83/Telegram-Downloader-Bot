from pyrogram import Client, filters

import json
from pyromod.helpers import ikb, array_chunk, kb
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import aiosqlite
from db import Context
import aiofiles
context = Context.DatabaseManager()


async def IsUserExist(userId: int):
    user = await context.ExecuteQueryOne(f"SELECT * FROM Users WHERE UserId = {userId}")
    
    if user == None:
        return False
    else:
        return True


async def GetLangList():
    async with aiofiles.open('language.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
  
    return res


async def GetLang(id: int):
    lenUser =await context.ExecuteQueryOne(f"SELECT UserLanguage FROM Users WHERE UserID = {id} ")
    
    async with aiofiles.open('language.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
  

    return res[f'{lenUser[0]}']


async def GetUsersInfo():
    data = await context.ExecuteQueryOne("SELECT COUNT() FROM Users")
    if data!=None:
      return data[0]
    else:    
     return  0
async def AddNewUser(userId: int, userName: str,app):
    asmin =await GetDataConfig1("Admin")
    await app.send_message(asmin,f"""🥳 کاربری جدید به ربات اضافه شد

نام کاربری : {userName}

شناسه : <code>{userId}</code>

❤️‍🔥 هورااااا

.
""")
    await context.QueryWidthOutValue(
        f"INSERT INTO Users(UserId,UserName,STEP) VALUES({userId}, '{userName}','home')")
  


async def AddLangToUser(userId: int, langKeys: str):
   await context.QueryWidthOutValue(
        f"UPDATE Users SET UserLanguage = '{langKeys}' WHERE UserId = {userId}")

  

async def GetDataConfig1(data):
    async with aiofiles.open('config.json', mode='r',encoding='utf-8') as f: 
      res =   json.loads(await f.read())
  
    return res['Admin']

async def ChangeStepUser(userId , data):
    await context.QueryWidthOutValue(f"UPDATE Users SET STEP = '{data}' WHERE UserId = {userId}")


async def GetUserSTEP(userId):
    step = await context.ExecuteQueryOne(f"SELECT STEP FROM Users WHERE UserId = {userId}")
    return step[0]

async def GetMainKey(userId: int):
    lang = await GetLang(userId)
    await ChangeStepUser(userId,'home')
    if await GetDataConfig1("Admin") == userId:
        return ReplyKeyboardMarkup([[lang['btnYoutube'], lang['btnIstagram']], [lang['btnSpotify'], lang['btnSoundCloud']], [lang['btnMangageUser'], lang['ManageBot']]], resize_keyboard=True, one_time_keyboard=True)

    else:
        return ReplyKeyboardMarkup([[lang['btnYoutube'], lang['btnIstagram']], [lang['btnSpotify'], lang['btnSoundCloud']], [lang['btnMangageUser']]], resize_keyboard=True, one_time_keyboard=True)


async def AddUserActivity(userId: int, url: str, type: str):
    userActivity =await context.ExecuteQueryOne(
        f"SELECT * FROM UserDownload WHERE UserId = {userId}  AND URL = '{url}' AND type = '{type}' ")
    
    if userActivity == None:
        lastrowId = await context.Query("INSERT INTO UserDownload(URL,UserId,type) VALUES(?,?,?)", (
                        url, userId, type))
        uuid = lastrowId.lastrowid

       
        return uuid
    else:
        return userActivity[0]


async def UpdateUserActivity(ua: int, mesId: str, name: str):
    userActive= await context.ExecuteQueryOne(f"SELECT * FROM UserDownload WHERE Id = {ua}")
    
    await context.QueryWidthOutValue(
        f"UPDATE UserDownload SET CountDownload = {userActive[4] + 1} , MesId = '{mesId}' , Name = '{name}'   WHERE Id = {ua}")
  


async def Forward(udId: int):
    data =await context.ExecuteQueryOne(f"SELECT * FROM UserDownload WHERE Id = {udId} ")
    
    return data[5]


async def GetUserDownloaded(uuId: int):
    res = await context.ExecuteQueryAll(
        f"SELECT * FROM UserDownload WHERE UserId = {uuId} AND CountDownload != 0 ")
    
    btn = []
    if res != []:
        for data in res:
            details = []
            if data[6] == None:
                details.append(InlineKeyboardButton(
                    data[1][:40], url=f"{data[1]}"))
            else:
                details.append(InlineKeyboardButton(
                    data[1][:40], url=f"{data[1]}"))
                details.append(InlineKeyboardButton(
                    f"{data[6][:50]}", callback_data="ARS"))
            btn.append(details)
            btn.append([InlineKeyboardButton("📥", callback_data=f"ARSForwarder_{data[0]}"), InlineKeyboardButton(
                f"{data[4]} 🔁", callback_data="ARS")])
            btn.append([InlineKeyboardButton(
                "❌", callback_data=f"DeleteItem_{data[0]}")])
    else:
        lan =await GetLang(uuId)
        btn.append([InlineKeyboardButton(
            f"{lan['NoContent']}", callback_data="ARS")])
    return btn


async def GetUrl(ua: int):
    userActive =await context.ExecuteQueryOne(f"SELECT * FROM UserDownload WHERE Id = {ua}")

    return userActive[1]


async def DeleteItem(udId: int):
   await context.QueryWidthOutValue(f"DELETE FROM UserDownload WHERE Id = {udId}")
    


async def GetDataConfig(data: str):
    if data == "INSTAACCOUNT":

        async with aiofiles.open('config.json', mode='r',encoding='utf-8') as f: 
               res =   json.loads(await f.read())
  
   
        return res['INSTAACCOUTNAME']
    elif data == "SESSION":
        async with aiofiles.open('config.json', mode='r',encoding='utf-8') as f: 
               res =   json.loads(await f.read())
        return res['SESSION']
    elif data == "Admin":
        async with aiofiles.open('config.json', mode='r',encoding='utf-8') as f: 
               res =   json.loads(await f.read())
        return res['Admin']


async def GetLockCahnel():
    LockChanels = await  context.ExecuteQueryAll(f"SELECT * FROM Lock")
    
    btn = []
    for lock in LockChanels:
        btn.append((lock[1], f"ARS"))
        btn.append(("❌", f"DeleteCahnel_{lock[0]}"))
    return btn
async def GetLockALlCahnel():
    data = await context.ExecuteQueryAll(f"SELECT * FROM Lock")
    return data


async def AddChanel(Name: str, ChanelDes: str):
    await context.Query("INSERT INTO Lock(Name,UserLink) VALUES(?,?)", (
        Name,
        ChanelDes
    ))
   

async def DeleteChanel(data:int):
    await context.QueryWidthOutValue(f"DELETE FROM Lock WHERE Id = {data}")
   
    LockChanels = await context.ExecuteQueryAll(f"SELECT * FROM Lock")
    
    btn = []
    for lock in LockChanels:
        btn.append((lock[1], f"ARS"))
        btn.append(("❌", f"DeleteCahnel_{lock[0]}"))
    return btn

async def GetAllUser():
    user = await context.ExecuteQueryAll("SELECT UserId FROM Users")
    
    return user

async def GetlistChanel():
    LockChanels = await context.ExecuteQueryAll(f"SELECT * FROM Lock")
    
    btn = []
    for lock in LockChanels:
        lock
        btn.append([InlineKeyboardButton(lock[1],url=f"https://t.me/{lock[2]}")])
    return btn