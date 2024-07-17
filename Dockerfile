FROM alpine:3.9

RUN mkdir -p /home/docker/gitlab-backup;
ENV HOME /home/docker

COPY gitlab-backup.py /home/docker/gitlab-backup/gitlab-backup.py
COPY requirements.txt /home/docker/gitlab-backup/requirements.txt
COPY config.json.example /home/docker/gitlab-backup/config.json.example
COPY backup.sh /home/docker/gitlab-backup/backup.sh

WORKDIR /home/docker/gitlab-backup
RUN apk add --no-cache python3 py3-pip git; \
    pip3 install --upgrade pip; \
    pip3 install -r requirements.txt; \
    chmod -R 777 /home/docker; \
    chmod +x backup.sh;

CMD ["./backup.sh"]
