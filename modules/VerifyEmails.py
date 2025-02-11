import requests
import argparse
import re
import random
import string
from colorama import Fore, Style

class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL

def GetOfficeSession():
    Headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
                      " (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }

    Session = requests.session()
    Response = Session.get("https://www.office.com", headers=Headers)
    ClientId = re.findall(b'"appId":"([^"]*)"', Response.content)

    Response = Session.get("https://www.office.com/login?es=Click&ru=/&msafed=0", headers=Headers, allow_redirects=True)
    HpgId = re.findall(b'hpgid":([0-9]+),', Response.content)
    HpgAct = re.findall(b'hpgact":([0-9]+),', Response.content)
    SCtx = re.findall(b'"sCtx":"([^"]*)"', Response.content)

    if not ClientId or not HpgId or not HpgAct or not SCtx:
        print(f"{Colors.RED}[!] Error retrieving session details.{Colors.RESET}")
        return None, None, None

    Headers.update({
        "client-request-id": ClientId[0].decode(),
        "Referer": Response.url,
        "hpgrequestid": Response.headers.get("x-ms-request-id", ""),
        "canary": ''.join(random.choice(string.ascii_letters + string.digits + "-_") for _ in range(248)),
        "hpgid": HpgId[0].decode(),
        "Accept": "application/json",
        "hpgact": HpgAct[0].decode(),
        "Origin": "https://login.microsoftonline.com"
    })

    PayloadTemplate = {
        "isOtherIdpSupported": True,
        "checkPhones": False,
        "isRemoteNGCSupported": True,
        "isCookieBannerShown": False,
        "isFidoSupported": False,
        "originalRequest": SCtx[0].decode(),
        "forceotclogin": False,
        "isExternalFederationDisallowed": False,
        "isRemoteConnectSupported": False,
        "federationFlags": 0,
        "isSignup": False,
        "isAccessPassSupported": True
    }

    return Session, Headers, PayloadTemplate

def VerifyEmails(EmailList):
    print(f"{Colors.YELLOW}[*] Validating emails on Office.com...{Colors.RESET}")
    Session, Headers, PayloadTemplate = GetOfficeSession()
    if not Session:
        return
    
    ValidEmails = []

    for Email in EmailList:
        Payload = PayloadTemplate.copy()
        Payload["username"] = Email
        Response = Session.post(
            "https://login.microsoftonline.com/common/GetCredentialType?mkt=en-US",
            headers=Headers,
            json=Payload
        )

        if Response.status_code == 200:
            Exists = not int(Response.json().get("IfExistsResult", 1))
            if Exists:
                print(f"{Colors.GREEN}[+] Valid: {Email}{Colors.RESET}")
                ValidEmails.append(Email)
            else:
                print(f"{Colors.RED}[-] Invalid: {Email}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Error checking {Email}{Colors.RESET}")

    return ValidEmails

def main():
    Parser = argparse.ArgumentParser(description="Check if email addresses are valid on Office.com")
    Parser.add_argument("--email", "-e", help="Single email to verify")
    Parser.add_argument("--emailList", "-eL", help="File containing emails to check (one per line)")

    Args = Parser.parse_args()

    EmailList = []

    if Args.email:
        EmailList.append(Args.email)
    if Args.emailList:
        with open(Args.emailList, "r") as File:
            EmailList.extend([Line.strip() for Line in File.readlines()])
            
    if not EmailList:
        print(f"{Colors.RED}[!] No emails provided. Use --email or --emailList argument.{Colors.RESET}")
    else:
        VerifyEmails(EmailList)

if __name__ == "__main__":
    main()
    # Parser = argparse.ArgumentParser(description="Check if email addresses are valid on Office.com")
    # Parser.add_argument("--email", "-e", help="Single email to verify")
    # Parser.add_argument("--emailList", "-eL", help="File containing emails to check (one per line)")

    # Args = Parser.parse_args()

    # EmailList = []

    # if Args.email:
    #     EmailList.append(Args.email)
    # if Args.emailList:
    #     with open(Args.emailList, "r") as File:
    #         EmailList.extend([Line.strip() for Line in File.readlines()])

    # if not EmailList:
    #     print(f"{Colors.RED}[!] No emails provided. Use --email or --emailList argument.{Colors.RESET}")
    # else:
    #     VerifyEmails(EmailList)
