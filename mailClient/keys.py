from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
import base64
import json
import hashlib

# GENERATE A KEY PAIR
def genKeys():
    privKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    publicKey = privKey.public_key()

    privateKeyPem = privKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


    publicKeyPem = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return privateKeyPem, publicKeyPem

# GENERATE A DUMMY EMAIL
def sigToAddr(sig, service):
    hash = hashlib.sha256(sig).hexdigest()
    addr = service + hash[:10] + "@thebugshub.com"
    return hash, addr

#SIGN A MESSAGE
def signMessage(message, privPem):
    message_bytes = message.encode('utf-8')
    signature = privPem.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )  
    signature_base64 = base64.b64encode(signature)
    return signature_base64
