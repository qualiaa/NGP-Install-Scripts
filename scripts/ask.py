def ask(prompt, default="y"):
	result = raw_input(prompt + " [Y/n]: ")
	if not result:
		result = default
	if result.lower() == "y":
		return True
	elif result.lower() == "n":
		return False
	else:
		return ask(prompt,default)
