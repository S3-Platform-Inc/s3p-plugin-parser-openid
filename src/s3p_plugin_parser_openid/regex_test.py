import re

# Sample data as a list of strings
files = [
    "openid-4-verifiable-presentations-1_0.zip",
    "openid-4-verifiable-presentations-1_0.xml",
    "openid-4-verifiable-presentations-1_0.html",
    "openid-4-verifiable-presentations-1_0-23.zip",
    "openid-4-verifiable-presentations-1_0-23.html",
    "openid-4-verifiable-presentations-1_0.md",
    "openid-connect-rp-metadata-choices-1_0.html",
    "openid-connect-rp-metadata-choices-1_0-01.html",
    "openid-connect-rp-metadata-choices-1_0.txt",
    "openid-connect-rp-metadata-choices-1_0-01.txt",
    "openid-connect-rp-metadata-choices-1_0.xml",
    "openid-connect-rp-metadata-choices-1_0-01.xml",
    "openid-4-verifiable-presentations-1_0-22.zip",
    "openid-4-verifiable-presentations-1_0-22.html"
]

# Regular expression pattern
pattern = r'^(?!.*-\d+\.html$).*\.html$'

print(re.match(pattern, "openid-connect-rp-metadata-choices-1_0-01.html"))
if re.match(pattern, "openid-connect-rp-metadata-choices-1_0-01.html"):
    print('NO MATCH')
print(re.match(pattern, "openid-connect-rp-metadata-choices-1_0.html"))
if re.match(pattern, "openid-connect-rp-metadata-choices-1_0.html"):
    print('MATCH')

# Filtering HTML files
html_files = [file for file in files if re.match(pattern, file)]

# Output the result
print(html_files)