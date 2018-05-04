import subprocess, os 
import fcntl 
import time
import binascii
import sys
import shutil
import json
import zipfile

curr_dir = os.path.dirname(os.path.realpath(__file__))

if (len(sys.argv) != 2 and sys.argv[1] != "--configFile"):
	print "python yuesLib.py --configFile /path/to/config/file.json"
	sys.exit(0)


data = json.load(open(sys.argv[2]))

currLibPath = data["currentlyUsedLibrary"]["jarFilepath"]
targetLibPath = data["targetUpgradeLibrary"]["jarFilepath"]

currLibName = os.path.basename(currLibPath).replace('.jar', '')
targetLibName = os.path.basename(targetLibPath).replace('.jar', '')

old_lib_input = curr_dir + "/input/" + currLibName
new_lib_input = curr_dir + "/input/" + targetLibName

zip_ref = zipfile.ZipFile(currLibPath, 'r')
zip_ref.extractall(old_lib_input)
zip_ref.close()


zip_ref = zipfile.ZipFile(targetLibPath, 'r')
zip_ref.extractall(new_lib_input)
zip_ref.close()


cmd = "./startAnalysis.sh " + targetLibName + " " + currLibName + " " + curr_dir + "/input"
proc_shell = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, err) = proc_shell.communicate()
print err
