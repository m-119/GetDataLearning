import re

def salary(s: str, min='min', max='max', stable='stable', currency='currency') -> dict:
    curency: dict = {
        # трансляция
        'ман.': 'AZN', 'бел. руб.': 'BYR', '€': 'EUR', 'тенге': 'KZT', 'руб': 'RUR', 'грн': 'UAH', '$ ': 'USD',
        'сум UZS': 'UZS', 'лари GEL': 'GEL', 'сом KGS': 'KGS',
        # обозначение, по хорошему можно через регулярку на 3 заглавных символа, но так вышло быстрее собрать значения
        'AZN': 'AZN', 'BYR': 'BYR', 'EUR': 'EUR', 'KZT': 'KZT', 'RUR': 'RUR', 'UAH': 'UAH', 'USD': 'USD', 'UZS': 'UZS',
        'GEL': 'GEL', 'KGS': 'KGS'
    }
    result = {min: None, stable: None, max: None, currency: None}

    r_digits = re.compile('\d+', re.IGNORECASE)
    r_min = re.compile('от', re.IGNORECASE)
    r_max = re.compile('до', re.IGNORECASE)
    # r_hand = re.compile(' на руки', re.IGNORECASE)
    # обозначение валют на основе ключенй словаря
    r_curency = re.compile(f'({"|".join(list(curency.keys()))})', re.IGNORECASE)

    if s is None:
        return result

    sr = re.sub(r'\s+', '', s).lower()
    min_max = r_digits.findall(sr)

    if len(min_max) == 1:
        if r_min.findall(sr):
            result[min] = int(min_max[0])
        elif r_max.findall(sr):
            result[max] = int(min_max[0])
        else:
            result[stable] = int(min_max[0])
    elif len(min_max) == 2:
        result[min] = int(min_max[0])
        result[max] = int(min_max[1])
    c = r_curency.search(sr)
    if c:
        result[currency] = curency[c.group(0)]
    return result