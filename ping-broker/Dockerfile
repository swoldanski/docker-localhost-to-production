FROM alpine
ENV AUTHOR=Stranger
ENV BROKER=non-existent-broker

WORKDIR /srv
COPY index_template.html .

EXPOSE 80
CMD env && cd /srv/ && sed -e s/Docker/"$AUTHOR"/ -e s/HOSTNAME/"$HOSTNAME"/  -e s/VERSION/"$VERSION"/ -e s/BROKER/"$BROKER"/ index_template.html > index.html && httpd -f -vv & ping $BROKER