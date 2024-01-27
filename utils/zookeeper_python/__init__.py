"""Hosted Zookeeper discovery"""

import logging
import yaml
import os
import socket
import sys
import re

from kazoo.client import KazooClient
from dns import resolver
from dns.exception import DNSException
import six

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_DIR = os.path.join(
    r'\\' if sys.platform == 'win32' else os.sep,
    ''
)


class ZkUtilsException(Exception):
    """ Exceptions coming from hosted zookeeper discovery"""

def _get_connection_details_from_config_file():
    pass

def _build_address_from_resource(r):
    pass

RE_TXT_PRINC = re.compile(r'princ=(\w+)\@')

try:
    _dns_resolve = getattr(resolver, 'resolve')
except AttributeError:
    _dns_resolve = getattr(resolver, 'query')

def _get_connection_details_from_dns(env, rootnode, region='na'):
    pass

def getConnectionDetails(env, rootnode, region='na', zone=None):
    pass

def getKazooClient(env, rootnode, region='na', zone=None, onbehalfId=None, **argv):
    pass

def getKazooClient_connstring(connstring, proid, onbehalId=None, **argv):
    pass