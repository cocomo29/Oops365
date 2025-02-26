import argparse
import importlib
import sys
from colorama import Fore, Style

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('modules')

MODULES = {
    "check": "modules.CheckDomain",
    "generate": "modules.GenerateEmails",
    "verify": "modules.VerifyEmails",
    "spray": "modules.SprayAttack",
    "mfasweep": "modules.MFASweep",
}

def banner():
    print(Fore.CYAN + r"""
   ___                      _____   __   ____  
  / _ \   ___   _ __   ___ |___ /  / /_ | ___| 
 | | | | / _ \ | '_ \ / __|  |_ \ | '_ \|___ \ 
 | |_| || (_) || |_) |\__ \ ___) || (_) |___) |
  \___/  \___/ | .__/ |___/|____/  \___/|____/ 
               |_|  """ + Fore.YELLOW + """         v1.0.0 by @cocomo29""" + Fore.RESET + """
""")
    
    print(Fore.RED + Style.BRIGHT + "  Oops, I pwned it again! 💀\n" + Style.RESET_ALL)

    print(Fore.GREEN + "  [*] CHECK     " + Fore.WHITE + "- Check if a domain has O365 services enabled")
    print(Fore.GREEN + "  [*] GENERATE  " + Fore.WHITE + "- Generate potential email addresses from a given domain")
    print(Fore.GREEN + "  [*] VERIFY    " + Fore.WHITE + "- Validate email addresses against O365")
    print(Fore.GREEN + "  [*] SPRAY     " + Fore.WHITE + "- Perform a password spraying attack on verified emails")
    print(Fore.GREEN + "  [*] MFASWEEP  " + Fore.WHITE + "- Search for MFA enforcement gaps across multiple services\n")

    print(Fore.MAGENTA + "  Usage:" + Fore.YELLOW + " python3 Oops365.py <MODULE> [OPTIONS]\n")
    print(Fore.MAGENTA + "  Example:" + Fore.YELLOW + " python3 Oops365.py CHECK --domain example.com")
    print("           " + Fore.YELLOW + "python3 Oops365.py SPRAY -eList emails.txt -p 'Shinzowosasageyo!' --delay 2.0\n" + Style.RESET_ALL)



def main():
    parser = argparse.ArgumentParser(description="Oops365 - Modular Office 365 Tool")
    
    parser.add_argument("module", type=str, nargs="?", choices=MODULES.keys(), help="Module to run (CHECK, GENERATE, VERIFY, SPRAY, MFASWEEP)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the selected module")

    args = parser.parse_args()

    if args.module is None:
        banner()
    else:
        module_name = MODULES[args.module.lower()]  

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "main"):
                sys.argv = [args.module] + args.args
                try:
                    module.main()
                except KeyboardInterrupt:
                    print(f"\n{Fore.RED}[!] Operation interrupted by user. Exiting gracefully, Bye!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Module '{args.module}' does not have a 'main()' function!{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}[!] Failed to import module: {module_name}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Operation interrupted by user. Exiting gracefully...{Style.RESET_ALL}")
