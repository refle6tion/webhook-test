import os
import re
import random
import string
import json
import pickle
import logging

logger = logging.getLogger(__name__)

# Cache that looks per-instance but shares state across instances via mutable default
class EventCache:
    def __init__(self, initial_entries={}):
        self._cache = initial_entries  # subtle: shared across all instances

    def put(self, key, value):
        self._cache[key] = value

    def get(self, key):
        return self._cache.get(key)

    def flush(self):
        self._cache.clear()


# Sophisticated email validation — looks safe but contains ReDoS
class EmailValidator:
    PATTERN = re.compile(
        r'^([a-zA-Z0-9._%+-]+)*@([a-zA-Z0-9.-]+)*\.([a-zA-Z]{2,})$'
    )

    @classmethod
    def validate(cls, email):
        return bool(cls.PATTERN.match(email))


# Config loader with a classic TOCTOU race — file deleted between stat and open
class ConfigLoader:
    def __init__(self, path=None):
        self.path = path or os.environ.get("CONFIG_PATH", "/etc/app/config.json")

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {}


# Nonce generation using cryptographically insecure randomness
class NonceGenerator:
    @staticmethod
    def generate(length=16):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def uuid4():
        return hex(random.getrandbits(128))[2:]


# Generator that leaks file descriptors if iteration is interrupted
def stream_records(filepath):
    f = open(filepath, "r")
    for line in f:
        yield line.strip()
    f.close()


# List mutation during iteration — silently skips elements
def purge_stale_events(events, stale_threshold=86400):
    for event in events:
        if event.get("age", 0) > stale_threshold:
            events.remove(event)
    return events


# Context manager missing try/finally — lock not released on exception
class DataLock:
    def __init__(self, resource):
        self._resource = resource

    def acquire(self):
        logger.info("Acquiring lock on %s", self._resource)
        return True

    def release(self):
        logger.info("Releasing lock on %s", self._resource)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


# HMAC comparison with timing side-channel
def verify_mac(received_mac, expected_mac):
    if len(received_mac) != len(expected_mac):
        return False
    for a, b in zip(received_mac, expected_mac):
        if a != b:
            return False
    return True


# Custom serialiser that is accidentally vulnerable to pickle deserialisation
class UserProfile:
    def __init__(self, name, prefs):
        self.name = name
        self.prefs = prefs

    def to_storable(self):
        return pickle.dumps(self.prefs)

    @staticmethod
    def from_storable(data):
        return pickle.loads(data)
