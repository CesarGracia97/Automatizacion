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