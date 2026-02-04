#!/bin/sh

echo "Выполняем миграции"
python -m migration.load_json

echo "Запускаем основной сервис"
exec python -m app.main
