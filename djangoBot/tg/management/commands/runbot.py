from django.core.management import BaseCommand

from telegram.ext import Updater , CommandHandler, MessageHandler, Filters ,CallbackQueryHandler
from config.settings import TOKEN
from tg.views import start,for_inline ,contact ,locations ,for_message

class Command(BaseCommand):
	def handle(self , *args , **kwargs):
		updater=Updater(TOKEN)
		updater.dispatcher.add_handler(CommandHandler('start' , start ))
		updater.dispatcher.add_handler(CallbackQueryHandler(for_inline))
		updater.dispatcher.add_handler(MessageHandler(Filters.text , for_message))
		updater.dispatcher.add_handler(MessageHandler(Filters.contact , contact))
		updater.dispatcher.add_handler(MessageHandler(Filters.location , locations))
		updater.start_polling()
		updater.idle()
