EXTERNAL_VOLUME_ID="104210771"

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/opt/awscliv2.zip"
unzip /opt/awscliv2.zip -d /opt
/opt/aws/install
aws --version
  
# Mount external volume
echo "Attempting to setup external volume with ID $EXTERNAL_VOLUME_ID..."
mkdir -p /mnt/main
mount /dev/disk/by-id/scsi-0HC_Volume_${EXTERNAL_VOLUME_ID} /mnt/main

#  Set up ai_newsletter cron job
chmod +x /opt/general/ai_newsletter/process.sh
(crontab -l 2>/dev/null; echo "0 7 * * * /opt/general/ai_newsletter/process.sh >> /var/log/ai_newsletter.log 2>&1") | crontab -