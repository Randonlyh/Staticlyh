#!/usr/bin/python3
import sys
import datetime
from pathlib import Path
import os
import re

import markdown

def help_message():
	print("Arguments:")
	print("--help [-h] - Prints this message")
	print("build [b] \"path/to/source\" - Compiles the pages in _post and creates link pages for each subfolder inside it")
	sys.exit()

def build():
	path = sys.argv[2]

	# Loads the template html
	template = path + "/posts.htemplate"
	with open(template, 'r') as f:
		template = f.read()
	
	# Grabs all the post paths
	posts_path = path + "/_posts"
	posts_path = Path(posts_path)
	md_files = gather_files(posts_path)

	# Find all folders
	folders = []
	for entry in posts_path.iterdir():
		if entry.is_dir():
			if "/_drafts" not in str(entry):
				entry_split = str(entry).split("/")
				folders.append(entry_split[-1])

	# Flip the list for later when link pages are being generated (newest post will appear first)
	md_files = list(reversed(md_files))

	# Calculate destination paths and store date if it exists in the original filename

	html_files = md_files.copy()
	date_of = list()
	date_exists = list()
	title = list()
	for i in range(len(html_files)):
		html_files[i] = html_files[i].replace("_", "")
		html_files[i] = html_files[i].replace(" ", "-")
		html_files[i] = html_files[i].replace(".md", ".html")
		
		date_exists.append(find_date(html_files[i]))

		if date_exists[i] == True:
			date_of.append(html_files[i].split("/")[-1][:10])
		else:
			date_of.append("Unknown")
		
	for i in range(len(md_files)):
		with open(md_files[i], 'r', encoding="utf-8") as input:
			title.append(input.readline())
			text = input.read()
		
		print("Creating: " + html_files[i])

		# Parsing out the title
		title[i] = title[i].replace("# ", "")
		title[i] = title[i].replace("\n", "")

		# Overwriting the template with data
		out = template
		out = out.replace("--text", markdown.markdown(text))
		out = out.replace("--title", title[i])
		out = out.replace("--year", datetime.datetime.now().strftime("%Y"))
		out = out.replace("--dateof", (date_of[i]))

		with open(html_files[i], 'w', encoding="utf-8") as output:
			output.write(out)
	
	if not folders:
		create_link_page("", path, md_files, html_files, title, date_of)
	else:
		for entry in folders:
			create_link_page(entry, path, md_files, html_files, title, date_of)
	
	print("All done!")
	return

def gather_files(path='.'):
	folders = []
	for entry in path.iterdir():
		if entry.is_dir():
			if "/_drafts" not in str(entry):
				folders.append(entry)

	list_of_files = []
	if not folders:
		for file in sorted(path.iterdir()):
			if str(file).endswith(".md"):
				list_of_files.append(str(file))
	
	for folder in folders:
		for file in sorted(folder.iterdir()):
			if str(file).endswith(".md"):
				list_of_files.append(str(file))
	
	if not list_of_files:
		print("Error, no files to work on found. Aborting...")
		sys.exit()
	
	return list_of_files

def find_date(filename):
	x = re.search("\\d{2,4}-\\d{1,2}\\-\\d{1,2}", filename)
	if not x:
		return False
	
	return True

def create_link_page(name, path, md_files, html_files, title, date):
	out = []
	path_obj = Path(path + name + ".htemplate")
	if not path_obj.exists():
		print("Skipping: " + name + ".html (corresponding .htemplate does not exist)")
		return

	print("Creating: " + name + ".html (links page)")
	with open(path + name + ".htemplate", 'r', encoding="utf-8") as page:
		out = page.read()

	out = out.replace("--year", datetime.datetime.now().strftime("%Y"))

	# Keeping the part of the file that may need copy pasting
	repeatable = out
	repeatable = repeatable[repeatable.index("--/"):repeatable.index("/--")]
	out = out.replace(repeatable, "")
	repeatable = repeatable[3:]
	repeatable += "/--"

	for i in range(len(md_files)):
		post_split = html_files[i].split("/")
		
		if name != "":
			if post_split[-2] != name:
				continue
		
		print("Adding: " +  html_files[i] + " to " + name + ".html")
		text = ""

		with open(md_files[i], 'r', encoding='utf-8') as page:
			page.readline()
			text = page.read()
		
		# Preview of the post
		text = text[:200]
		text = text.replace("#", "")
		text += "..."
		text = markdown.markdown(text)

		# Getting the page link
		link_split = html_files[i].split("/")
		if name == "":
			link = link_split[-2] + "/" + link_split[-1]
		else:
			link = link_split[-3] + "/" + link_split[-2] + "/" + link_split[-1]

		# Pasting in other page info
		out = out.replace("/--", repeatable)
		out = out.replace("--description", text)
		out = out.replace("--dateof", date[i])
		out = out.replace("--title", title[i])
		out = out.replace("--path", link)

	out = out.replace("--/", "")
	out = out.replace("/--", "")

	if name == "":
		with open(path + "posts.html", 'w', encoding="utf-8") as page:
			page.write(out)
	else:
		with open(path + name + ".html", 'w', encoding="utf-8") as page:
			page.write(out)
	
	return

if __name__ == "__main__":
	if len(sys.argv) < 2:
		help_message()

	elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
		help_message()

	elif sys.argv[1] == 'build' or sys.argv[1] == 'b':
		if len(sys.argv) < 3:
			print("Error, path not supplied. Aborting...")
			sys.exit()
		
		build()
