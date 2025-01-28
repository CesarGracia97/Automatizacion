import calendar
from datetime import datetime


class Tools:
    @staticmethod
    def mounthsTranslateGenerator(months):
        # Diccionario de traducción de meses
        MONTHS_TRANSLATION = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        # Crear lista con nombre traducido y detalles
        translated_months = [
            {
                "nombre": f"{MONTHS_TRANSLATION[month['mes']]} {month['ano']}",
                "mes": month["mes"],
                "ano": month["ano"]
            }
            for month in months
        ]

        return translated_months

    @staticmethod
    def obtener_ultimo_dia_mes(fecha: datetime) -> str:
        # Obtenemos el año y el mes de la fecha proporcionada
        ano = fecha.year
        mes = fecha.month

        # Usamos calendar.monthrange para obtener el último día del mes
        _, ultimo_dia = calendar.monthrange(ano, mes)

        # Devolvemos la fecha en formato 'YYYY-MM-DD'
        return f"{ano}-{mes:02d}-{ultimo_dia:02d}"