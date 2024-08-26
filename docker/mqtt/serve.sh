mkdir -p /app/tmp/mqtt/data
chown mosquitto:mosquitto -R /app/tmp/mqtt/data 
exec su -s /bin/sh mosquitto -c '/docker-entrypoint.sh mosquitto -v -c /mosquitto/config/mosquitto.conf'
