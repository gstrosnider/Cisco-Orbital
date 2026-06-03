###Linux script to reset a password for a given account on the endpoint using passwd.

import subprocess

def set_passwd(new_passwd):
    passwd = new_passwd + "\n" + new_passwd + "\n"
    proc = subprocess.Popen(['/usr/bin/passwd', '{{ .USERNAME }}'], stdin=subprocess.PIPE)
    proc.communicate(passwd.encode("utf-8"))

set_passwd("{{ .NEWPASSWORD }}")
