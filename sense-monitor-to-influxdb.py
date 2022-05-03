import asyncio
from decouple import config
from retry import retry
from sense_energy import ASyncSenseable
from influxdb_client import InfluxDBClient, Point

sense_username=config('SENSE_USERNAME')
sense_password=config('SENSE_PASSWORD')
influxdb_url=config('INFLUXDB_URL')
influxdb_token=config('INFLUXDB_TOKEN')
influxdb_org=config('INFLUXDB_ORG')
influxdb_bucket=config('INFLUXDB_BUCKET')

influxdb_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influxdb_client.write_api()

def realtime_callback(payload):
    records = []
    for device in payload['devices']:
        records.append(Point("sense_devices").tag("id", device['id']).tag('name', device['name']).field("watts", device['w']))
    for index, channel in enumerate(payload['channels']):
        records.append(Point("sense_channel").tag("channel", index).field("watts", channel))
    write_api.write(influxdb_bucket, influxdb_org, records)

@retry()
async def main():
    sense = ASyncSenseable()
    await sense.authenticate(sense_username, sense_password)
    await sense.async_realtime_stream(realtime_callback)

asyncio.run(main())
