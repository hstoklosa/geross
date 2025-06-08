import hmac
import hashlib

def verify_signature(data, signature, secret):
    """Return True if signatures match (use sha256)."""
    sha_name, sig = signature.split('=', 1)
    if sha_name != 'sha256':
        return False
    mac = hmac.new(secret.encode(), data, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), sig)