""" Next Generation Programmers (NGP) installer script

 Usage: python installer.py [installation directory] [log file]

 This script installs all of the software required for the
 Next Generation Programmers course.
 This script requires Python to be installed.

 Any questions can be sent to j.bayne@warwick.ac.uk
"""

from __future__ import print_function
import sys
import os, os.path
import shutil
from subprocess import call, check_call, STDOUT
from programs import programs
from log import log
from ask import ask

# The list of programs the script will try to install
# from programs.py
install_list = [
	"Scratch",
	"Python",
	"Sublime Text",
	"Processing",
	"Multitran En-Ru Dict",
	"Google Chrome",
	"GIMP",
	"MIT App Inventor"
]


file_dir = os.getenv("file_dir","files")
script_dir = os.getenv("script_dir","scripts")
install_dir = os.getenv("install_dir",r"C:\NGP")
link_dir = r"C:\Users\Public\Desktop\NGP"

install_all = False
make_links = True
failure = False

print("Script starting with", file=log.file)
print("\tinstall_dir =",install_dir, file=log.file)
print("\tfile_dir =",file_dir, file=log.file)
print("\tscript_dir =",script_dir, file=log.file)
print("\tlink_dir =",link_dir, file=log.file)

if not os.access(install_dir, os.F_OK):
	try:
		os.makedirs(install_dir)
	except Exception:
		print("Could not create directory",install_dir,file=log)
		sys.exit(1)

if not os.access(install_dir, os.W_OK):
	print("Cannot modify contents of directory",install_dir,file=log)
	sys.exit(1)

install_all = ask("Install all programs?")
make_links = ask("Create shortcuts to created programs?")

if make_links:
	try:
		if not os.access(link_dir,os.F_OK):
			os.makedirs(link_dir)
		if not os.access(link_dir,os.W_OK):
			raise Exception()
	except Exception:
		if ask("Cannot create shortcuts. Continue?"):
			make_links = False
		else:
			del log
			sys.exit(1)


def make_link(name, target):
	target = target.format(install_dir=install_dir)
	dest = os.path.join(link_dir,name + ".lnk")

	if not os.access(target, os.F_OK):
		raise RuntimeError("Target program",target,"not found")
	

	call([r"scripts\createShortcut.bat", dest, target],
		 stdout=log.file,stderr=STDOUT,shell=True)

	if not os.access(dest, os.F_OK):
		raise RuntimeWarning("Could not create shortcut")

def run_installer(program):
	command = [x.format(install_dir=install_dir, file_dir=file_dir)
			   for x in [program.installer] + program.arguments]

	print("\t",command, file=log.file)
	check_call(command)

def install_program(program):
	if program.dependencies:
		print("Installing dependencies of", program.name, file=log)
	for dep_name in program.dependencies:
		try:
			install_program(programs[dep_name])
		except Exception as e:
			failure = True
			print("Error:",e, file=log.file)
			print("Installation of",dep_name," as dependency of",program.name,"failed!", file=log)
			if not ask("Installation of "+program.name+" may fail. Continue anyway?"):
				raise e


	print("Installing", program.name, file=log)
	if program.installer is not None:
		print("Running installer for", program.name, file=log.file)
		run_installer(program)

	if make_links and program.link is not None:
		print("Creating link for", program.name, file=log)
		make_link(program.name, program.link)

	if program.post_setup is not None:
		print("Running post-setup for", program.name, file=log.file)
		program.post_setup(install_dir, file_dir, script_dir)


if ask("Set wallpaper to NGP?", default="n"):
	print("Setting wallpaper", file=log.file)
	shutil.copy2(os.path.join(file_dir,"wallpaper.jpg"),install_dir)
	call(["reg","add","HKEY_CURRENT_USER\Control Panel\Desktop",
			"/v","Wallpaper",
			"/t","REG_SZ",
			"/d","C:\NGP\wallpaper.jpg",
			"/f"])

for program_name in install_list:
	program = programs[program_name]
	if install_all or ask("Install "+program_name+"?"):
		try:
			install_program(program)
		except Exception as e:
			failure = True
			print("Error:",e, file=log.file)
			print("Installation of",program_name,"failed!", file=log)
			if not ask("Install remaining programs?"):
				break

del log
if failure:
	sys.exit(1)