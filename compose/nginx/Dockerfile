FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf
COPY nginx /etc/nginx

# installs the `ps` command in the nginx image
RUN apt-get update && apt-get install -y procps

ADD start.sh /start.sh
ADD nginx-secure.conf /etc/nginx/nginx-secure.conf
ADD dhparams.pem /etc/ssl/private/dhparams.pem
RUN chmod +x /start.sh
CMD /start.sh
