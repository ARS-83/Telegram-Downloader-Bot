from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyromod.helpers import ikb, array_chunk
from pytube import YouTube
import pyromod
import httpx
import aiofiles
import datetime
import os
import requests
import datetime
import time
import instaloader
import shutil
from instabot import Bot
import random
from sclib.asyncio import SoundcloudAPI, Track, Playlist
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup as bs
from plugins import Config
from spotdl import Spotdl, Song
language = []
# // https://youtu.be/5vQC4sNDHgk?si=4qGAU5ueNOJIqVxO


# Config


# spotify
CLIENTID = "d65d0d9753e2411682ebd49452a351fc"
CLIENTSECRET = "690d8b7d02044fe990e60d89b0b676e6"

async def lockChanel(c:Client,userId:int):
  chanels = await Config.GetLockALlCahnel()
  for chanel in chanels:
    try:
  
      await c.get_chat_member(chat_id=chanel[2],user_id=userId)
    except:
        return False

  return True  


async def CheckJoin(_,c:Client,m:Message):
   
  chanels = await Config.GetLockALlCahnel()
  for chanel in chanels:
    try:
  
      await c.get_chat_member(chat_id=chanel[2],user_id=m.from_user.id)
    except:
        return False

  return True  


async def lockChanel(c:Client,userId:int):
  chanels = await Config.GetLockALlCahnel()
  for chanel in chanels:
    try:
  
      await c.get_chat_member(chat_id=chanel[2],user_id=userId)
    except:
        return False

  return True  

CheckLock = filters.create(CheckJoin)
async def CheckBtnsNot(_,c:Client,m:Message):
   btns = ["مدیریت ⚫️","Manage ⚫️","دانلود شده 🟤","Downloaded 🟤","اسپاتیفای 🟢","/start","ساند کلاد 🟠","اینستاگرام 🟣","یوتوب 🔴","Media ⚪️","Instagram 🟣","YouTube 🔴","Spotify 🟢","SoundCloud 🟠"]

   if m.text not in btns : 
       
       return True
   else:
       await Config.ChangeStepUser(m.from_user.id,"home")
       
       return False
  
checkBtnsNot = filters.create(CheckBtnsNot)
@Client.on_message(  checkBtnsNot & CheckLock)
async def STEPHandler(c:Client,m:Message):
  STEP = await Config.GetUserSTEP(m.from_user.id)
  if m.text!=None:
   if "/start " in m.text :
     await Start(c,m)
     return
 
  if  m.text == "انصراف" or m.text == "Cancel":
      await CancelKeys(c,m)
      return
  elif  STEP == "downloadYoutube" :
        
        await YoutubeDownload(c,m)
        return
  
  elif STEP == "Post" :
        
        await PostDownload(c,m)
        return
  elif STEP ==  "Story" :
        
        await StoryDownload(c,m)
        return
  elif "GetUserInstagramDetails" in STEP:
 
        await GetUserInstagramDetails(c,m)
        return

  elif STEP ==  "SoungSoundCloud" :
       
        await SoungSoundCloud(c,m)
        return

  elif STEP == "PlayListSoundCloud":
     
        await PlayListSoundCloud(c,m)
        return
 
  else:
       await Config.ChangeStepUser(m.from_user.id,'home')


