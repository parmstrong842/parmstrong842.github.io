import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime, timezone
from urllib.parse import quote
import re

# ----------------------------
# Podcast metadata
# ----------------------------
PODCAST_TITLE = "Cum Town Archive"
PODCAST_LINK = "https://archive.org/details/toxictethers-cum-town-archive"
PODCAST_DESCRIPTION = "Archive of Cum Town podcast episodes."
PODCAST_AUTHOR = "Cum Town"
PODCAST_IMAGE = "https://example.com/artwork.jpg"  # optional
PODCAST_LANGUAGE = "en-us"

# ----------------------------
# Internet Archive item ID
# ----------------------------
ITEM_ID = "toxictethers-cum-town-archive"
BASE_URL = f"https://archive.org/download/{ITEM_ID}/"

# ----------------------------
# File containing metadata
# ----------------------------
XML_FILE = "toxictethers-cum-town-archive_files.xml"  # your XML metadata
OUTPUT_FILE = "podcast.rss"

# ----------------------------
# Helper to format timestamp to RFC 822
# ----------------------------
def format_pubdate(timestamp):
  try:
      ts = int(timestamp)
      pub_date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
  except (ValueError, TypeError):
      pub_date = ""
  return pub_date

# ----------------------------
# Parse XML metadata
# ----------------------------
tree = ET.parse(XML_FILE)
root = tree.getroot()

rss_items = []

for file in root.findall('file'):
    # Full path of the file on Internet Archive
    raw_filename = file.attrib['name']  # e.g., "Cum Town Archive/1) Cum Town Archive/01 - Ep. 1 - The Original Cum Boys.mp3"

    if not raw_filename.lower().endswith(".mp3"):
        continue
    
    # URL-encode full path
    filename = quote(raw_filename)

    audio_url = f"{BASE_URL}{filename}"

    title = escape(file.findtext('title', default='Untitled'))
    description = escape(file.findtext('comment', default=''))
    pub_date = format_pubdate(file.findtext('mtime', default='0'))

    # Build RSS item
    item = f"""
    <item>
      <title>{title}</title>
      <description>{description}</description>
      <pubDate>{pub_date}</pubDate>
      <enclosure url="{audio_url}" type="audio/mpeg"/>
      <itunes:explicit>false</itunes:explicit>
    </item>
    """
    rss_items.append(item.strip())

# ----------------------------
# Build full RSS feed
# ----------------------------
rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{PODCAST_TITLE}</title>
    <link>{PODCAST_LINK}</link>
    <language>{PODCAST_LANGUAGE}</language>
    <description>{PODCAST_DESCRIPTION}</description>
    <itunes:author>{PODCAST_AUTHOR}</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:image href="{PODCAST_IMAGE}"/>
    {'\n'.join(rss_items)}
  </channel>
</rss>
"""

# ----------------------------
# Write RSS feed to file
# ----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(rss_feed)

print(f"RSS feed generated: {OUTPUT_FILE}")
