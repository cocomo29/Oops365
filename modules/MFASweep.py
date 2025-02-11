import requests
import base64
import json
import random
import time
import re
import argparse
from exchangelib import Credentials, Account
from colorama import Fore, Style

def authAsm(username, password):
    # print(f"{Colors.YELLOW}[*] MFA Sweeping...{Colors.RESET}")
    url = "https://login.microsoftonline.com"
    print(f"{Fore.YELLOW}[*] Logging into Microsoft Service Management API{Style.RESET_ALL}")
    bodyParams = {
        'resource': 'https://management.core.windows.net',
        'client_id': '1950a258-227b-4e31-a9cf-717495945fc2',
        'grant_type': 'password',
        'username': username,
        'password': password,
        'scope': 'openid'
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    finalUrl = url + "/Common/oauth2/token"
    response = requests.post(finalUrl, data=bodyParams, headers=headers)
    
    if response.status_code == 200:
        print(f"{Fore.GREEN}[+] SUCCESS! {username} is able to authenticate to the Microsoft Service Management API{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}[-] FAILED! {username} failed to authenticate to the Microsoft Service Management API{Style.RESET_ALL}")
        return False

def authWp(device, username, password, userAgent):
    print(f"{Fore.YELLOW}[*] Logging into Microsoft Web Portal with {device}{Style.RESET_ALL}")
    o365 = requests.Session()
    headers = {"User-Agent": userAgent}
    response = o365.get('https://outlook.office365.com', headers=headers)
    
    partialCtxPattern = re.compile(r'urlLogin":".*?"')
    partialCtx = partialCtxPattern.findall(response.text)

    ctxPattern = re.compile(r'ctx=.*?"')
    ctx = ctxPattern.findall(partialCtx[0])[0].replace('ctx=', '').replace('"', '')

    sftPattern = re.compile(r'sFT":".*?"')
    sft = sftPattern.findall(response.text)[0].replace('sFT":"', '').replace('"', '')

    userForm = {
        "username": username,
        "isOtherIdpSupported": "false",
        "checkPhones": "false",
        "isRemoteNGCSupported": "true",
        "isCookieBannerShown": "false",
        "isFidoSupported": "true",
        "originalRequest": ctx,
        "country": "US", 
        "forceotclogin": "false",
        "isExternalFederationDisallowed": "false",
        "isRemoteConnectSupported": "false",
        "federationFlags": "0",
        "isSignup": "false",
        "flowToken": sft,
        "isAccessPassSupported": "true"
    }

    jsonForm = json.dumps(userForm)
    url = "https://login.microsoftonline.com/common/GetCredentialType?mkt=en-US"
    response = o365.post(url, headers=headers, json=jsonForm)

    authBody = {
        "i13": "0",
        "login": username,
        "loginfmt": username,
        "type": "11",
        "LoginOptions": "3",
        "lrt": "",
        "lrtPartition": "",
        "hisRegion": "",
        "hisScaleUnit": "",
        "passwd": password,
        "ps": "2",
        "psRNGCDefaultType": "",
        "psRNGCEntropy": "",
        "psRNGCSLK": "",
        "canary": "",
        "ctx": ctx,
        "hpgrequestid": "",
        "flowToken": sft,
        "NewUser": "1",
        "FoundMSAs": "",
        "fspost": "0",
        "i21": "0",
        "CookieDisclosure": "0",
        "IsFidoSupported": "1",
        "isSignupPost": "0",
        "i2": "1",
        "i17": "",
        "i18": "",
        "i19": "198733",
    }

    response = o365.post("https://login.microsoftonline.com/common/login", headers=headers, data=authBody)

    if "ESTSAUTH" in [cookie.name for cookie in o365.cookies]:
        print(f"{Fore.GREEN}[+] SUCCESS! {username} was able to authenticate to the Microsoft 365 Web Portal.{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}[-] FAILED! {username} failed to authenticate to the Microsoft 365 Web Portal.{Style.RESET_ALL}")
        return False

def authEws(username, password):
    print(f"{Fore.YELLOW}[*] Logging into Exchange Web Services {Style.RESET_ALL}")
    credentials = Credentials(username=username, password=password)
    try:
        account = Account(primary_smtp_address=username, credentials=credentials, autodiscover=True)
        lastEmail = account.inbox.all().order_by('-datetime_received')[0]
        print(f"{Fore.GREEN}[+] SUCCESS! {username} was able to authenticate to Microsoft 365 EWS!{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[-] FAILED! {username} failed to authenticate to Exchange Web Services: {e}{Style.RESET_ALL}")
        return False

def authAs(username, password):
    print(f"{Fore.YELLOW}[*] Logging into Microsoft Active Sync{Style.RESET_ALL}")
    easUrl = "https://outlook.office365.com/Microsoft-Server-ActiveSync"
    encodeUsernamePassword = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {encodeUsernamePassword}"}
    try:
        easLogin = requests.get(easUrl, headers=headers)
        if easLogin.status_code == 505:
            print(f"{Fore.GREEN}[+] SUCCESS! {username} successfully authenticated to O365 ActiveSync.{Style.RESET_ALL}")
            return True
    except Exception as e:
        pass
    print(f"{Fore.RED}[-] FAILED! {username} failed to authenticate to Microsoft ActiveSync.{Style.RESET_ALL}")
    return False

def jitteredSleep(stime, jitter=1):
    jitterRange = stime * jitter / 100
    stime += random.uniform(-jitterRange, jitterRange)
    print(f"{Fore.YELLOW}[*]Sleeping {stime} seconds...{Style.RESET_ALL}")
    time.sleep(stime)

def main():
    parser = argparse.ArgumentParser(description="Microsoft Authentication Script")
    parser.add_argument("-e", "--email", required=True, help="Email address for login")
    parser.add_argument("-p", "--password", required=True, help="Password for login")
    args = parser.parse_args()

    username = args.email
    password = args.password

    adfsDomain = False
    adfsLoginSuccess = False
    ewsSuccess = False
    gapiSuccess = False
    asmSuccess = False
    mwpwSuccess = False
    mwplSuccess = False
    mwpmSuccess = False
    mwpaSuccess = False
    mwpiSuccess = False
    mwpwpSuccess = False
    asmSuccess = False
    asSuccess = False

    print("Starting Microsoft Authentication Checks...")

    if adfsDomain:
        adfsLoginSuccess = authAdfs(username, password)

    print(f"\n{Fore.MAGENTA}[*] MICROSOFT API CHECKS{Style.RESET_ALL}")
    gapiSuccess = authAsm(username, password)
    asmSuccess = authAsm(username, password)

    print(f"\n{Fore.MAGENTA}[*] MICROSOFT WEB PORTAL CHECKS{Style.RESET_ALL}")
    mwpwSuccess = authWp('Windows', username, password, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    mwplSuccess = authWp('Linux', username, password, 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0)')
    mwpmSuccess = authWp('Mac OS', username, password, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)')
    mwpaSuccess = authWp('Android', username, password, 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5)')
    mwpiSuccess = authWp('iPhone', username, password, 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X)')
    mwpwpSuccess = authWp('Windows Phone', username, password, 'Mozilla/5.0 (Mobile; Windows Phone 8.1)')

    print(f"\n{Fore.MAGENTA}[*] LEGACY AUTH CHECKS{Style.RESET_ALL}")
    ewsSuccess = authEws(username, password)
    asSuccess = authAs(username, password)

    print(f"\n{Fore.YELLOW}[*] SINGLE FACTOR ACCESS RESULTS:{Style.RESET_ALL}")
    gapiResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if gapiSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    asmResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if asmSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwpwResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwpwSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwplResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwplSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwpmResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwpmSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwpaResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwpaSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwpiResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwpiSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    mwpwpResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if mwpwpSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    ewsResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if ewsSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    adfsResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if adfsDomain else f"{Fore.RED}NO{Style.RESET_ALL}"
    adfsLoginResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if adfsLoginSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"
    asResult = f"{Fore.GREEN}YES{Style.RESET_ALL}" if asSuccess else f"{Fore.RED}NO{Style.RESET_ALL}"

    results = f"""
        Microsoft Graph API: {gapiResult}
        Microsoft Service Management API: {asmResult}
        Microsoft 365 Web Portal w/ Windows User Agent: {mwpwResult}
        Microsoft 365 Web Portal w/ Linux User Agent: {mwplResult}
        Microsoft 365 Web Portal w/ Mac OS User Agent: {mwpmResult}
        Microsoft 365 Web Portal w/ Android User Agent: {mwpaResult}
        Microsoft 365 Web Portal w/ iPhone User Agent: {mwpiResult}
        Microsoft 365 Web Portal w/ Win Phone User Agent: {mwpwpResult}
        Exchange Web Services: {ewsResult}
        Active Sync: {asResult}
        ADFS found: {adfsResult}
        ADFS Auth: {adfsLoginResult}
        {Style.RESET_ALL}
        """
    print(results)

if __name__ == "__main__":
    main()
