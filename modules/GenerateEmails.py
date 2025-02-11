import argparse
from colorama import Fore, Style

def generateEmails(firstName, lastName, domain, outputFile=None):
    emailCombinations = []

    # If lastName exists, generate full name-based emails
    if lastName:
        emailCombinations.extend([
            f"{firstName}.{lastName}@{domain}",
            f"{firstName}{lastName}@{domain}",
            f"{firstName[0]}_{lastName}@{domain}",
            f"{firstName[0]}.{lastName}@{domain}",
            f"{firstName[0]}{lastName}@{domain}",
            f"{firstName}.{lastName[0]}@{domain}",
            f"{firstName}{lastName[0]}@{domain}",
            f"{firstName}.{lastName}_@{domain}",
            f"{firstName}_{lastName}_@{domain}",
            f"{firstName}_{lastName}@{domain}",
            f"{firstName}.{lastName[0]}@{domain}",
            f"{firstName[0]}.{lastName[0]}@{domain}",
            f"{lastName}.{firstName}@{domain}",
            f"{firstName}-{lastName}@{domain}",
            f"{lastName}.{firstName[0]}@{domain}",
        ])
    else:  # If only firstName is provided
        emailCombinations.extend([
            f"{firstName}@{domain}",
            f"{firstName[0]}{firstName}@{domain}",
            f"{firstName[0]}.{firstName}@{domain}"
        ])

    print(f"{Fore.BLUE}[*] Generated Email Combinations:{Style.RESET_ALL}")
    for email in emailCombinations:
        print(f"  {Fore.GREEN}{email}{Style.RESET_ALL}")

    if outputFile:
        with open(outputFile, "w") as file:
            for email in emailCombinations:
                file.write(f"{email}\n")
        print(f"{Fore.YELLOW}[*] Results saved to {outputFile}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Generate common email patterns for a given name and domain")
    parser.add_argument("--name", "-n", required=True, help="First and last name (or just first name)")
    parser.add_argument("--domain", "-d", required=True, help="Target domain for email generation")
    parser.add_argument("--output", "-o",help="Save results to a file")

    args = parser.parse_args()

    names = args.name.split()
    firstName = names[0]
    lastName = names[1] if len(names) > 1 else None  # Assign None if there's no last name

    generateEmails(firstName, lastName, args.domain, args.output)

if __name__ == "__main__":
    main()
    # parser = argparse.ArgumentParser(description="Generate common email patterns for a given name and domain")
    # parser.add_argument("--name", "-n", required=True, help="First and last name (or just first name)")
    # parser.add_argument("--domain", "-d", required=True, help="Target domain for email generation")
    # parser.add_argument("--output", "-o",help="Save results to a file")

    # args = parser.parse_args()

    # names = args.name.split()
    # firstName = names[0]
    # lastName = names[1] if len(names) > 1 else None  # Assign None if there's no last name

    # generateEmails(firstName, lastName, args.domain, args.output)
