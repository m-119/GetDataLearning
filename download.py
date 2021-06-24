import requests
# В данном вариант приходится файл загрузить в оперативную память до записи.
# Нужен контроль над именем файла в open

url = 'https://ru.wikipedia.org/wiki/PNG#/media/Файл:PNG_transparency_demonstration_1.png'

response = requests.get(url)

with open ('pic.png', 'wb') as f:
    f.write(response.content)

import wget
# В данном варианте имя и расширение определяется из источника
# Файл пишется не весь сразу а частями
# Файл не перезапишется если будет одинаковое имя

wget.download(url)