# apps/telegram_bot/management/commands/run_bot.py
from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from apps.telegram_bot.handlers.document_handler import handle_excel_document

class Command(BaseCommand):
    help = 'Levanta el servicio del Bot de Telegram en el backend de Django'

    def handle(self, *args, **kwargs):
        # Asegúrate de agregar TELEGRAM_BOT_TOKEN en tu base.py o env variables
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

        @bot.message_handler(content_types=['document'])
        def on_document(message):
            handle_excel_document(message, bot)

        self.stdout.write(self.style.SUCCESS('Servicio de Telegram iniciado correctamente. Escuchando peticiones locales...'))
        
        # Mantiene el script corriendo en Linux (tu Debian 12)
        bot.infinity_polling()