# Task "RAINFALL"

## Description:
Napisz program, który sprawdzi, czy danego dnia będzie padać. Użyj do tego poniższego API.
URL do API:

https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}

W URL należy uzupełnić parametry: latitude, longitude oraz searched_date

## Requirements:
Aplikacja ma działać następująco:
- Program pyta dla jakiej daty należy sprawdzić pogodę. 
- Data musi byc w formacie YYYY-mm-dd, np. 2022-11-03.
- W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną datę następny dzień.
- Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
- Istnieją trzy możliwe informacje dla opadów deszczu:
1. Będzie padać (dla wyniku większego niż 0.0)
2. Nie będzie padać (dla wyniku równego 0.0)
3. Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)
- Wyniki zapytań powinny być zapisywane do pliku. 
- Jeżeli szukana data znajduje sie juz w pliku,
nie wykonuj zapytania do API, tylko zwróć wynik z pliku.