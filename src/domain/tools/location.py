# coding utf-8

from typing import Optional

import piexif

import httpx


def _convert_to_degress(value):
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1]
    s = value[2][0] / value[2][1]
    return d + (m / 60.0) + (s / 3600.0)


def extract_gps_from_exif(exif_dict: dict):
    gps_ifd = exif_dict.get("GPS")
    if not gps_ifd:
        return None

    lat_ref = gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef)
    lat = gps_ifd.get(piexif.GPSIFD.GPSLatitude)
    lon_ref = gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef)
    lon = gps_ifd.get(piexif.GPSIFD.GPSLongitude)

    if not (lat_ref and lat and lon_ref and lon):
        return None

    try:
        lat_ref = (
            lat_ref.decode()
            if isinstance(lat_ref, (bytes, bytearray))
            else str(lat_ref)
        )
        lon_ref = (
            lon_ref.decode()
            if isinstance(lon_ref, (bytes, bytearray))
            else str(lon_ref)
        )
    except Exception:
        lat_ref = str(lat_ref)
        lon_ref = str(lon_ref)

    latitude = _convert_to_degress(lat)
    if lat_ref.upper() == "S":
        latitude = -latitude

    longitude = _convert_to_degress(lon)
    if lon_ref.upper() == "W":
        longitude = -longitude

    return latitude, longitude


async def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    # Uses OpenStreetMap Nominatim. Respect its usage policy if using in production.
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"format": "jsonv2", "lat": str(lat), "lon": str(lon)}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(
            url, params=params, headers={"User-Agent": "PhotoGeoLocator/1.0 (example)"}
        )
        if r.status_code != 200:
            return None
        j = r.json()
        return j.get("display_name")
