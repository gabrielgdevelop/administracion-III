import os
import tempfile
from datetime import datetime
from apps.morbilidad.services.excel_processor import ExcelMorbilidadService

def handle_excel_document(message, bot):
    now = datetime.now()
    if now.weekday() == 4 and now.hour >= 15:
        bot.reply_to(message, "⚠️ Cierre semanal activo. No se aceptan más reportes de morbilidad por esta semana.")
        return

    file_name = message.document.file_name
    if not file_name.endswith(('.xlsx', '.xls')):
        bot.reply_to(message, "❌ Error: El sistema solo procesa archivos Excel (.xlsx).")
        return

    bot.reply_to(message, "⏳ Leyendo estructura del archivo y procesando datos...")

    temp_path = ""
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # SOLUCIÓN: Usar la carpeta temporal nativa del sistema operativo (Windows o Linux)
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"morb_{message.message_id}_{file_name}")
        
        with open(temp_path, 'wb') as f:
            f.write(downloaded_file)
            
        inserted_count = ExcelMorbilidadService.process_file(temp_path)
        bot.reply_to(message, f"✅ ¡Exitoso! Se migraron {inserted_count} pacientes a la Base de Datos Local. Pendientes de validación por el Estadístico.")
        
    except ValueError as e:
        bot.reply_to(message, f"❌ Error de formato en Excel: {str(e)}")
    except Exception as e:
        # SOLUCIÓN: Mostrar el error real en la terminal y en Telegram para depurar
        error_msg = str(e)
        print(f"🔥 ERROR CRÍTICO CAPTURADO: {error_msg}")
        bot.reply_to(message, f"❌ Error interno capturado: {error_msg}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)