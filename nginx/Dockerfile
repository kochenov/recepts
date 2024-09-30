FROM nginx:latest

# Копируем основной конфигурационный файл Nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Копируем дополнительные конфигурации (например, для виртуальных хостов)
COPY ./nginx/conf.d/ /etc/nginx/conf.d/
