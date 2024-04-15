import subprocess

def check_status(command, expected_value):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return "[ GOOD ]" if output.decode().strip() == expected_value else "[ BAD ]"
    except subprocess.CalledProcessError:
        return "[ BAD ]"

def main():
    print("\033[1;95m-------------------------[users and groups audit in progress]-------------------------")

    max_days_status = check_status("grep -cP '^PASS_MAX_DAYS\\s+90$' /etc/login.defs", "1")
    print(f"[*] Checking Maximum number of days of password usage\t\t\t\t\t{max_days_status}")

    min_days_status = check_status("grep -cP '^PASS_MIN_DAYS\\s+5$' /etc/login.defs", "1")
    print(f"[*] Checking Minimum number of days between password changes\t\t\t\t{min_days_status}")

    warn_age_status = check_status("grep -cP '^PASS_WARN_AGE\\s+10$' /etc/login.defs", "1")
    print(f"[*] Checking Number of days warning before password expiration\t\t\t\t{warn_age_status}")

    inactive_status = check_status("useradd -D | grep -cP '^INACTIVE=30$'", "1")
    print(f"[*] Checking users locking after inactivity\t\t\t\t\t\t{inactive_status}")

    root_group_status = check_status("id -gn root | grep -cP '^root$'", "1")
    print(f"[*] Checking root primary group\t\t\t\t\t\t\t\t{root_group_status}")

    libpam_installed_status = check_status("dpkg-query -W -f='${Status}' libpam-cracklib 2>/dev/null | grep -c 'ok installed'", "1")
    print(f"[*] Checking libpam-cracklib installation\t\t\t\t\t\t{libpam_installed_status}")

    min_password_length_status = check_status("grep -cP '.*minlen=14.*' /etc/pam.d/common-password", "1")
    print(f"[*] Checking minimum password length\t\t\t\t\t\t\t{min_password_length_status}")

    reject_username_status = check_status("grep -cP '.*reject_username.*' /etc/pam.d/common-password", "1")
    print(f"[*] Checking username rejection\t\t\t\t\t\t\t\t{reject_username_status}")

    dcredit_status = check_status("grep -cP '.*dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1.*' /etc/pam.d/common-password", "1")
    print(f"[*] Checking if Password complexity class\t\t\t\t\t\t{dcredit_status}")

    maxrepeat_status = check_status("grep -cP '.*maxrepeat=2.*' /etc/pam.d/common-password", "1")
    print(f"[*] Checking if passwords with 2 same consecutive characters are rejected\t\t{maxrepeat_status}")

    remember_status = check_status("grep -cP '.*remember=24.*' /etc/pam.d/common-password", "1")
    print(f"[*] Checking last 24 passwords is enabled\t\t\t\t\t\t{remember_status}")

    tally2_status = check_status("grep -cP '.*auth required pam_tally2\.so onerr=fail audit silent deny=5 unlock_time=1200.*' /etc/pam.d/login", "1")
    print(f"[*] Checking if accounts locked out after unsuccessful login attempts\t\t\t{tally2_status}")

    access_conf_status = check_status("grep -cP '^-:wheel:ALL EXCEPT LOCAL.*' /etc/security/access.conf", "1")
    print(f"[*] Checking if non-local logins to privileged accounts are not allowed\t\t\t{access_conf_status}")

    delay_status = check_status("grep -cP '.*delay=10000000.*' /etc/pam.d/login", "1")
    print(f"[*] Checking delay time between login prompts\t\t\t\t\t\t{delay_status}")

if __name__ == "__main__":
    main()
