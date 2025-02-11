import requests
import argparse
import json
from colorama import Fore, Style

def checkIntraId(targetDomain):
    url = f"https://login.microsoftonline.com/getuserrealm.srf?login={targetDomain}"

    try:        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "NameSpaceType" in data and data["NameSpaceType"] == "Managed":
            print(f"{Fore.GREEN}[+] {targetDomain} is using Azure AD (Managed Authentication){Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] {targetDomain} is using Federated Authentication (ADFS or similar){Style.RESET_ALL}")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Request failed: {e}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Check if a domain uses Azure AD or Federated Authentication")
    parser.add_argument("--domain", "-d", required=True, help="Target domain to check")
    args = parser.parse_args()

    checkIntraId(args.domain)

if __name__ == "__main__":
    main()
    # parser = argparse.ArgumentParser(description="Check if a domain uses Azure AD or Federated Authentication")
    # parser.add_argument("--domain", "-d", required=True, help="Target domain to check")
    # args = parser.parse_args()

    # checkIntraId(args.domain)
