import os.path
from datetime import datetime, timedelta
from requests import get


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

    # Sprawdzenie, czy API zwróciło informacje o opadach
    if 'hourly' in data and 'rain' in data['hourly']:
        hourly_precipitation = data['hourly']['rain']

        # Sprawdzenie, czy wystapia jakiekolwiek opady
        if any(precipitation > 0.0 for precipitation in hourly_precipitation):
            return (f'Dnia {searched_date} pod szerokością geograficzną {latitude} '
                    f'i długością geograficzną {longitude} wystąpią opady.')
        else:
            return (f'Dnia {searched_date} pod szerokością geograficzną {latitude} '
                    f'i długością geograficzną {longitude} nie wystąpią opady.')

    # Sytuacja, gdy API nie zwróciło informacji, również ze względu na zbyt odległą datę
    return (f'Nie stwierdzono, czy dnia {searched_date} pod szerokością geograficzną {latitude} '
            f'i długością geograficzną {longitude} wystąpią opady.')


def save_to_file(file_name, content):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(content + '\n')
    print(content)
    print(f'Informacje o opadach zostaly zapisane do pliku {file_name}.')


def main():
    latitude, longitude, searched_date = enter_data()

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
