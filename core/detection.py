import requests
import json
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException

roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_607A3AF742350DD123ED8CE1A8CE766BA5C905CE2EBA47D1AD0D23B8CE78EB07F93D7880A407D7EC4206EDCFA2A7BD3922E2539EB3E029EC872301DE6149728850DE81E529A1004CE38C617876D70A497780492D01375EE33AF00F242C4EEE7736794E53B57780814B379D3BCF8DD3212B0F1F1463031304B0C15EA56520990F3E94952547CD87FCC204B44A94FB49298230F8ABD0859CD36C524530A445845272AC4FC57795CD42F967991752A1E7DC283D1B46AA8E8FCA1ABE41B6E39B715525FBAC6186B07FD3C6D9028D736D510A0E635BC31D630F3F6197A3CA30547E4C7204FE006B1A5E709F8829297C6E4C824DD66A12ED73DBD1DE15E6119881254DA46AA29178F26AB104D1F991E6F96E82D04004DC88B70BDC309FAFDFF81092E77238E9CDC102B18D80D79B463FC14DBA17EF5657E6F21AA64E042694BB42894409E3AB1B5D12CBBC8A933990E85B1B207CBE99FABE4CD0A6EC7B2B5614DE198154B5E24F3A2BBED33D7FF0BE55FCB7D41B29AD8FFB972297759C239ADDC0914F312B0796BAF91B610865ABD10AB90B9314511B317185C2692F3838065F815D2D193C3C019306E33D2C211CEDDA2CA28E3471EA00ADDCFAA3A5CDE2DA24B4C734CC409114A6F3FBBDF7B07D59EC9621C364BDFEF494A9B2BAD31A7451B7541A922F83EA4D007BC23C959FCD56381330ACED5E0F3BE267C602B90A5D9D5FE223CD5CDEB8132FC67778D29F9FE39F3A83F4CFA991526E512480A2C80A6499CB710E86A65B7355C299DDAB5135CEE35BB5AC06639A96497CB1C5A7652AF43E4205B201EFDE04F94D1849455DDA334CAA0917238238A166A1142CD8740BC97A53E8A64BDA99EC2AEC2E2F04B59F7F0A3A9715D4FC169BBAFCD889018C3955D5FE5DD163F67E14E91CBB51C7041470AFF48FBFF68708DC6B57AE18CD17707A04823110E54FF8A63DAB738FDF56ECC3CD1CE10DBFF020B410C4A281CCD590422FEF9C70518559AF3E687E75D90D9F466614822B106CDE14AE60FCBF0E0B40A36F1807951CDB7994"}
def clothings(id):
  clothings = 0
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
    check = session.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30").result()
    check = check.json()
  except RequestException as e:
    print(e)
    return 0

  def get_page(cursor=None):
      nonlocal check
      try:
        if cursor:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30&cursor={cursor}"
        else:
          url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30"
        check = session.get(url).result().json()
      except RequestException as e:
        print(e)
        return 0
      return check

  while True:
      if "data" in check:
          clothings += len(check['data'])
      if "nextPageCursor" not in check or not check['nextPageCursor']:
          break
      else:
          check = get_page(check['nextPageCursor'])
  return clothings

def robux(id):
  # Import Local Cookie Variable
  global roblox_cookie
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://economy.roblox.com/v1/groups/{id}/currency', cookies=roblox_cookie, timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    data = json.loads(response.text)
    if "robux" in data:
      robux = data.get("robux", 0)
    else:
      robux = 0
  except RequestException as e:
    print(e)
    return 0
  return robux

def gamevisits(id):
  # Create a FuturesSession object
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))

  # Make the API request asynchronously
  try:
    future = session.get(f'https://games.roblox.com/v2/groups/{id}/games?accessFilter=All&sortOrder=Asc&limit=100', timeout=5)
  except RequestException as e:
    print(e)
    return 0

  # Wait for the request to complete and load the response into a dictionary
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
      
  except RequestException as e:
    print(e)
    return 0

  # If there are no games, return "None"
  if not data:
    return 0
  
  # Find the total number of visits for all games
  total_visits = 0
  for game in data:
    visits = game["placeVisits"]
    total_visits += visits
  return total_visits
  
def gamecount(id):
  session = FuturesSession()
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
  session.mount('https://', HTTPAdapter(max_retries=retries))
  try:
      # Send the request asynchronously and return a Future object
      future = session.get(f'https://games.roblox.com/v2/groups/{id}/games?accessFilter=All&sortOrder=Asc&limit=100', timeout=5)
  except RequestException as e:
    print(e)
    return 0
  try:
    response = future.result()
    os = json.loads(response.text)
    if "data" in os:
      data = os["data"]
    else:
      data = 0
  except RequestException as e:
    print(e)
    return 0
  if not data:
    return 0
  else:
    return len(data)

def groupimage(id):
  # Create a session with retries enabled
  session = FuturesSession()
  retry = Retry(connect=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('https://', adapter)

  # Send the request asynchronously and return a Future object
  future = session.get(f'https://thumbnails.roblox.com/v1/groups/icons?groupIds={id}&size=150x150&format=Png&isCircular=false', timeout=5)

  # Wait for the request to complete and handle any errors that may occur
  try:
    response = future.result()
    icon_url = response.json()
    if "data" in icon_url and len(icon_url["data"]) > 0:
       image = icon_url["data"][0]["imageUrl"]
    else:
       image = "https://cdn.discordapp.com/icons/1078288294707744809/7d803a2786cede6dd1b0d0fb0bc52577.png?size=1024"

  except RequestException as e:
    print(e)
    image = "https://cdn.discordapp.com/icons/1078288294707744809/7d803a2786cede6dd1b0d0fb0bc52577.png?size=1024"
  return image 