async def PlayListSoundCloud(c:Client,m:Message):
           language =await Config.GetLang(m.from_user.id)
           try:
             await m.delete()
             await c.send_message(chat_id=m.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
             IdActivity = await Config.AddUserActivity(m.from_user.id, m.text, "sound")
             dataGet = m.text
             if "https://on.soundcloud.com/" in dataGet:
               response = requests.get(dataGet)
               dataGet = response.url
             api = SoundcloudAPI()
             playlist  = await api.resolve(dataGet)
             assert type(playlist) is Playlist
             mes =await m.reply_text(f"""
🔍 : {playlist.title}

🕐 : { time.strftime("%M:%S", time.gmtime(playlist.duration))}

🔺 : {playlist.track_count}

📥👇🏻👇🏻👇🏻

""",reply_markup=await Config.GetMainKey(m.from_user.id))
             mesId = f"{mes.id},"
             for track in playlist.tracks:
                  url =await track.get_stream_url()
                  mes = await c.send_audio(chat_id=m.from_user.id, audio=url,caption=track.title )
                  mesId += f"{mes.id},"

             await m.message.reply("✅")  
             await Config.UpdateUserActivity(IdActivity,mesId,playlist.title)

             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
             return   
           except:
             await m.delete()
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

async def SoungSoundCloud(c:Client,m:Message):
         language =await Config.GetLang(m.from_user.id)
         try:
          await m.delete()
          await c.send_message(chat_id=m.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
          IdActivity = await Config.AddUserActivity(m.from_user.id, m.text, "sound")
          dataGet = m.text   
          api = SoundcloudAPI()
          if "https://on.soundcloud.com/" in dataGet:
              response = requests.get(dataGet)
              dataGet = response.url
          
          track = await api.resolve(dataGet) 
          url = await track.get_stream_url()
          mes =await c.send_audio(chat_id=m.from_user.id, audio=url ,caption=track.title )
          await Config.UpdateUserActivity(IdActivity,mes.id,track.title)
          await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
           
         
            #  await call.message.reply(language['notDownloadable'])
            #  await c.send_message(chat_id=call.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(call.from_user.id))
            #  return
         except:
             await m.delete()
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

async def GetUserInstagramDetails(c:Client,m:Message):
          language =await Config.GetLang(m.from_user.id)
          try:  
            INSTAACCOUNT =await Config.GetDataConfig("INSTAACCOUNT")
            SESSION =await Config.GetDataConfig("SESSION")
            await m.delete()
            await c.send_message(chat_id=m.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
            Loader = instaloader.Instaloader()
            Loader.load_session_from_file(
           INSTAACCOUNT , SESSION)
            profile = Loader.check_profile_id(m.text)
            is_private = language['yes']
            if profile.is_private != True:
              is_private = language['no']
            await m.reply_photo(profile.profile_pic_url_no_iphone, caption=f""" 
🔍 {language['UserDetails']}  :

✍🏻 {language['BIO']} :

{profile.biography}

🔘 {language['mediacount']} : {profile.mediacount}

👤 {language['author']} : {profile.username}

👥 {language['FullName']} : {profile.full_name}

🗣 {language['followers']} : {profile.followers}     

🫂 {language['followees']} : {profile.followees}     

🫂 {language['IsPrivate']} : {is_private}  

🔺🔻🔺🔻🔺🔻🔺

""")
            shutil.rmtree(f"{profile.username}")
            return
          except:
             await m.delete()
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

async def StoryDownload(c:Client,m:Message):
         language =await Config.GetLang(m.from_user.id)
         try: 
          INSTAACCOUNT =await Config.GetDataConfig("INSTAACCOUNT")
          SESSION =await Config.GetDataConfig("SESSION")
          await c.send_message(chat_id=m.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
          Loader = instaloader.Instaloader()
          Loader.load_session_from_file(
            INSTAACCOUNT, SESSION)
          IdActivity = await Config.AddUserActivity(m.from_user.id, m.text, "insta")
          profile = Loader.check_profile_id(m.text.split("/")[-2])
          alireza = Loader.get_stories(userids=[profile.userid])

          itemSelect = None
          for a in alireza:
            for item in a.get_items():
                if item.mediaid == int(m.text.split("/")[5].split("?")[0]):
                    itemSelect = item
                    break
            if itemSelect != None:
                break

          if itemSelect.is_video == True:
            Loader.download_storyitem(itemSelect, m.text.split('/')[-2])
            await m.message.delete()
            files = os.listdir(f"{m.text.split('/')[-2]}")
            for f in files:
                if ".mp4" in f:
                    mes=await m.reply_video(f"{m.text.split('/')[-2]}/{f}")
                    shutil.rmtree(f"{m.text.split('/')[-2]}")
                    await Config.UpdateUserActivity(IdActivity,mes.id,profile.username)
                    await Config.ChangeStepUser(m.from_user.id,'home')
                    return

          elif itemSelect.is_video != True:
            Loader.download_storyitem(itemSelect, m.text.split('/')[-2])
            await m.delete()
            files = os.listdir(f"{m.text.split('/')[-2]}")
            for f in files:
                if ".jpg" in f:
                    mes =await m.reply_photo(f"{m.text.split('/')[-2]}/{f}")
                    shutil.rmtree(f"{m.text.split('/')[-2]}")
                    await Config.UpdateUserActivity(IdActivity,mes.id,profile.username)
                    await Config.ChangeStepUser(m.from_user.id,'home')
                    return
          await Config.ChangeStepUser(m.from_user.id,'home')    
         except:
             await m.delete()
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

async def PostDownload(c:Client,m:Message):
    language =await Config.GetLang(m.from_user.id)
    # try:
    if "https://www.instagram.com/p/" or "https://www.instagram.com/reel/" in m.text:
        #    try:  
             
             INSTAACCOUNT =await Config.GetDataConfig("INSTAACCOUNT")
             SESSION =await Config.GetDataConfig("SESSION")
             await c.send_message(chat_id=m.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
             Loader = instaloader.Instaloader(max_connection_attempts=300,request_timeout=3)
             Loader.load_session_from_file(
            INSTAACCOUNT, SESSION)
            
             IdActivity = await Config.AddUserActivity(m.from_user.id, m.text, "insta")
             post = instaloader.structures.Post.from_shortcode(
                Loader.context, m.text.split("/")[-2])
            
             await c.send_message(m.from_user.id, language['PleaseWait'])
             Loader.download_post(
                post, target=m.text.split("/")[-2])
             files = os.listdir(f"{m.text.split('/')[-2]}")
             mes =None
             mesId = ""
             for f in files:
                if ".jpg" in f:
                   mes= await m.reply_photo(f"{m.text.split('/')[-2]}/{f}")
                   mesId += f"{mes.id },"
                elif ".mp4" in f:
                    mes =await  m.reply_video(f"{m.text.split('/')[-2]}/{f}")
                    mesId += f"{mes.id },"
                elif ".txt" in f:
                    files = open(
                        f"{m.text.split('/')[-2]}/{f}", "r", encoding='utf-8')
                    mes =await m.reply(files.read())
                    mesId += f"{mes.id },"
             shutil.rmtree(f"{m.text.split('/')[-2]}")
             await Config.UpdateUserActivity(IdActivity,mesId,post.caption[:40])
             await Config.ChangeStepUser(m.from_user.id,'home')
             return
        #    except:
        #      await call.message.delete()
        #      await call.message.reply(language['getProblem'])
        #      await c.send_message(chat_id=call.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(call.from_user.id))
    else:
            
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
    # except:
    #         await m.delete()
    #         await m.reply(language['getProblem'])

    #         await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
            
    #         return
async def YoutubeDownload(c:Client,m:Message):
            language =await Config.GetLang(m.from_user.id)
        # try:
            IdActivity = await Config.AddUserActivity(m.from_user.id, m.text, "yt")
            await m.reply(language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))

            yt = YouTube(m.text)
            convert = str(datetime.timedelta(seconds=yt.length))
            video_streams = yt.streams.filter(
                file_extension='mp4', progressive=True).all()
            audio_streams = yt.streams.get_audio_only()

            keysDownloder = []
            if audio_streams != None:
                keysDownloder.append((f"🎵 {audio_streams.abr}",f"DownloadYoutube_{audio_streams.abr}_{IdActivity}_3"))
                keysDownloder.append((
                    f"{round(audio_streams.filesize_mb,2)} MB", "ARS"))
            for videoRes in video_streams:
                keysDownloder.append(
                    (f"📥 { videoRes.resolution}", f"DownloadYoutube_{videoRes.resolution}_{IdActivity}_4"))
                keysDownloder.append((
                    f"{round(videoRes.filesize_mb,2)} MB", "ARS"))

            test = await m.reply_photo(yt.thumbnail_url, caption=f"""

👤 {language['author']} : {yt.author}

♦️ {language['caption']} : {yt.title}

🕐 {convert}

👁 {yt.views}
""", reply_markup=ikb(array_chunk(keysDownloder, 2)))
            
            await Config.ChangeStepUser(m.from_user.id,'home')
            return
        # except:
        #     await m.delete()
        #     await m.reply(language['getProblem'])

        #     await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
            
        #     return
   


@Client.on_message(filters.command('start'))
async def Start(c: Client, m: Message):
    await lockChanel(c,m.from_user.id)
    if await Config.IsUserExist(m.from_user.id) != True:
       await Config.AddNewUser(m.from_user.id, m.from_user.username,c)
    langs = await Config.GetLangList()
    keys = []
    for lang in langs:
        keys.append((f"{langs[lang]['type']}", f"SelectLang_{lang}"))

    await m.reply_text("""
 به ربات دانلود  از پلتفرم های مختلف خوش امدید لطفا زبان مورد نظر خودتون رو انتخاب کنید ♦️

♦️ Welcome to the download bot from different platforms. Please choose your desired language 

▪️▫️▪️▫️▪️▫️▪️
""", reply_markup=ikb(array_chunk(keys, 1)))

@Client.on_message(filters.regex("Downloaded 🟤"))
@Client.on_message(filters.regex("دانلود شده 🟤"))
async def DownloadedHandel(c:Client,m:Message):
   language =await Config.GetLang(m.from_user.id)
   
   if await lockChanel(c,m.from_user.id)==True: 
    await m.reply(language['UserPanel'],reply_markup=InlineKeyboardMarkup(await Config.GetUserDownloaded(m.from_user.id)))
   else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 

@Client.on_message(filters.regex("انصراف"))
@Client.on_message(filters.regex("Cancel"))
async def CancelKeys(c: Client, m: Message):
    language =await Config.GetLang(m.from_user.id)
    
    await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

@Client.on_message(filters.regex("Manage ⚫️"))
@Client.on_message(filters.regex("مدیریت ⚫️"))
async def ManageBot(c:Client,m:Message):
  if await Config.GetDataConfig("Admin") == m.from_user.id  :
    language =await Config.GetLang(m.from_user.id)

    #TODO Create this
    await m.reply(language['ManageDes'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(language['messegeToAll'],callback_data="publicMessage"),InlineKeyboardButton(language['lock'],callback_data="lockchanel")],[InlineKeyboardButton(language['InfoBot'],callback_data="InfoBot")]]))
 

@Client.on_message(filters.regex("یوتوب 🔴"))
@Client.on_message(filters.regex("YouTube 🔴"))
async def YouTubeDownloader(c: Client, m: Message):
   language =await Config.GetLang(m.from_user.id)
   
   if await lockChanel(c,m.from_user.id)==True: 
    await Config.ChangeStepUser(m.from_user.id,'downloadYoutube')
    await m.reply(language['SendLink'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
   
    return
      
   else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel()))    
@Client.on_message(filters.regex("Instagram 🟣"))
@Client.on_message(filters.regex("اینستاگرام 🟣"))
async def InstagramHandler(c: Client, m: Message):

    language =await Config.GetLang(m.from_user.id)
    if await lockChanel(c,m.from_user.id)==True: 
     await m.reply(language['InstagramMain'], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(language['Story'], callback_data="Story"), InlineKeyboardButton(language['Post'], callback_data="Post")], [InlineKeyboardButton(language['UserDetails'], callback_data="GetUserInstagramDetails")]]))
    else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 

