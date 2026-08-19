import os
import requests
from pathlib import Path
from html import escape

USERNAME = "FloRdgs"
API_KEY = os.environ["LASTFM_API_KEY"]

params = {
"method": "user.gettopartists",
"user": USERNAME,
"api_key": API_KEY,
"period": "1month",
"limit": 5,
"format": "json",
}

response = requests.get(
"https://ws.audioscrobbler.com/2.0/",
params=params,
timeout=30,
)

response.raise_for_status()
data = response.json()

if "error" in data:
raise RuntimeError(
f"Last.fm error {data['error']}: {data['message']}"
)

artists = data["topartists"]["artist"]

html = """

<div align="center">
<table>
<tr>
"""

for artist in artists:
name = escape(artist["name"])
url = escape(artist["url"], quote=True)
playcount = escape(str(artist.get("playcount", "0")))

```
image = ""

for img in artist.get("image", []):
    if img.get("size") == "extralarge":
        image = img.get("#text", "")
        break

if not image:
    for img in artist.get("image", []):
        if img.get("size") == "large":
            image = img.get("#text", "")
            break

if image:
    image = escape(image, quote=True)

    html += f"""
```

<td align="center">
  <a href="{url}">
    <img src="{image}" width="120" height="120" alt="{name}">
  </a>
  <br>
  <b>{name}</b>
  <br>
  <sub>{playcount} écoutes</sub>
</td>
"""

html += """

</tr>
</table>
</div>
"""

readme = Path("README.md")
content = readme.read_text(encoding="utf-8")

start = "<!-- LASTFM_TOP_ARTISTS_START -->"
end = "<!-- LASTFM_TOP_ARTISTS_END -->"

if start not in content:
raise RuntimeError("LASTFM_TOP_ARTISTS_START absent du README.md")

if end not in content:
raise RuntimeError("LASTFM_TOP_ARTISTS_END absent du README.md")

start_index = content.index(start) + len(start)
end_index = content.index(end)

new_content = (
content[:start_index]
+ "\n"
+ html
+ "\n"
+ content[end_index:]
)

readme.write_text(new_content, encoding="utf-8")

print("Top artists Last.fm mis à jour.")
for artist in artists:
print(
f"- {artist['name']}: "
f"{artist.get('playcount', 0)} écoutes"
)
