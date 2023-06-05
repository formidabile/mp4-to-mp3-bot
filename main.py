import moviepy.editor
from pytube import YouTube
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Функция-обработчик для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который умеет переводить видео в аудио. Отправь ссылку на видео, и я сделаю тебе аудио.")

# Функция-обработчик для простого сообщения
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[{datetime.now()}] Bot got message from @{update.message.chat.username}...")
    if ("youtube.com/watch?v=" in update.message.text and 'youtube.com/watch?v=' != update.message.text)\
            or ("youtu.be/" in update.message.text and 'youtu.be/' != update.message.text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Бот переводит видео в mp3-файл. Пожалуйста, подожди немного...')
        try:
            title = download_video(update.message.text)
            mp4_to_mp3(title)
            audio = open(f"audio/{title}.mp3", 'rb')
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
        except OSError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Что-то пошло не так. Попробуй еще раз')
        except ConnectionError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Что-то пошло не так. Попробуй еще раз')

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Это не видео. Попробуй еще раз')
    print(f"[{datetime.now()}] Bot handled message...")


def download_video(url):
    yt = YouTube(url=url)
    out_video = yt.streams.filter(progressive=True, file_extension="mp4").first().download()
    #os.rename(out_video, f"source/{yt.title}.mp4")
    return yt.title

def mp4_to_mp3(name):
    video = moviepy.editor.VideoFileClip(f"{name}.mp4")
    audio = video.audio
    audio.write_audiofile(f"audio/{name}.mp3")

def main():
    # Создаем экземпляр класса ApplicationBuilder и передаем ему токен вашего бота
    updater = ApplicationBuilder().token('MY-TOKEN').build()

    # Регистрируем обработчик для команды /start
    start_handler = CommandHandler('start', start)
    updater.add_handler(start_handler)

    # Регистрируем обработчик для простых сообщений
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    updater.add_handler(echo_handler)

    print(f"[{datetime.now()}] Bot has been launched...")
    # Запускаем бота
    updater.run_polling()

    print(f"[{datetime.now()}] Bot has been stopped...")
    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()

    #url = input("Enter the link on video you want to download: ")
    #new_name = input("Enter the name of video: ")
    #if download_video(url=url, name=new_name) == -1:
    #    print("Oops... Something went wrong")
    #    return -1
    #print(yt.title)

    #mp4_to_mp3(new_name)


if __name__ == '__main__':
    main()