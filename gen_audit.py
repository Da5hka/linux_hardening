import subprocess

print()
print("\033[1;95m-------------------------[users and groups audit in progress]-------------------------")

def check_signature(command, pattern):
    output = subprocess.getoutput(command)
    signature = output.count(pattern)
    if signature == 0:
        return "\033[91m[ BAD ]"
    else:
        return "\033[92m[ GOOD ]"

status = check_signature("grep -cP '^PASS_MAX_DAYS\s+90$' /etc/login.defs", "PASS_MAX_DAYS\s+90$")
print("\033[39m[*] Checking Maximum number of days of password usage\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '^PASS_MIN_DAYS\s+5$' /etc/login.defs", "PASS_MIN_DAYS\s+5$")
print("\033[39m[*] Checking Minimum number of days between password changes\t\t\t\t{}".format(status))

status = check_signature("grep -cP '^PASS_WARN_AGE\s+10$' /etc/login.defs", "PASS_WARN_AGE\s+10$")
print("\033[39m[*] Checking Number of days warning before password expiration\t\t\t\t{}".format(status))

status = check_signature("useradd -D | grep -cP '^INACTIVE=30$'", "INACTIVE=30$")
print("\033[39m[*] Checking users locking after inactivity\t\t\t\t\t\t{}".format(status))

status = check_signature("id -gn root| grep -cP '^root$'", "root")
print("\033[39m[*] Checking root primary group\t\t\t\t\t\t\t\t{}".format(status))

installed = subprocess.getoutput("dpkg-query -W -f='${Status}' libpam-cracklib 2>/dev/null | grep -c 'ok installed'")
if installed == "0":
    status = "\033[91m[ BAD ]"
else:
    status = "\033[92m[ GOOD ]"
print("\033[39m[*] Checking libpam-cracklib installation\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*minlen=14.*' /etc/pam.d/common-password", "minlen=14")
print("\033[39m[*] Checking minimum password length\t\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*reject_username.*' /etc/pam.d/common-password", "reject_username")
print("\033[39m[*] Checking if username in password is allowed\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*minclass=4.*' /etc/pam.d/common-password", "minclass=4")
print("\033[39m[*] Checking if Password complexity class\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1.*' /etc/pam.d/common-password", "dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1")
print("\033[39m[*] Checking if Password complexity class\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*maxrepeat=2.*' /etc/pam.d/common-password", "maxrepeat=2")
print("\033[39m[*] Checking if passwords with 2 same consecutive characters are rejected\t\t{}".format(status))

status = check_signature("grep -cP '.*remember=24.*' /etc/pam.d/common-password", "remember=24")
print("\033[39m[*] Checking last 24 passwords is enabled\t\t\t\t\t\t{}".format(status))

status = check_signature("grep -cP '.*auth required pam_tally2\.so onerr=fail audit silent deny=5 unlock_time=1200.*' /etc/pam.d/login", "auth required pam_tally2\.so onerr=fail audit silent deny=5 unlock_time=1200")
print("\033[39m[*] Checking if accounts locked out after unsuccessful login attempts\t\t\t{}".format(status))

status = check_signature("grep -cP '^-:wheel:ALL EXCEPT LOCAL.*' /etc/security/access.conf", "^-:wheel:ALL EXCEPT LOCAL")
print("\033[39m[*] Checking if non-local logins to privileged accounts are not allowed\t\t\t{}".format(status))

status = check_signature("grep -cP '.*delay=10000000.*' /etc/pam.d/login", "delay=10000000")
print("\033[39m[*] Checking delay time between login prompts\t\t\t\t\t\t{}".format(status))

print("\033[0m")
