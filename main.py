import os.path
from datetime import datetime, timedelta
from requests import get


def give_data():
    while True:
        try:
            latitude = float(input('Podaj szerokosc geograficzna (-90 do 90): '))
            if -90 <= latitude <= 90:
                break
            else:
                print('Blad: Wprowadz wartosc z zakresu od -90 do 90.')
        except ValueError:
            print('Blad: Wprowadz poprawna wartosc liczbowa.')

    while True:
        try:
            longitude = float(input('Podaj dlugosc geograficzna (-180 do 180): '))
            if -180 <= longitude <= 180:
                break
            else:
                print('Blad: Wprowadz wartosc z zakresu od -180 do 180.')
        except ValueError:
            print('Blad: Wprowadz poprawna wartosc liczbową.')

    current_date = datetime.now().date()
    searched_date = input('Podaj date w formacie YYYY-MM-DD: ')
    if not searched_date:
        searched_date = current_date + timedelta(days=1)

    return latitude, longitude, searched_date


def download_data(latitude, longitude, searched_date):
    url = (
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}'
        f'&longitude={longitude}'
        f'&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon'
        f'&start_date={searched_date}&end_date={searched_date}'
    )

    response = get(url)
    return response


def check_precipitation(response, latitude, longitude, searched_date):
    data = response.json()
    hourly_precipitation = data['hourly']['rain']

    # Sprawdzenie wystepowanie jakichkolwiek opadow danego dnia
    if any(precipitation > 0.0 for precipitation in hourly_precipitation):
        return (f'Dnia {searched_date} pod szerokoscia geograficzna {latitude} '
                f'i dlugoscia geograficzna {longitude} wystapia opady.')

    # Sprawdzenie braku jakichkolwiek opadow danego dnia
    elif all(precipitation == 0.0 for precipitation in hourly_precipitation):
        return (f'Dnia {searched_date} pod szerokoscia geograficzna {latitude} '
                f'i dlugoscia geograficzna {longitude} nie wystapia opady.')

    else:
        return (f'Nie stwierdzono, czy dnia {searched_date} pod szerokoscia geograficzna {latitude} '
                f'i dlugoscia geograficzna {longitude} wystapia opady.')


def save_to_file(file_name, content):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(content + '\n')
    print(content)
    print(f'Informacje o opadach zostaly zapisane do pliku {file_name}.')


def main():
    latitude, longitude, searched_date = give_data()

    # Sprawdzenie, czy w pliku sa juz zapisane informacje o opadach w danym miejscu i dniu
    file_name = 'informacja_o_opadach.txt'
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if searched_date.strftime('%Y-%m-%d') in line and str(latitude) in line and str(longitude) in line:
                    print(line.strip())
                    return

    # Zapytanie do API, jesli dane nie sa zapisane w pliku
    response = download_data(latitude, longitude, searched_date)
    precipitation_info = check_precipitation(response, latitude, longitude, searched_date)
    save_to_file('informacja_o_opadach.txt', precipitation_info)


if __name__ == '__main__':
    print('>>> PROGRAM INFORMUJACY O OPADACH W DANYM MIEJSCU I DNIU <<<')
    main()
