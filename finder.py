import multiprocessing
import os
import shutil
import pyfiglet
import requests
import time
import re
from core.controllers import Controller
from core.arguments import parse_args
# Clear the terminal and get terminal size
os.system('cls')
columns, rows = shutil.get_terminal_size()

# Generate the ASCII art text using pyfiglet
ascii_text = pyfiglet.figlet_format("Lyxtem", font="standard")

# Split the ASCII art text into lines
lines = ascii_text.split("\n")

# Calculate the position of each line in the middle of the terminal
positions = []
x = int(columns / 2 - len(max(lines, key=len)) / 2)  # Calculate x based on the length of the longest line
for i in range(len(lines)):
    y = int(rows / 2 - len(lines) / 2 + i)
    positions.append(y)


# Move the cursor to the calculated positions and print the text in a single print statement
print("\033[1m\033[32m", end="")
for i in range(len(lines)):
    print(f"\033[{positions[i]};{x}H{lines[i]}")
print("\033[1m\033[35m", end="")
print(f"\033[{positions[-1]+1};{x};{x}H[ MACHINE ] : Lyxtem finder")
print("\033[0m", end="")  # Reset font attributes and text color to default values

def get_content_from_sources():
  """
  Makes HTTP requests to the sources, retrieves the content, parses the content for
  proxy information, removes duplicates, and sorts the proxies.
  """
  # Add the URLs of the sources here
  sources = [
   'https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt',
   'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
   'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt',
   'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
   'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
   'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt',
   'https://raw.githubusercontent.com/omarwrf55/rice-ambatokamer2/main/data%20(3).txt',
   'https://raw.githubusercontent.com/omarwrf55/rice-ambatokamer2/main/data%20(2).txt',
   'https://raw.githubusercontent.com/omarwrf55/kol2/main/data%20(2).txt'
  ]

  # Make an HTTP request to each URL and retrieve the content
  content = []
  for url in sources:
    response = requests.get(url)
    content.append(response.text)

  # Parse the content for proxy information, remove duplicates, and sort the proxies
  proxies = []
  for text in content:
    regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
    proxies = re.findall(regex, str(content))
  proxies = list(set(proxies))
  proxies.sort()

  # Write the proxies to a file
  with open('proxies.txt', 'w') as f:
    for proxy in proxies:
      f.write(proxy + "\n")
  return proxies


if __name__ == "__main__":
    get_content_from_sources()
    multiprocessing.freeze_support()
    controller = Controller(
        arguments=parse_args()
    )
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass
