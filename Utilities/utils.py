import json
import os
from google.protobuf.message import Message
from google.protobuf import json_format, message
from Crypto.Cipher import AES
from Configuration.AESConfiguration import MAIN_KEY, MAIN_IV


def load_accounts():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, 'Configuration', 'AccountConfiguration.json')
    with open(path, 'r') as f:
        return json.load(f)


def pad(text: bytes) -> bytes:
    length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([length] * length)


def aes_cbc_encrypt(text: bytes) -> bytes:
    aes = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return aes.encrypt(pad(text))


def encode_protobuf(data: dict, proto_message: Message) -> bytes:
    json_format.ParseDict(data, proto_message)
    return aes_cbc_encrypt(proto_message.SerializeToString())


def decode_protobuf(encoded_data: bytes, message_type) -> dict:
    instance = message_type()
    instance.ParseFromString(encoded_data)
    return json.loads(json_format.MessageToJson(instance))