def is_music_link(link):
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']
    return any(link.endswith(ext) for ext in audio_extensions)


def is_video_link(link):
    video_extensions = ['.mp4', '.avi', '.mkv',
        '.wmv', '.flv', '.mov', '.webm']
    return any(link.endswith(ext) for ext in video_extensions)


def is_image_link(link):
    image_extensions = ['.jpg', '.jpeg', '.png',
        '.gif', '.bmp', '.webp', '.tiff']
    return any(link.endswith(ext) for ext in image_extensions)


def is_docoument(link):
    doc = [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls"]


def is_downloadable(url,IsEncode):

   if  IsEncode ==False:
    try:
        response = requests.head(url)
        content_type = response.headers['content-type'].lower()
        print(content_type)
        print(response.headers['content-length'])
        if 'text' in content_type or 'html' in content_type:
            return [False,"NoFile"]  
        if 'content-length' in response.headers:
            file_size = int(response.headers['content-length'])
            if file_size <= 0:
                return  [False,"NoSize"]  
            if file_size >= 104857600:
                return  [False,"BigFile"] 
    
        if 'audio/' or  'video/' or 'image/' in response.headers['content-type'].lower():

            return [True,f"{response.headers['content-type'].lower()}"] 
        return [False,"NoFile"]  
    except requests.RequestException:
        return [False,"ErrInGet"]    
   else:
      try: 
        response = requests.head(url)
        if 'content-length' in response.headers:

            file_size = int(response.headers['content-length'])
            if file_size <= 0:
                return  [False,"NoSize"]  
            elif file_size >= 104857600:
                return  [False,"BigFile"] 
            else:
                return [True,""]
        else:
              return  [True,""]
      except requests.RequestException:
            return [False,"ErrInGet"]    
  
@Client.on_message(filters.regex("Media ⚪️"))
@Client.on_message(filters.regex("رسانه ⚪️"))
async def MediaHandler(c: Client, m: Message):
   language =await Config.GetLang(m.from_user.id)
   if await lockChanel(c,m.from_user.id)==True: 
    await m.reply(language['PleaseWait'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
    anwser = await pyromod.Chat.ask(text=language['SendLink'], self=m.chat)
    if anwser.text != language['cancelKey']:
        try:
            await m.delete()
            mes = None
            await m.reply( text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
            typeDownload = is_downloadable(anwser.text,True)
            if typeDownload[0]==True:    
             if is_video_link(anwser.text):
                mes =await m.reply_video(anwser.text)
                IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
                return
             elif is_music_link(anwser.text):
                mes =await m.reply_audio(anwser.text)
                IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
                return
             elif is_image_link(anwser.text):
                mes =await m.reply_photo(anwser.text)
               
                IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
                return
             elif is_docoument(anwser.text):
               mes = await m.reply_document(anwser.text)
               IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
               await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
               return
             else:
                typeDownload = is_downloadable(anwser.text,False)
                name = random.randint(0,10000)
                if typeDownload[0]==True:

                    typeDownload = typeDownload[1]
                    if typeDownload.startswith('audio/'):
                        res = requests.get(anwser.text,allow_redirects=True)
                        file = open(f"Media/{name}.mp3","wb")
                        file.write(res.content)
                        file.close()
                        mes =await m.reply_audio(res.content)
                        os.remove(f"Media/{name}.mp3")
                        IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                        await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
                        return
                    elif typeDownload.startswith('video/'):
                        res = requests.get(anwser.text,allow_redirects=True)
                        file = open(f"Media/{name}.mp4","wb")
                        file.write(res.content)
                        file.close()
                        mes =await m.reply_video(video=f"Media/{name}.mp4")
                        os.remove(f"Media/{name}.mp4")
                        IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                        print(IdActivity)
                        await Config.UpdateUserActivity(IdActivity,mes.id,"Media")
                        return
                elif typeDownload.startswith('image/'):
                        res = requests.get(anwser.text,allow_redirects=True)
                        file = open(f"Media/{name}.jpg","wb")
                        file.write(res.content)
                        file.close()
                        mes =await m.reply_photo(video=f"Media/{name}.jpg")
                        os.remove(f"Media/{name}.jpg")
                        IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "media")
                        await Config.UpdateUserActivity(IdActivity,mes.id,"Media")

                        return
                elif typeDownload[1]=="NoFile":
                    await m.delete()
                    await m.reply(language['canotdiagnosis'])
                    return
                elif  typeDownload[1]=="BigFile": 
                    await m.delete()
                    await m.reply(language['BigFile'])                   
                    return
                elif   typeDownload[1]=="ErrInGet":
                 await m.delete()
                 await m.reply(language['getProblem'])
                 return
                elif   typeDownload[1]=="NoSize":
                    await m.delete()
                    await m.reply(language['NoSize'])
                    return
            elif     typeDownload[1]=="NoFile":
                    await m.delete()
                    await m.reply(language['canotdiagnosis'])
                    return
            elif  typeDownload[1]=="BigFile": 
                    await m.delete()
                    await m.reply(language['BigFile'])     
                    return   
            elif   typeDownload[1]=="ErrInGet":
                await m.delete()
                await m.reply(language['getProblem'])
                return
            elif   typeDownload[1]=="NoSize":
                await m.delete()
                await m.reply(language['NoSize'])
                return

            
        except:
             
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
              
    else:
         
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))

   else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel()))    


