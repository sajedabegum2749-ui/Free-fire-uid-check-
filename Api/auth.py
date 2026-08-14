import requests
import json
from Proto.compiled import MajorLogin_pb2
from Utilities.utils import encode_protobuf, decode_protobuf
from Configuration.APIConfiguration import RELEASEVERSION


GARENA_AUTH_URL = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
MAJOR_LOGIN_URL = "https://loginbp.ggpolarbear.com/MajorLogin"

GARENA_HEADERS = {
    'User-Agent': "GarenaMSDK/4.0.19P9(A063 ;Android 13;en;IN;)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip"
}

LOGIN_HEADERS = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; A063 Build/TKQ1.221220.001)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'Authorization': "Bearer",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': RELEASEVERSION,
}


def get_garena_token(uid: int, password: str) -> dict | None:
    payload = {
        'uid': uid,
        'password': password,
        'response_type': "token",
        'client_type': "2",
        'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        'client_id': "100067"
    }
    try:
        r = requests.post(GARENA_AUTH_URL, data=payload, headers=GARENA_HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[Garena Auth Error] {e}")
        return None


def get_major_login(access_token: str, open_id: str) -> dict | None:
    payload = encode_protobuf(
        {"openid": open_id, "logintoken": access_token, "platform": "4"},
        MajorLogin_pb2.request()
    )
    try:
        r = requests.post(MAJOR_LOGIN_URL, data=payload, headers=LOGIN_HEADERS, timeout=15)
        return decode_protobuf(r.content, MajorLogin_pb2.response)
    except Exception as e:
        print(f"[Major Login Error] {e}")
        return None


def authenticate(region_accounts: dict, region: str) -> dict | None:
    """
    Full auth flow: Garena token → MajorLogin → returns {token, serverUrl}
    """
    creds = region_accounts.get(region)
    if not creds:
        return None

    garena = get_garena_token(creds['uid'], creds['password'])
    if not garena or 'access_token' not in garena:
        return None

    login = get_major_login(garena['access_token'], garena['open_id'])
    if not login or 'token' not in login:
        return None

    return login  # has: token, serverUrl, accountId, etc.
