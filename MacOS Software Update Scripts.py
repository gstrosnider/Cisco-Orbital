import subprocess
import sys
import getpass

def update_macos():
  try:
    process = subprocess.Popen(
      ['softwareupdate', '-ia'],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True
    )

    password = "{{ .orbital_param_password }}"
print("opening file: %s" % password)
file = print(password)
    
    output, error = process.communicate(input='yes\n')

    if output:
      print(f"Update result:\n{output}")
    if error:
      print(f"Error during software update:\n{error}")

  except Exception as e:
    print(f"Error during software update: {e}")

if __name__ == "__main__":
  update_macos()
  
  
import subprocess
import sys
import getpass

def update_macos():
    password = "{{ .systempassword }}"
    
    update_command = "sudo softwareupdate -i -a -R"
    
    run_update_command = f"echo {password} | {update_command}"
        
if __name__ == "__main__":
    update_macos()
    
Software Update Tool

Finding available software
Downloading macOS Sonoma 14.6.1

Downloaded: macOS Sonoma 14.6.1
Failed to authenticate    
    
2024-08-21 16:07:50.919 softwareupdate[64033:37282395] XType: Using static font registry.
Password: Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
  File "<string>", line 15, in <module>
  File "<string>", line 12, in update_macos
  File "/opt/cisco/orbital/python/lib/python3.10/subprocess.py", line 526, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command 'echo Password' | sudo -S sudo softwareupdate -i -a' returned non-zero exit status 1.



from subprocess import *
import sys
import os 

password = "{{ .systempassword }}"

process = Popen("sudo softwareupdate -i -a -R", shell=True)

run_update_command = f"sudo -SA {process} {password}"