@Client.on_message(filters.regex("SoundCloud 🟠"))
@Client.on_message(filters.regex("ساند کلاد 🟠"))
async def SoundCloudHandler(c: Client, m: Message):
    language =await Config.GetLang(m.from_user.id)
    if await lockChanel(c,m.from_user.id)==True: 
     await m.reply(language['MainSoundCloud'], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(language['Sound'], callback_data="SoungSoundCloud"), InlineKeyboardButton(language['PlayList'], callback_data="PlayListSoundCloud")]]))
    else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 

@Client.on_message(filters.regex("Spotify 🟢"))
@Client.on_message(filters.regex("اسپاتیفای 🟢"))
async def SpotifyHandler(c: Client, m: Message):
   language =await Config.GetLang(m.from_user.id)
   if await lockChanel(c,m.from_user.id)==True: 
    await m.reply(language['PleaseWait'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
    anwser = await pyromod.Chat.ask(text=language['SendLink'], self=m.chat)
    if anwser.text != language['cancelKey']:
        try:
            IdActivity = await Config.AddUserActivity(m.from_user.id, anwser.text, "spty")
            await m.delete()
            await m.reply( text=language['PleaseWait'], reply_markup=await Config.GetMainKey(m.from_user.id))
            s = Spotdl(client_id=CLIENTID,client_secret=CLIENTSECRET)
            song = Song.from_url(anwser.text)
            search_term = f" {song.name} {song.artist} {song.album_name}"
            videos_search = VideosSearch(search_term, limit =1 )
            link = videos_search.result()['result'][0]['link']
            yt = YouTube(link)
            yt.streams.filter(mime_type="audio/webm").first().download(filename=f"Music/{song.name}.mp3")
            mes =await m.reply_audio(audio=f"Music/{song.name}.mp3")
            os.remove(f"Music/{song.name}.mp3")
            await Config.UpdateUserActivity(IdActivity,mes.id,song.name)
            return
        except:
             
             await m.reply(language['getProblem'])
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
              
    else:
         
             await c.send_message(chat_id=m.from_user.id, text=language['Main'], reply_markup=await Config.GetMainKey(m.from_user.id))
   else:
       await m.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel()))    
