#!/usr/bin/env python
#
# Created on Jun 5, 2019
# @author: Luiz Rodrigues (Avi Networks) 
#
# AVISDK based Script to scale out VSes with Single SEs
#
# Requires AVISDK ("pip install avisdk")
# This script works for Avi Controler version 17.2.1 onwards
# Usage:
#    usage: vs_scale_in_adjustment.py -c CONTROLLER [-u USERNAME] -p PASSWORD 
#                                     [-t TENANT] [-a API_VERSION] -s SE_GROUP
#       CONTROLLER = controller IP address or name
#       USERNAME = username, by default admin
#       PASSWORD = user password
#       TENANT = Tenant name in Avi
#       API_VERSION = Controller version, by default is 17.2.10
#       SE_GROUP = Service Engine Group Name
import json
import argparse
from avi.sdk.avi_api import ApiSession
from time import sleep
import logging
import requests
def get_vs_list(api, api_version, se_group):
    vs_list = []
    rsp = api.get('virtualservice', api_version=api_version, params={'page_size': 1000,
                                                                     'se_group_ref__name__contains': se_group})
    for vs in rsp.json()['results']:
        vs_list.append(vs['uuid'])
    return vs_list
def vs_scalein(api, api_version, vs_uuid):
    rsp = api.get('virtualservice/%s/runtime' % vs_uuid, api_version=api_version)
    vs_data = json.loads(rsp.text)
    scale_vip_id = vs_data['vip_summary'][0]['vip_id']
    num_se_assigned = vs_data['vip_summary'][0]['num_se_assigned']
    num_se_requested = vs_data['vip_summary'][0]['num_se_requested']
    print ("Analysing VS %s" % vs_uuid)
    while num_se_requested > num_se_assigned:
        print ("    adjusting SEs: requested %i, assigned %i" % (num_se_requested, num_se_assigned))
        api.post('virtualservice/%s/scalein' % vs_uuid, data={'vip_id': scale_vip_id})
        sleep(1)
        rsp = api.get('virtualservice/%s/runtime' % vs_uuid, api_version=api_version)
        vs_data = json.loads(rsp.text)
        num_se_assigned = vs_data['vip_summary'][0]['num_se_assigned']
        num_se_requested = vs_data['vip_summary'][0]['num_se_requested']
    print ("    adjusted SEs: requested %i, assigned %i" % (num_se_requested, num_se_assigned))
        
def main():
    requests.packages.urllib3.disable_warnings()
    #Getting Required Args
    parser = argparse.ArgumentParser(description="AVISDK based Script to scale out VSes with Single SEs")
    parser.add_argument("-c", "--controller", required=True, help="Controller IP address")
    parser.add_argument("-u", "--username", required=False, default="admin", help="Login username")
    parser.add_argument("-p", "--password", required=True, help="Login password")
    parser.add_argument("-t", "--tenant", required=False, help="Tenant Name")
    parser.add_argument("-a", "--api_version", required=False, default="17.2.10", help="API version")
    parser.add_argument("-s", "--se_group", required=True, help="Service Engine Group name")
    args = parser.parse_args()
    host = args.controller
    password = args.password
    user=args.username
    tenant=args.tenant
    api_version = args.api_version
    se_group = args.se_group
    # Getting API session for the intended Controller.
    api = ApiSession.get_session(host, user, password, tenant=tenant, api_version=api_version)
    # Getting the list of VirtualService(s).
    vs_list = get_vs_list(api, api_version, se_group)
    # Scaling-out the VS
    for vs_uuid in vs_list:
        vs_scalein(api, api_version, vs_uuid)
if __name__ == "__main__":
    main()
