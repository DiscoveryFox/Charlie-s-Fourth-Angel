import re

def useRegex(input):
    pattern = re.compile(r"^\\[\\+] Target opened the link!\\\\r\\\\n\\[\\+] IP: \\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\\b\\\\r\\\\n$")
    return pattern.match(input, re.IGNORECASE)


var = "[+] Target opened the link!\r\n[+] IP: 77.22.251.151\r\n"
print(var)

#pattern = re.compile("https://[\w-]*\.ngrok\.io")
#compiled_ip = re.compile(
#    "^\[\+] Target opened the link!\\r\\n\[\+] IP: \b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b\\r\\n$")

#print(pattern.match(var, re.IGNORECASE))

print(useRegex(var))
