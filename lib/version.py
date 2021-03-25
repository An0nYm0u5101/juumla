from rich import print

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import os
import xmltodict

def get_joomla_version_1(args):
    print('\n[yellow][INF] Trying to get Joomla version... [/]')

    manifest_path = f'{args.u}/administrator/manifests/files/joomla.xml'

    try:
        response = requests.get(manifest_path, verify=False, timeout=10, allow_redirects=False)
        headers = response.headers
        status_code = response.status_code

        if(status_code == 200 and 'application/xml' in headers):
            data = xmltodict.parse(response.content)
            joomla_version = data["extension"]["version"]

            print(f"[green][INF] Joomla version found: {joomla_version}\n")
        else:
            print(f'\n[red][ERR] Joomla version not found on first check... [/]')
            get_joomla_version_2(args)

    except requests.exceptions.ConnectionError:
        return print(f'\n[red][ERR] Connection problems with {manifest_path}[/]')
    except xmltodict.expat.ExpatError:
        return print(f"[red][ERR] Can't parse Joomla XML, stopping... \n[/]")

    

def get_joomla_version_2(args):
    language_path = f'{args.u}/language/en-GB/en-GB.xml'

    try:
        response = requests.get(language_path, verify=False, timeout=10, allow_redirects=False)
        status_code = response.status_code

        if(status_code == 200):
            data = xmltodict.parse(response.content)
            joomla_version = data["metafile"]["version"]

            print(f"[green][INF] Joomla version found: {joomla_version} on second check\n")
        else:
            return print(f'\n[red][ERR] Joomla version not found on second check... [/]')
            
    except requests.exceptions.ConnectionError:
        return print(f'\n[red][ERR] Connection problems with {language_path}[/]')