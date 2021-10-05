# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# https://yandex.ru/dev/disk/api/reference/capacity.html
import requests
import json
# Описание элементов ответа Элемент 	Описание
# trash_size
#
# Объем файлов, находящихся в Корзине, в байтах.
# total_space
#
# Общий объем Диска, доступный пользователю, в байтах.
# used_space
#
# Объем файлов, уже хранящихся на Диске, в байтах.
# system_folders
#
# Абсолютные адреса системных папок Диска. Имена папок зависят от языка интерфейса пользователя в момент создания персонального Диска. Например, для англоязычного пользователя создается папка Downloads, для русскоязычного — Загрузки и т. д.
#
# На данный момент поддерживаются следующие папки:
#
#     applications — папка для файлов приложений;
#     downloads — папка для файлов, загруженных из интернета (не с устройства пользователя).
#
# https://yandex.ru/dev/disk/api/reference/recent-public.html
# получение инфы
# https://oauth.yandex.ru/client/e8fa3920253246a19cf17bc909f1fd8d
# получение токена
# https://oauth.yandex.ru/verification_code#access_token=AQAAAABRXO0sAAdrGl7dma-UHkwhoaiPTs2HHHA&token_type=bearer&expires_in=31536000


# url = 'https://cloud-api.yandex.net/v1/disk/'
url = 'https://cloud-api.yandex.net/v1/disk?path=app:/'
token = 'AQAAAABRXO0sAAdrGl7dma-UHkwhoaiPTs2HHHA'

headers = {
    'Content-Type': 'application/json',

    'Authorization': token
}
#
disk_total_space = 'total_space'
folder_info = 'system_folders'
#
disk = requests.get(f'{url}', headers = headers)
#
print(disk.json())

#
disk = requests.get(f'{url}{disk_total_space}', headers = headers)

print(disk_total_space+' = '+str(disk.json()[disk_total_space]))
#
disk = requests.get(f'{url}{folder_info}', headers = headers)
# print(disk.json())

# # Названия файлов в папке
print('Содержимое:')
for i in disk.json()[folder_info]:
    print(i)
#
with open('disk.json', 'w') as f:
     json.dump(disk.json(), f)
