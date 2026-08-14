import requests
from Proto.compiled import (
    PlayerPersonalShow_pb2,
    PlayerStats_pb2,
    PlayerCSStats_pb2,
    SearchAccountByName_pb2,
)
from Utilities.utils import encode_protobuf, decode_protobuf
from Configuration.APIConfiguration import RELEASEVERSION

HEADERS_BASE = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; A063 Build/TKQ1.221220.001)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': RELEASEVERSION,
}


def _headers(token: str) -> dict:
    return {**HEADERS_BASE, 'Authorization': f"Bearer {token}"}


def get_player_info(server_url: str, token: str, uid: int,
                    need_gallery: bool = False,
                    need_blacklist: bool = False,
                    need_spark: bool = False) -> dict | None:
    """GetPlayerPersonalShow — full profile info."""
    payload = encode_protobuf({
        "accountId": uid,
        "callSignSrc": 7,
        "needGalleryInfo": need_gallery,
        "needBlacklist": need_blacklist,
        "needSparkInfo": need_spark,
    }, PlayerPersonalShow_pb2.request())

    try:
        r = requests.post(
            f"{server_url}/GetPlayerPersonalShow",
            data=payload,
            headers=_headers(token),
            timeout=15
        )
        r.raise_for_status()
        return decode_protobuf(r.content, PlayerPersonalShow_pb2.response)
    except Exception as e:
        print(f"[GetPlayerPersonalShow Error] {e}")
        return None


def get_player_br_stats(server_url: str, token: str, uid: int, matchmode: int = 0) -> dict | None:
    """GetPlayerStats — Battle Royale stats. matchmode: 0=career, 1=normal, 2=ranked."""
    payload = encode_protobuf(
        {"accountid": uid, "matchmode": matchmode},
        PlayerStats_pb2.request()
    )
    try:
        r = requests.post(
            f"{server_url}/GetPlayerStats",
            data=payload,
            headers=_headers(token),
            timeout=15
        )
        r.raise_for_status()
        return decode_protobuf(r.content, PlayerStats_pb2.response)
    except Exception as e:
        print(f"[GetPlayerStats Error] {e}")
        return None


def get_player_cs_stats(server_url: str, token: str, uid: int, matchmode: int = 0) -> dict | None:
    """GetPlayerTCStats — Clash Squad stats. matchmode: 0=career, 1=normal, 6=ranked."""
    payload = encode_protobuf(
        {"accountid": uid, "gamemode": 15, "matchmode": matchmode},
        PlayerCSStats_pb2.request()
    )
    try:
        r = requests.post(
            f"{server_url}/GetPlayerTCStats",
            data=payload,
            headers=_headers(token),
            timeout=15
        )
        r.raise_for_status()
        return decode_protobuf(r.content, PlayerCSStats_pb2.response)
    except Exception as e:
        print(f"[GetPlayerTCStats Error] {e}")
        return None


def search_by_name(server_url: str, token: str, keyword: str) -> dict | None:
    """FuzzySearchAccountByName — search players by nickname."""
    payload = encode_protobuf(
        {"keyword": keyword},
        SearchAccountByName_pb2.request()
    )
    try:
        r = requests.post(
            f"{server_url}/FuzzySearchAccountByName",
            data=payload,
            headers=_headers(token),
            timeout=15
        )
        r.raise_for_status()
        return decode_protobuf(r.content, SearchAccountByName_pb2.response)
    except Exception as e:
        print(f"[FuzzySearch Error] {e}")
        return None
