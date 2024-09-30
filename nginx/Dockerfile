# Используем официальный образ nginx
FROM nginx:latest

# Копируем наши конфигурационные файлы в контейнер
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/ /etc/nginx/conf.d/
