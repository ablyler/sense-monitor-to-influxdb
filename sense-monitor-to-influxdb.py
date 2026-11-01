import asyncio
import logging
import time

import aiohttp
from decouple import config
from influxdb_client import InfluxDBClient, Point
from sense_energy import ASyncSenseable

sense_monitor_name = str(config("SENSE_MONITOR_NAME"))
sense_username = str(config("SENSE_USERNAME"))
sense_password = str(config("SENSE_PASSWORD"))
influxdb_url = str(config("INFLUXDB_URL"))
influxdb_token = str(config("INFLUXDB_TOKEN"))
influxdb_org = str(config("INFLUXDB_ORG"))
influxdb_bucket = str(config("INFLUXDB_BUCKET"))

influxdb_client = InfluxDBClient(
    url=influxdb_url,  # type: ignore
    token=influxdb_token,  # type: ignore
    org=influxdb_org,  # type: ignore
)
write_api = influxdb_client.write_api()


def realtime_callback(payload):
    records = []
    for device in payload["devices"]:
        records.append(
            Point("sense_devices")
            .tag("monitor_name", sense_monitor_name)
            .tag("id", device["id"])
            .tag("name", device["name"])
            .field("watts", device["w"])
        )
    for index, channel in enumerate(payload["channels"]):
        records.append(
            Point("sense_channel")
            .tag("monitor_name", sense_monitor_name)
            .tag("channel", index)
            .field("watts", channel)
        )
    write_api.write(
        influxdb_bucket,  # type: ignore
        influxdb_org,  # type: ignore
        records,
    )


LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger("sense-monitor")

WSS_TIMEOUT = config("SENSE_WSS_TIMEOUT", default=30, cast=int)
API_TIMEOUT = config("SENSE_API_TIMEOUT", default=30, cast=int)
MIN_BACKOFF = 5
MAX_BACKOFF = 300
# A stream that stays up this long counts as healthy and resets the backoff.
HEALTHY_RUN_SECONDS = 300


async def stream_once():
    async with aiohttp.ClientSession() as session:
        sense = ASyncSenseable(
            api_timeout=API_TIMEOUT,
            wss_timeout=WSS_TIMEOUT,
            client_session=session,
        )
        await sense.authenticate(sense_username, sense_password)
        log.info("Authenticated to Sense; streaming realtime data")
        await sense.async_realtime_stream(realtime_callback)


async def main():
    backoff = MIN_BACKOFF
    while True:
        started = time.monotonic()
        try:
            await stream_once()
            log.warning("Realtime stream ended; reconnecting")
        except asyncio.CancelledError:
            raise
        except Exception as ex:  # reconnect on any API/network failure
            log.warning("Realtime stream failed: %r", ex)
        if time.monotonic() - started >= HEALTHY_RUN_SECONDS:
            backoff = MIN_BACKOFF
        log.info("Reconnecting in %ss", backoff)
        await asyncio.sleep(backoff)
        backoff = min(backoff * 2, MAX_BACKOFF)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        write_api.close()
        influxdb_client.close()
