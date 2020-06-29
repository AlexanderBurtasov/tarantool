# HTTP server with tarantool database
Тестовое приложение: Python-based HttpServer && Tarantool 2.2

# Dependencies

## Build docker images
  Call script:
  ```sh
  build_images.sh
  ```
  Если все получилось, то должны появиться 2 image: **httpserver:0.9** и **bugdb:0.9**.

## Run images
  Call script: 
  ```sh
  run_images.sh
  ```
  Если все получилось, то наш http-server будет доступен через **порт 5502**. По умолчанию сервер настроен на обработку **50** запросов в секунду.

## Change settings
Файл: **docker/docker-compose.yml**.
Можно менять значения:
  - services/httpserver/SERVER_PORT - порт, который мониторит httpserver
  - services/httpserver/REQUEST_PER_SECOND - задает максимальное количество обрабатываемых в секунду запросов.
Остальные значения я бы не менял: отвалится контейнер с tarantool или еще что-нибудь.
  
## Request examples
  * GET value with key id_0:
  ```curl
curl --request GET \
  --url http://192.168.99.100:5052/kv/id_0
  ```

  * CREATE record with key id_0
  ```sh
curl --request POST \
  --url http://192.168.99.100:5052/kv \
  --header 'content-type: application/json' \
  --data '{
	"key": "id_0",
	"value": {
		"title": "Hells bells",
		"year": 1996
	}
}'
```

  * ALTER value with key id_0
  ```sh
curl --request PUT \
  --url http://192.168.99.100:5052/kv/id_0 \
  --header 'content-type: application/json' \
  --data '{
	"value": {
		"title": "Scoro dembel",
		"year": 1997
	}
}
'
```

  * DELETE record with key id_0
  ```sh
curl --request DELETE \
  --url http://192.168.99.100:5052/kv/id_0
  ```

## Комментарии к заданию
1) скачать/собрать тарантул -- **скачал и собрал. Правда, docker-образ tarantool делал не на основе сборки, а на основе существующего образа**
2) запустить тестовое приложение -- **запустил!**
3) реализовать kv-хранилище доступное по http -- **реализовал: есть образ с БД tarantool, есть питоновский http-server, обрабатывающий запросы**
4) выложить на гитхаб -- **выложил**
    задеплоить где-нибудь в публичном облаке, чтобы мы смогли проверить работоспособность (или любым другим способом) -- **банально не дошли руки. Если запустить скрипты ./build_images.sh и run_images.sh - все будет.**
 
 - POST возвращает 409 если ключ уже существует, **сделано**
 - POST, PUT возвращают 400 если боди некорректное **сделано**
 - PUT, GET, DELETE возвращает 404 если такого ключа нет **сделано**
 - все операции логируются **тут не было указано, на каком уровне ведется логирование: БД, или http server. Я сделал как проще мне - логирование http-server. Логи доступны в папке /home/tarantool/httpserver/logs внутри контейнера с сервером.**
 - в случае, если число запросов в секунду в http api превышает заданый интервал, возвращать 429 ошибку. **сделал**

Сервер брал самый простой, про многопоточность не думал. Куда при необходимости вкорячить мьютексы - знаю.
