#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, requests, json
from inspect import stack
from common import retry
from traceback import print_exc
from httplib import OK, NO_CONTENT

from config import (DEBUG, TARGET_COUNTRY, API_SECRET, API_HOST, API_VERSION,
                    AF, PAIRED_DEVICE_GUID, GUID, DEVICE_TYPE, GEOIP_OVERRIDE)


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_jwt_payload_from_paypal(baid=None):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/paypal/billing-agreements/%s' \
                       % (API_HOST, API_VERSION, baid), headers=headers)
    
    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_paypal_billing_agreement(baid=None):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/paypal/billing-agreements/%s/confirm' \
                       % (API_HOST, API_VERSION, baid), headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_node_by_country(family=AF):
    headers = {'X-Auth-Token': API_SECRET}
    country = urllib.quote(TARGET_COUNTRY)
    
    if GEOIP_OVERRIDE:
        print 'override:%s' % GEOIP_OVERRIDE
        country = GEOIP_OVERRIDE
        
    res = requests.get('%s/api/v%s/node/%s/country/%s' \
                       % (API_HOST, API_VERSION, family, country),
                       headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_node_by_guid(family=AF, guid=PAIRED_DEVICE_GUID):
    if not guid: return None
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/node/%s/guid/%s' \
                       % (API_HOST, API_VERSION, family, guid),
                       headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_device_env_by_name(guid=GUID, name=None, default=None):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/device/%s/env/%s' \
                       % (API_HOST, API_VERSION, guid, name),
                       headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: default = res.content
    return default


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_alpha(country):
    if not country: country = TARGET_COUNTRY
    country = urllib.quote(country)
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/country/%s' \
                       % (API_HOST, API_VERSION, country),
                       headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def get_guid_by_public_ipaddr(ipaddr=None, family=4):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.get('%s/api/v%s/ipaddr/%s/%s' \
                       % (API_HOST, API_VERSION, ipaddr, str(family)),
                       headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return res.content


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def put_device(family=AF, data=None, guid=GUID):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.put('%s/api/v%s/device/%s/%s/%d' \
                       % (API_HOST, API_VERSION, DEVICE_TYPE, guid, family),
                       data=json.dumps(data), headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return (res.status_code, res.content)


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def dequeue_speedtest(guid=GUID):
    result = False
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.head('%s/api/v%s/speedtest/%s' \
                        % (API_HOST, API_VERSION, guid),
                        headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [NO_CONTENT]: result = True
    return result


@retry(Exception, cdata='method=%s()' % stack()[0][3])
def update_speedtest(guid=GUID, data=None):
    headers = {'X-Auth-Token': API_SECRET}
    res = requests.patch('%s/api/v%s/speedtest/%s' \
                         % (API_HOST, API_VERSION, guid),
                         data=json.dumps(data), headers=headers)

    if DEBUG: print '{0}: status_code={1} content={2}'\
       .format(stack()[0][3], res.status_code, res.content)
    if res.status_code in [OK]: return (res.status_code, res.content)
