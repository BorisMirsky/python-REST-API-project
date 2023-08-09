import requests


def dollar_rate():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    result = float(data['Valute']['USD']['Value'])
    return result


