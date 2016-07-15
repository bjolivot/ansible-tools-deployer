#!/usr/bin/python
import ConfigParser
import subprocess
import os
import sys
import git
from git import Repo

def create_directory_structure():
    if not os.path.exists(working_dir):
        os.makedirs(working_dir) 
    if not os.path.exists(working_dir +"/" + Config.get("main","tools_root_dir")):
        os.makedirs(working_dir +"/" + Config.get("main","tools_root_dir"))
    if not os.path.exists(working_dir +"/" + Config.get("main","playbooks_root_dir")):
        os.makedirs(working_dir +"/" + Config.get("main","playbooks_root_dir"))
    if not os.path.exists(working_dir +"/" + Config.get("main","roles_root_dir")):
        os.makedirs(working_dir +"/" + Config.get("main","roles_root_dir"))


def is_binary_available(binary_name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([binary_name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def get_git(path,dir_name,git_uri):
    if os.path.isdir(path + "/" + dir_name) and git_override == "False":
        return False
    if os.path.isdir(path + "/" + dir_name):
        #subprocess.call(["cd " + path + "/" + dir_name + " && git pull"])
        git.cmd.Git(path + "/" + dir_name).fetch("origin")
        git.cmd.Git(path + "/" + dir_name).reset("--hard")
        #print("cd " + path + "/" + dir_name + " && git pull")
        return True
    else:
        #subprocess.call(["git", "clone " + git_uri + " " + path + "/" + dir_name])
        Repo.clone_from(git_uri, path + "/" + dir_name)
        #print("cd " + path + " && git clone " + git_uri + " " + dir_name)
        return True

def git_loop(ini_key,path):
    git_list = Config.options(ini_key)
    for git_line_key in git_list:
        if get_git(path,git_line_key,Config.get(ini_key,git_line_key)):
            print("Git :" + ini_key + ": OK")
        else:
            print("Git :" + ini_key + ": Not changed, try git_override if needed")



def get_roles():
    git_loop("git_roles_list",working_dir +"/" + Config.get("main","roles_root_dir"))





Config = ConfigParser.ConfigParser()
Config.read(__file__ + ".ini")

working_dir = Config.get("main","working_dir")
git_override = Config.get("main","git_override")

print("over : " + git_override)

if not is_binary_available("ansible"):
  print "\n[error] Ansible must be installed"
  sys.exit(1)

if not is_binary_available("git"):
  print "\n[error] git must be installed"
  sys.exit(1)



create_directory_structure()

get_roles()


