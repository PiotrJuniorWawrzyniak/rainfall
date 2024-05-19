import os.path
from datetime import datetime, timedelta
from requests import get


class WeatherForecast:
    def __init__(self, file_name='informacja_o_opadach.txt'):
        self.file_name = file_name
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.file_name):
            return {}
        with open(self.file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        data = {}
        for line in lines:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                date, info = parts
                data[date] = info
        return data

    def _save_data(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            for date, info in self.data.items():
                file.write(f'{date}: {info}\n')

    @staticmethod
    def download_data(latitude, longitude, searched_date):
        url = (
            f'https://api.open-meteo.com/v1/forecast?latitude={latitude}'
            f'&longitude={longitude}'
            f'&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon'
            f'&start_date={searched_date}&end_date={searched_date}'
        )
        response = get(url)
        return response.json()

    @staticmethod
    def check_precipitation(data, latitude, longitude, searched_date):
        if 'hourly' in data and 'rain' in data['hourly']:
            hourly_precipitation = data['hourly']['rain']
            if any(precipitation > 0.0 for precipitation in hourly_precipitation):
                return (f'Dnia {searched_date} pod szerokością geograficzną {latitude} '
                        f'i długością geograficzną {longitude} wystąpią opady.')
            else:
                return (f'Dnia {searched_date} pod szerokością geograficzną {latitude} '
                        f'i długością geograficzną {longitude} nie wystąpią opady.')
        return (f'Nie stwierdzono, czy dnia {searched_date} pod szerokością geograficzną {latitude} '
                f'i długością geograficzną {longitude} wystąpią opady.')

    def __setitem__(self, date, info):
        self.data[date] = info
        self._save_data()

    def __getitem__(self, date):
        return self.data.get(date, None)

    def __iter__(self):
        return iter(self.data.keys())

    def items(self):
        return ((date, info) for date, info in self.data.items())


def enter_data():
    while True:
        try:
            latitude = float(input('Podaj szerokosc geograficzna (-90 do 90): '))
            if -90 <= latitude <= 90:
                break
            else:
                print('Blad! Wprowadz wartosc z zakresu od -90 do 90.')
        except ValueError:
            print('Blad! Wprowadz poprawna wartosc liczbowa.')

    while True:
        try:
            longitude = float(input('Podaj dlugosc geograficzna (-180 do 180): '))
            if -180 <= longitude <= 180:
                break
            else:
                print('Blad! Wprowadz wartosc z zakresu od -180 do 180.')
        except ValueError:
            print('Blad! Wprowadz poprawna wartosc liczbową.')

    current_date = datetime.now().date()
    while True:
        searched_date_str = input('Podaj date w formacie YYYY-MM-DD: ')
        if searched_date_str:
            try:
                searched_date = datetime.strptime(searched_date_str, '%Y-%m-%d').date()
                break
            except ValueError:
                print('Blad! Wprowadz date w formacie YYYY-MM-DD.')
        else:
            searched_date = current_date + timedelta(days=1)
            break

    return latitude, longitude, searched_date


def main():
    latitude, longitude, searched_date = enter_data()
    weather_forecast = WeatherForecast()

    searched_date_str = searched_date.strftime('%Y-%m-%d')
    if searched_date_str in weather_forecast:
        print(weather_forecast[searched_date_str])
    else:
        data = WeatherForecast.download_data(latitude, longitude, searched_date_str)
        info = WeatherForecast.check_precipitation(data, latitude, longitude, searched_date_str)
        weather_forecast[searched_date_str] = info
        print(info)


if __name__ == '__main__':
    print('>>> PROGRAM INFORMUJACY O OPADACH W DANYM MIEJSCU I DNIU <<<')
    main()
