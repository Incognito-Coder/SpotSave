import urllib.request
from SpotBot.spotify import MusicDownloader, AlbumDownloader
from pyrogram.types.bots_and_keyboards.reply_keyboard_markup import ReplyKeyboardMarkup
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import ReplyKeyboardRemove
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.types import Message
import SpotBot.spotify as spotify
import os
from SpotBot.config import Configs
import logging

logging.basicConfig(level=logging.DEBUG)

icbot = Client('SpotSaveBot', bot_token=Configs.API_KEY,
               api_id=Configs.API_ID, api_hash=Configs.API_HASH)

MAIN_KEYS = ReplyKeyboardMarkup(
    [['Download as FLAC', 'Download as MP3'], ['Album Downloader']], resize_keyboard=True)


@icbot.on_message(filters.private & filters.command(['start', 'Start'], '/'))
async def hello(Client, msg: Message):
    await msg.reply_text(f'Hello {msg.from_user.first_name}\nWelcome to **{Configs.BOT_NAME}** Bot.', reply_markup=MAIN_KEYS)


@icbot.on_message(filters.private & filters.command(['about', 'About', 'help', 'Help'], ['/', '!', '#']))
async def about(Client, msg: Message):
    await msg.reply_text(f'Developer : {Configs.OWNER}\n**Don\'t forget join in our channel.**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Dev Channel', url=Configs.CHANNEL_URL)]]))


@icbot.on_message(filters.private & filters.regex('Download as MP3'))
async def mp3dl(Client, msg: Message):
    status = None
    try:
        member = await icbot.get_chat_member(Configs.CHANNEL, msg.from_user.id)
        status = member.status.value
    except UserNotParticipant:
        pass
    if not status in ['member', 'owner', 'administrator']:
        await msg.reply_text(f'You must be a member of our channel\n@{Configs.CHANNEL}',
                             reply_markup=ReplyKeyboardRemove(True))
    else:
        inputs = await Client.ask(chat_id=msg.from_user.id, text='Paste Spotify song url or enter search query\nExample: **Cool - Dua Lipa**\nAbort /cancel', reply_markup=ReplyKeyboardRemove(True))
        if not inputs.text == '/cancel':
            await msg.reply_text('__Searching for result.__')
            await MusicDownloader(
                query=inputs.text, format='mp3')
            await msg.reply_text(f'{spotify.Scaption}\n\n**Download of {spotify.Filename} complete.**\n__Uploading to you ...__', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Album Cover', url=spotify.Scover)]]))
            await msg.reply_audio(audio=spotify.Filename, caption=f'🎧 Downloaded By [{Configs.BOT_NAME}](https://telegram.me/{Configs.BOT_UNAME}) Bot', reply_markup=MAIN_KEYS)
            os.remove(spotify.Filename)
        else:
            await msg.reply_text(f'You\'ve backed to main.', reply_markup=MAIN_KEYS)


@icbot.on_message(filters.private & filters.regex('Download as FLAC'))
async def flacdl(Client, msg: Message):
    status = None
    try:
        member = await icbot.get_chat_member(Configs.CHANNEL, msg.from_user.id)
        status = member.status.value
    except UserNotParticipant:
        pass
    if not status in ['member', 'owner', 'administrator']:
        await msg.reply_text(f'You must be a member of our channel\n@{Configs.CHANNEL}',
                             reply_markup=ReplyKeyboardRemove(True))
    else:
        inputs = await Client.ask(chat_id=msg.from_user.id, text='FLAC Downloader\nPaste Spotify song url or enter search query\nExample: **Cool - Dua Lipa**\nAbort /cancel', reply_markup=ReplyKeyboardRemove(True))
        if not inputs.text == '/cancel':
            await msg.reply_text('__Searching for result.__')
            await MusicDownloader(
                query=inputs.text, format='flac')
            await msg.reply_text(f'{spotify.Scaption}\n\n**Download of {spotify.Filename} complete.**\n__Uploading to you ...__', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Album Cover', url=spotify.Scover)]]))
            urllib.request.urlretrieve(spotify.Scover, 'thumb.jpg')
            await msg.reply_audio(audio=spotify.Filename, caption=f'🎧 Downloaded By [{Configs.BOT_NAME}](https://telegram.me/{Configs.BOT_UNAME}) Bot', thumb='thumb.jpg', performer=spotify.Sartist, reply_markup=MAIN_KEYS)
            os.remove(spotify.Filename)
            os.remove('thumb.jpg')
            os.remove(spotify.IFilename)
        else:
            await msg.reply_text(f'You\'ve backed to main.', reply_markup=MAIN_KEYS)


@icbot.on_message(filters.private & filters.regex('Album Downloader'))
async def album(Client, msg: Message):
    status = None
    try:
        member = await icbot.get_chat_member(Configs.CHANNEL, msg.from_user.id)
        status = member.status.value
    except UserNotParticipant:
        pass
    if not status in ['member', 'owner', 'administrator']:
        await msg.reply_text(f'You must be a member of our channel\n@{Configs.CHANNEL}',
                             reply_markup=ReplyKeyboardRemove(True))
    else:
        inputs = await Client.ask(chat_id=msg.from_user.id, text='Album Downloader\nPaste Spotify album url\nAbort /cancel', reply_markup=ReplyKeyboardRemove(True))
        if not inputs.text == '/cancel':
            await msg.reply_text('__Searching for result.__')
            await AlbumDownloader(inputs.text)
            await msg.reply_photo(photo=spotify.Scover, caption=f'Name : {spotify.Sname}\nArtists : {spotify.Sartist}', reply_markup=ReplyKeyboardRemove(True))
            await msg.reply_document(document=spotify.Sname+'.zip', caption=f'🎧 Downloaded By [{Configs.BOT_NAME}](https://telegram.me/{Configs.BOT_UNAME}) Bot', reply_markup=MAIN_KEYS)
            os.remove(spotify.Sname+'.zip')
        else:
            await msg.reply_text(f'You\'ve backed to main.', reply_markup=MAIN_KEYS)
icbot.run()
