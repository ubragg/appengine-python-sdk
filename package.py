import sys
import json
import re
import urllib2
import urllib
import zipfile
import shutil
import os
import subprocess
import xml.etree.ElementTree as ET

def run(cmd):
	p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

	while True:
		line = p.stdout.readline()

		print line.rstrip()

		if line == '':
			break

	if p.returncode > 0:
		raise Exception("command failed with returncode %s: %s" % (p.returncode, cmd))

def get_local_version():
	with open("package.json", "r") as f:
		package = json.load(f)

		if package.get("version") is None:
			raise Exception("Failed to retrieve local version")

		return package.get("version")

def set_local_version(version):
	with open("package.json", "r+") as f:
		package = json.load(f)
		package["version"] = version
		f.seek(0)
		json.dump(package, f, indent=2)
		f.truncate()

def get_remote_version():
	versions = []

	content = urllib2.urlopen("https://storage.googleapis.com/appengine-sdks")
	tree = ET.parse(content)
	root = tree.getroot()

	for contents in root.findall('{http://doc.s3.amazonaws.com/2006-03-01}Contents'):
		key = contents.find('{http://doc.s3.amazonaws.com/2006-03-01}Key').text

		m = re.search('^featured\/google_appengine_([0-9.]+).zip$', key)

		if m and m.group(1) not in versions:
			versions.append(m.group(1))

	versions.sort(reverse=True)

	if not len(versions):
		raise Exception("Failed to retrieve remote version")

	return versions[0]


if __name__ == '__main__':
	local_version = get_local_version()
	remote_version = get_remote_version()

	print "Local version: %s" % local_version
	print "Remote version: %s" % remote_version

	if remote_version > local_version:
		print "A new version is available, downloading %s" % remote_version

		urllib.urlretrieve("https://storage.googleapis.com/appengine-sdks/featured/google_appengine_%s.zip" % remote_version, "latest.zip")

		print "Extracting..."

		with zipfile.ZipFile("latest.zip", "r") as z:
			z.extractall("latest")

		if os.path.exists("google_appengine"):
			shutil.rmtree("google_appengine")

		os.rename("latest/google_appengine", "google_appengine")

		os.remove("latest.zip")
		shutil.rmtree("latest")

		set_local_version(remote_version)

	if "--commit" in sys.argv:
		run("git add --all && git commit -m \"%s\"" % remote_version)

	if "--tag" in sys.argv:
		run("git tag -m \"%s\"" % remote_version)

	if "--push" in sys.argv:
		run("git push --tags")

	if "--publish" in sys.argv:
		run("npm publish")
