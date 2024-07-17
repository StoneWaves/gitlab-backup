#!/bin/sh

echo "Project: gitlab-backup"
echo "Author:  StoneWaves"
echo "Base:    Alpine 3.9"
echo "Target:  Unraid"
echo ""

# If config doesn't exist yet, create it
if [ ! -f /home/docker/gitlab-backup/config.json ]; then
    cp /home/docker/gitlab-backup/config.json.example /home/docker/gitlab-backup/config.json
fi

# Update token in config.json match $TOKEN environment variable
echo "Update token in config.json match $TOKEN environment variable"
sed -i '/token/c\   \"token\" : \"'${TOKEN}'\",' /home/docker/gitlab-backup/config.json

# Update directory in config.json match $DIRECTORY environment variable
echo "Update directory in config.json match $DIRECTORY environment variable"
sed -i '/directory/c\   \"directory\" : \"'${DIRECTORY}'\",' /home/docker/gitlab-backup/config.json

# Update gitlab_url in config.json match $GITLAB_URL environment variable
echo "Update gitlab_url in config.json match $GITLAB_URL environment variable"
sed -i '/gitlab_url/c\   \"gitlab_url\" : \"'${GITLAB_URL}'\",' /home/docker/gitlab-backup/config.json
 
Start backup
while true
 do python3 gitlab-backup.py /home/docker/gitlab-backup/config.json
 chown -R nobody /home/docker/backups
 sleep $SCHEDULE
done
