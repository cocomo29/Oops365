<div style="text-align: center;">
    <h1>Oops365 🚀</h1>
</div>

Oops365 is a modular security testing tool for Microsoft 365. It helps assess authentication mechanisms, generate and verify emails, perform password spraying, and enumerate MFA settings.  

## Features  
- **CHECK** – Identify if a domain is **Managed** or **Federated**  
- **GENERATE** – Generate potential email addresses based on names and a domain  
- **VERIFY** – Check which generated emails are valid in Microsoft 365  
- **SPRAY** – Perform password spraying against valid accounts  
- **MFASWEEP** – Determine if MFA is enforced on valid accounts  

## Installation  
```bash  
git clone https://github.com/cocomo29/Oops365.git  
cd Oops365  
pip3 install -r requirements.txt
python3 Oop365.py
```
## Usage  
```bash
python3 Oops365.py <MODULE> <arguments>  
```

### Example Commands
* Check if a domain is managed or federated:
```bash
python3 Oops365.py check example.com  
```
* Generate email variations:
```bash
python3 Oops365.py generate "john cena" example.com --output emails.txt  
```
* Verify valid Microsoft 365 emails:
```bash
python3 Oops365.py verify -eL emails.txt
```

* Perform password spraying:
```bash
python3 Oops365.py spray -eL emails.txt t -p ponioail@@123    
```
* Enumerate MFA settings:
```bash
python3 Oops365.py mfasweep -e salad@cato.com -p appetizer  
```

# ToDo
* Proper Readme
* User agents upgrade/randomize
* utils.py maybe
* keyboard interrupt try except
* required = true
* and?
* requirements.txt



Contributions are alwas welcome, this script itself is inspired and combination of multiple amazing scripts i got to know from [pwnedlabs](http://pwnedlabs.io/) including but not limited to [uwg](https://github.com/hac01/uwg), [o365enum](https://github.com/gremwell/o365enum), [Oh365UserFinder](https://github.com/dievus/Oh365UserFinder), [MFASweep](https://github.com/dafthack/MFASweep), [Mfade](https://github.com/ibaiC/MFade) and more  <3
