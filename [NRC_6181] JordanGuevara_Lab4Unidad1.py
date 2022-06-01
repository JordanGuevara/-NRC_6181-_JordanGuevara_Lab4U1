import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class HolidayEcuador(HolidayBase):
    """
    La clase que representa el feriado en Ecuador por provincia (HolidayEcuador)
    Su objetivo general es determinar si la 
    fecha específica es vacaciones lo más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HolidayBase)
    ----------
    prov: str
        código de provincia según ISO3166-2
    Metodos
    -------
    __init__(self, plate, date, time, online=False):
        Construye todos los atributos necesarios para el objeto HolidayEcuador.
    _populate(self, year):
        Hace una devolucion si la fecha sale feriado o no
    """     
    # ISO 3166-2 códigos para las subdivisiones principales, 
    # llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO add more provinces

    def __init__(self, **kwargs):
        """
        Se construye todos los atributos necesarios para el objeto HolidayEcuador.
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Comprueba si una fecha es feriado o no
        
        Parametros
        ----------
        year : str
            año de una fecha
        Returns
        -------
        Devuelve verdadero si una fecha es un día festivo, de lo contrario, se muestra como verdadero.
        """                    
        # Día de Año Nuevo  
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Navidad
        self[datetime.date(year, DEC, 25)] = "Feliz Navidad [Merry Christmas]"
        
        # semana santa
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas (Dia del Conejo de Pascua) [Easter Day]"
        
        # Carnival
        total_lent_days = 46
        self[easter(year) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Labor day
        name = "Día Nacional del Trabajo [Labour Day]"
         # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al viernes o lunes inmediato anterior
        # respectivamente
        if year > 2015 and datetime.date(year, MAY, 1).weekday() in (5,1):
            self[datetime.date(year, MAY, 1) - datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio sera para el lunes siguiente
        elif year > 2015 and datetime.date(year, MAY, 1).weekday() == 6:
            self[datetime.date(year, MAY, 1) + datetime.timedelta(days=1)] = name
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # se moverá al viernes de esa semana
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, MAY, 1) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, MAY, 1)] = name
        
        # Batalla de Pichincha, las reglas son las mismas que el día del trabajo
        name = "Batalla del Pichincha [Pichincha Battle]"
        if year > 2015 and datetime.date(year, MAY, 24).weekday() in (5,1):
            self[datetime.date(year, MAY, 24).weekday() - datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, MAY, 24).weekday() == 6:
            self[datetime.date(year, MAY, 24) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, MAY, 24).weekday() in (2,3):
            self[datetime.date(year, MAY, 24) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, MAY, 24)] = name        
        
        # First Cry of Independence, the rules are the same as the labor day
        name = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and datetime.date(year, AUG, 10).weekday() in (5,1):
            self[datetime.date(year, AUG, 10)- datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, AUG, 10).weekday() == 6:
            self[datetime.date(year, AUG, 10) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, AUG, 10).weekday() in (2,3):
            self[datetime.date(year, AUG, 10) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, AUG, 10)] = name       
        
         # Independencia de Guayaquil, las reglas son las mismas que el día del trabajo
        name = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and datetime.date(year, OCT, 9).weekday() in (5,1):
            self[datetime.date(year, OCT, 9) - datetime.timedelta(days=1)] = name
        elif year > 2015 and datetime.date(year, OCT, 9).weekday() == 6:
            self[datetime.date(year, OCT, 9) + datetime.timedelta(days=1)] = name
        elif year > 2015 and  datetime.date(year, MAY, 1).weekday() in (2,3):
            self[datetime.date(year, OCT, 9) + rd(weekday=FR)] = name
        else:
            self[datetime.date(year, OCT, 9)] = name        
        
        # Dia de lso difuntos
        namedd = "Día de los difuntos [Dia de los muertos]" 
        # Independence de Cuenca
        nameic = "Independencia de Cuenca [Independence of Cuenca]"
         #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en días corridos,
        #se aplicarán las siguientes reglas:
        if (datetime.date(year, NOV, 2).weekday() == 5 and  datetime.date(year, NOV, 3).weekday() == 6):
            self[datetime.date(year, NOV, 2) - datetime.timedelta(days=1)] = namedd
            self[datetime.date(year, NOV, 3) + datetime.timedelta(days=1)] = nameic     
        elif (datetime.date(year, NOV, 3).weekday() == 2):
            self[datetime.date(year, NOV, 2)] = namedd
            self[datetime.date(year, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(year, NOV, 3).weekday() == 3):
            self[datetime.date(year, NOV, 3)] = nameic
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = namedd
        elif (datetime.date(year, NOV, 3).weekday() == 5):
            self[datetime.date(year, NOV, 2)] =  namedd
            self[datetime.date(year, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(year, NOV, 3).weekday() == 0):
            self[datetime.date(year, NOV, 3)] = nameic
            self[datetime.date(year, NOV, 2) + datetime.timedelta(days=2)] = namedd
        else:
            self[datetime.date(year, NOV, 2)] = namedd
            self[datetime.date(year, NOV, 3)] = nameic  
            
       # Fundación de Quito, aplica solo para la provincia de Pichincha,
        # las reglas son las mismas que el día del trabajo
        name = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and datetime.date(year, DEC, 6).weekday() in (5,1):
                self[datetime.date(year, DEC, 6) - datetime.timedelta(days=1)] = name
            elif year > 2015 and datetime.date(year, DEC, 6).weekday() == 6:
                self[(datetime.date(year, DEC, 6).weekday()) + datetime.timedelta(days=1)] =name
            elif year > 2015 and  datetime.date(year, DEC, 6).weekday() in (2,3):
                self[datetime.date(year, DEC, 6) + rd(weekday=FR)] = name
            else:
                self[datetime.date(year, DEC, 6)] = name

class PicoPlaca:
    """
   La clase que representara vehículo.
    medida de restricción (Pico y Placa) 
    - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributos
    ----------
    plate : str 
        El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos 
        caracteres que identifican e individualizan el vehículo respecto de los demás;
        
        El formato utilizado es
        XX-YYYY or XXX-YYYY, 
        donde X es una letra mayúscula e Y es un dígito.
    fecha: calle
        Fecha en la que el vehículo pretende transitar
        esta siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
    tiempo: calle
        tiempo en que el vehículo pretende transitar
        esta siguiendo el formato
        HH:MM: por ejemplo, 08:35, 19:30
    en línea: booleano, opcional
        si en línea == Verdadero, se utilizará la API de días festivos abstractos
    Métodos
    -------
    __init__(self, plate, date, time, online=False):
        Construye lo necesario para los atributos mencionados.
        para que el objeto PicoPlaca.
    plato (asi mismo):
        Obtiene el valor de placa como atributo
    placa (automovil, valor):
        Establece el atributo valor de placa
    fecha (uno mismo):
        Obtiene el atributo de fecha como valor
    fecha (auto, valor):
        Se establece el valor del atributo de fecha
    tiempo (asi mismo):
        Obtiene el valor del atributo de tiempo
    tiempo (asi mismo, valor):
        Establece el valor del atributo de tiempo
    __find_day(yo, fecha):
        Devuelve el día a partir de la fecha: por ejemplo, miércoles
    __is_forbidden_time(self, check_time):
        Devuelve Verdadero(True) si el tiempo que se proporciona está dentro de las horas pico prohibidas, de otra manera, sera Falso(False)
    __es_vacaciones:
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
    predecir (auto):
        Devuelve True si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora especificadas, de lo contrario, False
    """ 
    #Days of the week
    __days = [
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo"]

    # Dictionary that holds the restrictions inf the form {day: forbidden last digit}
    __restrictions = {
            "Lunes": [1, 2],
            "Martes": [3, 4],
            "Miercoles": [5, 6],
            "Jueves": [7, 8],
            "Viernes": [9, 0],
            "Sabado": [],
            "Domingo": []}

    def __init__(self, plate, date, time, online=False):
        """
       Se construye todos los atributos que son necesarios para el objeto o clase PicoPlaca.
        
        Parameteros
        ----------
            placa : calle
                El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
                caracteres que identifican e individualizan el vehículo respecto de los demás;
                El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito.
            fecha: calle
                Fecha en la que el vehículo pretende transitar
                Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
            tiempo: calle
                tiempo en que el vehículo pretende transitar
                Sigue el formato HH:MM: por ejemplo, 08:35, 19:30
            en línea: booleano, opcional
                si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)               
        """                
        self.plate = plate
        self.date = date
        self.time = time
        self.online = online


    @property
    def plate(self):
        """Obtiene el valor del atributo de placa"""
        return self._plate


    @plate.setter
    def plate(self, value):
        """
       Establece el valor del atributo de la placa
        Parameteros
        ----------
        Valor: str
        
        Aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el correspondiente formato que es
            XX-YYYY o XXX-YYYY,
            donde X es una letra mayúscula e Y es un dígito
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', value):
            raise ValueError(
                'La placa debe tener el siguiente formato: XX-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito')
        self._plate = value


    @property
    def date(self):
        """Obtiene el valor del atributo de fecha"""
        return self._date


    @date.setter
    def date(self, value):
        """
        Establece el valor del atributo de fecha
        Parameteros
        ----------
        Valor : str
        
        Aumenta
        ------
        ValorError
            Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el formato correspondiente: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._date = value
        

    @property
    def time(self):
        """Obtiene el valor del atributo de tiempo"""
        return self._time


    @time.setter
    def time(self, value):
        """
        Establece el valor de un atributo de tiempo
        Parameteros
        ----------
        Valor: str
        
        Aumenta
        ------
        ValorError
           Si la cadena de caracter que fue asignada no tiene el formato HH:MM (e.g., 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'La hora debe tener el siguiente formato de aparicion: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._time = value


    def __find_day(self, date):
        """
        Encuentrar el día por la fecha: por ejemplo, Jueves
        Parámetros
        ----------
        fecha: calle
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        Devoluciones
        -------
        Devuelvera el día en el punto de partida de la fecha como una cadena de caracteres
        """        
        d = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return self.__days[d]


    def __is_forbidden_time(self, check_time):
        """
         Comprueba si el tiempo proporcionado está dentro de las horas pico prohibidas,
        donde las horas pico son: 07:00 - 09:30 y 16:00 - 19:30
        Parámetros
        ----------
        check_time : str
            Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
        Devoluciones
        -------
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario, False
        """           
        t = datetime.datetime.strptime(check_time, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __is_holiday(self, date, online):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
        si en línea == Verdadero, utilizará una API REST, de lo contrario, mostrara los días festivos del año encontrados
        
        Parámetros
        ----------
        fecha: calle
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        en línea: booleano, opcional
            si en línea == Verdadero, se utilizará la API de días festivos abstractos
        Devoluciones
        -------
        Devuelve Verdadero (True) si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) que es un dia festivo en Ecuador, caso contrario, sera Falso(False)
        """            
        y, m, d = date.split('-')

        if online:
            # API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            # 1 solicitud por segundo
            # Conseguir la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones, obtenemos una matriz vacía
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return date in ecu_holidays


    def predict(self):
        """
        Comprueba si el siguiente vehículo con la placa seleccionada puede estar en la carretera en la fecha y hora proporcionada según el reglamento de Pico y Placa:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf    
        Returns
        -------
        Returns 
        Verdadero si el carro con
        la placa especificada puede estar en el camino
        en la fecha y hora que se muestra, de lo contrario sera Falso
        """
        # Comprobar si la fecha es un día festivo
        if self.__is_holiday(self.date, self.online):
            return True

        # Consultar vehículos excluidos de la restricción según la segunda letra de la placa o si se utilizan sólo dos letras
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.plate[1] in 'AUZEXM' or len(self.plate.split('-')[0]) == 2:
            return True

        # Compruebe si el tiempo comprobado no está en las horas pico restringidas
        if not self.__is_forbidden_time(self.time):
            return True

        day = self.__find_day(self.date)  # Buscar un día de la semana a partir de la fecha ingresada
        # Verifique si el último dígito de la placa no está restringido en este particular dia
        if int(self.plate[-1]) not in self.__restrictions[day]:
            return True

        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Pico y Placa Quito Predictor:  Verifique si el vehículo con la placa proporcionada puede estar en la carretera en la fecha y hora correspondiente')
    parser.add_argument(
        '-o',
        '--online',
        action='tienda_verdadero',
        help='usar la API abstract\ vacaciones')
    parser.add_argument(
        '-l',
        '--lámina',
        required=True,
        help='la placa del vehículo: XXX-YYYY o XX-YYYY, donde X es una letra mayuscula e Y es un digito')
    parser.add_argument(
        '-f',
        '--fecha',
        required=True,
        help='la fecha a comprobar: AAAA-MM-DD')
    parser.add_argument(
        '-t',
        '--time',
        required=True,
        help='la hora a comprobar: HH:MM')
    args = parser.parse_args()


    pyp = PicoPlaca(args.plate, args.date, args.time, args.online)

    if pyp.predict():
        print(
            'El vehículo con la siguiente placa {} PUEDE estar en la siguiente carretera que es el {} y {}.'.format(
                args.plate,
                args.date,
                args.time))
    else:
        print(
            'El vehículo con matrícula {} NO DEBE estar en la carretera de {} a {}.'.format(
                args.plate,
                args.date,
                args.time))