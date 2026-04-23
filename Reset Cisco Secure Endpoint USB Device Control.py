import subprocess
import time
from pathlib import Path

subprocess.run (["C:\/Program Files\/Cisco\/AMP\/{{ .CSE_VERSION }}/sfc.exe", "-k", "{{ .PASSWORD }}"])
 
time.sleep(10)

file_path = Path("C:\Program Files\Cisco\AMP\local.xml")

text = file_path.read_text(encoding="utf-8")
text = text.replace("<download>1</download>", "<download>0</download>")
text = text.replace("<load>1</load>", "<load>0</load>")
file_path.write_text(text, encoding="utf-8")

time.sleep(5)
 
subprocess.run (["C:\/Program Files\/Cisco\/AMP\/{{ .CSE_VERSION }}/sfc.exe", "-s"])  
