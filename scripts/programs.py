from __future__ import print_function
import os
import shutil
import ask
from subprocess import check_call, STDOUT

class Program:
	def __init__(self, name, installer, args=[], deps=[], post_setup=None, link=None):
		self.name = name
		self.installer = installer
		self.arguments = args
		self.dependencies = deps
		self.post_setup = post_setup
		self.link = link

def post_java(install_dir, file_dir, script_dir):
	#Set the JAVA_HOME environment variable if it is not already set
	
	if os.getenv("JAVA_HOME") is None:
		try:
			check_call(["setx", "/m","JAVA_HOME",os.path.join(install_dir,"Java","JRE")])
		except Exception:
			raise OSError("Insufficient permissions to modify environment variables")

def post_ai(install_dir, file_dir, script_dir):
	# App Inventor needs two things:
	#  1. A Java security exception for http://localhost:8888/,
	#  2. A 32-bit JRE instead of the provided 64-bit one.
	security_dir = "C:/Windows/Sun/Java/Deployment/security"
	exception_file = os.path.join(security_dir,"exception.sites")
	if not os.access(security_dir, os.F_OK):
		os.makedirs(security_dir)

	with open(exception_file, 'a') as f:
		print("http://localhost:8888/", file=f)


	original_jdk = os.path.join(install_dir,"AppInventor","JDK")
	new_jdk = os.path.join(install_dir,"Java","JDK")

	shutil.rmtree(original_jdk)
	shutil.copytree(new_jdk,original_jdk)

programs = {
	"Scratch":
		Program("Scratch",
			installer=r"{file_dir}\Scratch-448.exe",
			args=["-silent", "-eulaAccepted", "-location", "{install_dir}"],
			deps=["Adobe AIR"],
			link=r"{install_dir}\Scratch 2\Scratch 2.exe"),
	"MIT App Inventor":
		Program("MIT App Inventor",
			installer=r"{file_dir}\AI2U 64bit v3.8.exe",
			args=["/VERYSILENT",
				  "/SUPPRESSMSGBOXES",
				  "/NORESTART",
				  r"/DIR={install_dir}\AppInventor"],
			deps=["Java"],
			post_setup=post_ai,
			link=r"{install_dir}\AppInventor\startAI.cmd"),
	"Processing":
		Program("Processing",
			installer=r"{install_dir}\7z\7z.exe",
			args=["x",r"{file_dir}\processing-3.1.2-windows32.zip","-o{install_dir}"],
			deps=["7z"],
			link=r"{install_dir}\processing-3.1.2\processing.exe"),
	"Sublime Text":
		Program("Sublime Text",
			installer=r"{file_dir}\Sublime Text Build 3114 Setup.exe",
			args=["/SILENT",
				  "/SUPPRESSMSGBOXES",
				  "/NORESTART",
				  r'/DIR={install_dir}\Sublime Text'],
			link=r"{install_dir}\Sublime Text\sublime_text.exe"),
	"Python":
		Program("Python",
			installer=None,
			link=r"{install_dir}\Python\python.exe"),
	"Multitran En-Ru Dict":
		Program("Multitran En-Ru Dictionary",
			installer=r"{file_dir}\mt_big_demo.exe",
			args=["-s", r'-d{install_dir}\Dictionary'],
			link=r"{install_dir}\Dictionary\network\multitran.exe"),
	"Java":
		Program("Java", installer=None, deps=["JDK", "JRE"], post_setup=post_java),
	"JDK":
		Program("JDK",
			installer=r"{file_dir}\jdk-8u102-windows-i586.exe",
        	args=["/s", r'INSTALLDIR={install_dir}\Java\JDK']),
    "JRE":
    	Program("JRE",
    		installer=r"{file_dir}\jre-8u102-windows-i586.exe",
        	args=["/s", r'INSTALLDIR={install_dir}\Java\JRE']),
	"Adobe AIR":
		Program("Adobe AIR", 
			installer=r"{file_dir}\AdobeAIRInstaller.exe",
			args=["-silent","-eulaAccepted"]),
	"7z":
		Program("7z", 
			installer=r"{file_dir}\7z1602.exe", args=["/S",r'/D={install_dir}\7z']),
	"Google Chrome":
		Program("Google Chrome",
			installer="msiexec",
			args=["/i", r"{file_dir}\googlechromestandaloneenterprise.msi", "/quiet"]),
	"GIMP":
		Program("GIMP",
			installer=r"{file_dir}\gimp-2.8.18-setup.exe",
			args=["/VERYSILENT",
				  "/SUPPRESSMSGBOXES",
				  "/NORESTART",
				  r'/DIR={install_dir}\GIMP'],
			link=r"{install_dir}\GIMP\bin\GIMP-2.8.exe")
}