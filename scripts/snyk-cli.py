import json
import os
import re
import requests
import sys
import subprocess
import tarfile

def main(docker_command):

    proc = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    docker_image_id = out.decode("utf-8").strip('\n')

    
    snyk_token = os.getenv('SNYK_TOKEN')

    proc = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    docker_image_id = out.decode("utf-8").strip('\n')

    # Determine Protocol
    console_protocol = 'https' if tlscacert else 'http'

    # Base twistcli commnad to scan images
    snykcli_base_command = 'snyk test https://github.com/aarlaud-snyk/github-stats'

    proc = subprocess.Popen(snykcli_base_command, shell=True, stdout=subprocess.PIPE)
    stdout = proc.communicate()[0].decode('utf-8').strip('\n')

    # Concatenate twistcli executable with options from pipeline variables
    twistcli_exec = ' '\
        .join([snykcli_base_command, docker_image_id])

    # Execute command pipe stdout to variable and pipe to stdout and use for final exit code for threshold support
    proc = subprocess.Popen(twistcli_exec, shell=True)
    proc.communicate()

    if proc.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1])
