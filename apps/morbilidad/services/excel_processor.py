# apps/morbilidad/services/excel_processor.py
import pandas as pd
from django.db import transaction
from apps.catalogs.models.year import Year
from apps.catalogs.models.month import Month
from apps.catalogs.models.week import Week
from apps.morbilidad.models.detail_morbilidad import DetailMorbilidad
from apps.morbilidad.models.morbilidad import Morbilidad

class ExcelMorbilidadService:
    EXPECTED_COLUMNS = ['Cedula', 'Nombre', 'Apellido', 'Edad', 'Diagnostico', 'Fecha']

    @classmethod
    def process_file(cls, file_path: str) -> int:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip() # Limpiar espacios en blanco accidentales
        
        if not all(col in df.columns for col in cls.EXPECTED_COLUMNS):
            raise ValueError(f"Formato inválido. Se requieren las columnas: {', '.join(cls.EXPECTED_COLUMNS)}")

        registros_creados = 0
        
        # Transacción atómica: si falla un registro (ej. formato de fecha erróneo), 
        # se revierte todo el archivo para evitar bases de datos corruptas.
        with transaction.atomic():
            for _, row in df.iterrows():
                cls._insert_record(row)
                registros_creados += 1
                
        return registros_creados

    @classmethod
    def _insert_record(cls, row):
        fecha_atencion = pd.to_datetime(row['Fecha']).date()
        
        detalle = DetailMorbilidad.objects.create(
            cedula=str(row['Cedula']).strip(),
            nombre=str(row['Nombre']).strip(),
            apellido=str(row['Apellido']).strip(),
            edad=int(row['Edad']),
            diagnostico=str(row['Diagnostico']).strip(),
            fecha=fecha_atencion
        )

        year_str = str(fecha_atencion.year)
        month_name = fecha_atencion.strftime('%B')
        week_num = fecha_atencion.isocalendar()[1]

        year_obj, _ = Year.objects.get_or_create(name=year_str)
        month_obj, _ = Month.objects.get_or_create(name=month_name, year=year_obj)
        week_obj, _ = Week.objects.get_or_create(number=week_num, month=month_obj)

        Morbilidad.objects.create(
            morbilidad_detalle=detalle,
            week=week_obj,
            month=month_obj,
            year=year_obj,
            estado='Pendiente'
        )