@Client.on_callback_query()
async def CallBackHandler(c: Client, call: CallbackQuery):
    if "SelectLang_" in call.data:
        langKey = call.data.split('_')[1]
        await Config.AddLangToUser(call.from_user.id, langKey)
        language =await Config.GetLang(call.from_user.id)
        await call.message.delete()
        await c.send_message(chat_id=call.from_user.id, text=language['AfterSelectLang'], reply_markup=await Config.GetMainKey(call.from_user.id))
        return
    if "DownloadYoutube_" in call.data:
       language =await Config.GetLang(call.from_user.id)
       if await lockChanel(c,call.from_user.id)==True: 
        keyDownloader = call.data.split("_")
        Url = await Config.GetUrl(keyDownloader[2])
        await call.message.delete()
        await c.send_message(chat_id=call.from_user.id, text=language['PleaseWait'], reply_markup=await Config.GetMainKey(call.from_user.id))
        try:

            yt = YouTube(Url)

           

            
            if keyDownloader[3] == '4':
             
             streamViedo = yt.streams.get_by_resolution(keyDownloader[1])
             streamViedo.download(output_path=f"Media/YT")
             mes =await call.message.reply_video(video=f"Media/YT/{yt.title}.mp4",caption= yt.title, reply_markup=await Config.GetMainKey(call.from_user.id))
             await Config.UpdateUserActivity(keyDownloader[2],mes.id,yt.title)
             os.remove(f"Media/YT/{yt.title}.mp4")
            elif  keyDownloader[3] == '3':
                    streamViedo = yt.streams.get_audio_only()
                
                    streamViedo.download(output_path=f"Media/YT",filename=f'{yt.title}.mp3',)
                    mes =await call.message.reply_audio(audio=f"Media/YT/{yt.title}.mp3",caption= yt.title, reply_markup=await Config.GetMainKey(call.from_user.id))
                    await Config.UpdateUserActivity(keyDownloader[2],mes.id,yt.title)
                    os.remove(f"Media/YT/{yt.title}.mp3")
                    

           
        except:
            await call.message.reply(language['getProblem'])
       else:
        await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 
    if "Post" in call.data:
       language =await Config.GetLang(call.from_user.id)
       if await lockChanel(c,call.from_user.id)==True:  
        await call.message.delete()
        await Config.ChangeStepUser(call.from_user.id,'Post')
        await call.message.reply(language['SendLink'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        return
     
       
      
       else:
        await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 
        return
    if "Story" in call.data:
       language =await Config.GetLang(call.from_user.id)
       if await lockChanel(c,call.from_user.id)==True: 
        await call.message.delete()
        await Config.ChangeStepUser(call.from_user.id,'Story')
        await call.message.reply(language['SendLink'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        return
       
       else:
        await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 
        return
    if "GetUserInstagramDetails" == call.data:
      language =await Config.GetLang(call.from_user.id)
      if await lockChanel(c,call.from_user.id)==True:

        await call.message.delete()
        await Config.ChangeStepUser(call.from_user.id,'GetUserInstagramDetails')
        await call.message.reply(language['StoryQuestion'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        return
      
      else:
        await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel()))   
        return          
    if call.data == "SoungSoundCloud":
       language =await Config.GetLang(call.from_user.id)
       if await lockChanel(c,call.from_user.id)==True:
        await call.message.delete()
        await Config.ChangeStepUser(call.from_user.id,'SoungSoundCloud')
        await call.message.reply(language['SendLink'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        return
       else:
         await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 
         return
    if call.data == "PlayListSoundCloud":
         language =await Config.GetLang(call.from_user.id)
         if await lockChanel(c,call.from_user.id)==True:
          await call.message.delete()
          await Config.ChangeStepUser(call.from_user.id,'PlayListSoundCloud')

          await call.message.reply(language['SendLink'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
          return
         else:
          await call.message.reply(language['PleaseJoin'],reply_markup=InlineKeyboardMarkup(await Config.GetlistChanel())) 
          return




































        #  story =  instaloader.structures.Story.get_items(strotyItems)
        #  print(story)
        #  Loader.download_storyitem
        #  Loader.get_stories
        #  instaloader.structures.Story.get_items
        #  post = instaloader.structures.Story.get_items(
        #  Loader.context, anwser.text.split("/")[-2])
        #  await call.message.delete()
        #  await c.send_message(call.from_user.id,language['PleaseWait'])
        #  Loader.download_post(
        #  post, target=anwser.text.split("/")[-2])
        #  files = os.listdir(f"{anwser.text.split('/')[-2]}")

        # story = instaloader.structures.
        #   pass

        #    yt= YouTube('https://youtu.be/py-wsM3o7OQ?si=Yivi4nOPvLBWmWoV')
        #    video_streams = yt.streams.get_lowest_resolution()
        #    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        #                     tmp_filename = tmp_file.name
        #                     video_streams.download(output_path=None, filename=tmp_filename)
        #    await  m.reply_video(video=open(tmp_filename, 'rb'),caption="ARS Is Developer this @AR_S_83 (: \n Who are you ")
    if "ARSForwarder_" in  call.data :
        res = call.data.split("_")[1]
        data = await Config.Forward(int(res)) 
        print(data)
        if "," in data:
         sb = data.split(",")
         for s in sb:
          await c.forward_messages(call.from_user.id,call.from_user.id,int(s))
        else:    
         await c.forward_messages(call.from_user.id,call.from_user.id,int(data))
    if "DeleteItem_" in call.data:
        data = call.data.split("_")[1]
        await Config.DeleteItem(int(data))
        await call.edit_message_reply_markup(reply_markup= InlineKeyboardMarkup(await Config.GetUserDownloaded(call.from_user.id)))
    if "lockchanel"  in call.data:
        lang =await Config.GetLang(call.from_user.id)
        btn =  await Config.GetLockCahnel()
        btn.append((f"{lang['AddChanelLock']}","AddNewChanel"))
        btn.append((f"{lang['Back']}","BackToMenuManage"))
        await call.edit_message_text(lang['DesChanel'],reply_markup=ikb(array_chunk(btn,2)))  
    if "BackToMenuManage" in call.data:
      if await Config.GetDataConfig("Admin") == call.from_user.id  :
       language =await Config.GetLang(call.from_user.id)
       await call.edit_message_text(language['ManageDes'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(language['messegeToAll'],callback_data="publicMessage"),InlineKeyboardButton(language['lock'],callback_data="lockchanel")]]))
    if "AddNewChanel" in call.data:
        language =await Config.GetLang(call.from_user.id)
        await call.message.reply(language['PleaseWait'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        await call.message.delete()
        anwser = await pyromod.Chat.ask(text=language['EnterNameChanel'], self=call.message.chat)
        Name = ""
        Id = ""
        if anwser.text != language['cancelKey']:
            Name =anwser.text
            anwser = await pyromod.Chat.ask(text=language['EnterID'], self=call.message.chat)
            if anwser.text != language['cancelKey']:
                Id =anwser.text
                await Config.AddChanel(Name,Id)
                Id =""
                Name =""
                btn =  await Config.GetLockCahnel()
                btn.append((f"{language['AddChanelLock']}","AddNewChanel"))
                btn.append((f"{language['Back']}","BackToMenuManage"))
                await call.message.reply("✅")
                await call.message.reply(language['DesChanel'],reply_markup=ikb(array_chunk(btn,2)))  
    if "DeleteCahnel_" in call.data:
        data= call.data.split("_")[1]
        lang =await Config.GetLang(call.from_user.id)

        btn =  await Config.DeleteChanel(int(data))    
        btn.append((f"{lang['AddChanelLock']}","AddNewChanel"))
        btn.append((f"{lang['Back']}","BackToMenuManage"))         
        await call.edit_message_reply_markup(ikb(array_chunk(btn,2)))
    if call.data == "InfoBot" :
        if await Config.GetDataConfig("Admin") == call.from_user.id  :
            res = await Config.GetUsersInfo()
            await call.edit_message_text(f"تعداد کاربران : {res}")
    if call.data =="publicMessage":
        await call.message.delete()
        language =await Config.GetLang(call.from_user.id)
        await call.message.reply(language['PleaseWait'], reply_markup=ReplyKeyboardMarkup(
        [[language['cancelKey']]], resize_keyboard=True))
        await call.message.delete()
        anwser = await pyromod.Chat.ask(text=language['EnterText'], self=call.message.chat)
        
        if anwser.text != language['cancelKey']:
             await call.message.reply(language['Started'])
        
             for Id  in await Config.GetAllUser():
              try:
                await c.send_message(chat_id=Id[0],text=anwser.text)
              except:
                  ...  
