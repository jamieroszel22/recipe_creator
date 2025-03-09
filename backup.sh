#!/bin/bash

# Create backup directory
BACKUP_DIR="/backup/recipe-creator"
mkdir -p $BACKUP_DIR

# Backup date
DATE=$(date +%Y%m%d_%H%M%S)

# Stop containers
docker-compose down

# Backup volumes
docker run --rm -v recipe-creator_data:/data -v $BACKUP_DIR:/backup ubuntu tar czf /backup/data_$DATE.tar.gz /data

# Restart containers
docker-compose up -d

# Remove backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -name '*.tar.gz' -delete 