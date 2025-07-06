

import os

import subprocess

pre_command = "unset DISPLAY;"
command = pre_command + "echo 'Hello, World!'"
use_shell = True  # Set to False if you want to use a list of arguments instead of a shell command

process_sub = subprocess.Popen(
    command if use_shell else command.split(),
    shell=use_shell,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)


stdout, stderr = process_sub.communicate(timeout=5)

print("STDOUT:", stdout.decode())
print("STDERR:", stderr.decode())