import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime
from urllib.parse import quote  # <- this handles spaces and special characters

# ----------------------------
# Podcast metadata
# ----------------------------
PODCAST_TITLE = "Cum Town Archive"
PODCAST_LINK = "https://example.com"           # your website or podcast page
PODCAST_DESCRIPTION = "Archive of Cum Town podcast episodes."
PODCAST_AUTHOR = "Cum Town"
PODCAST_IMAGE = "https://example.com/artwork.jpg"
PODCAST_LANGUAGE = "en-us"

# ----------------------------
# Base URL for GitHub Pages
# ----------------------------
BASE_URL = "https://parmstrong842.github.io/"  # Update this to your GitHub Pages URL

# ----------------------------
# Files
# ----------------------------
XML_FILE = "episodes_metadata.xml"  # Your metadata XML
OUTPUT_FILE = "podcast.xml"

# ----------------------------
# Helper to convert timestamp to RFC 822 format
# ----------------------------
def format_rfc822(timestamp):
    dt = datetime.utcfromtimestamp(int(timestamp))
    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

# ----------------------------
# Parse XML metadata
# ----------------------------
tree = ET.parse(XML_FILE)
root = tree.getroot()
rss_items = []

for file in root.findall('file'):
    raw_filename = file.attrib['name'].split('/')[-1]  # e.g., "01 - Ep. 1 - The Original Cum Boys.mp3"
    
    # URL-encode filename for GitHub Pages
    filename = quote(raw_filename)
    
    audio_url = f"{BASE_URL}{filename}"                        # full URL for enclosure

    # Extract metadata from XML
    title = escape(file.findtext('title', default='Untitled'))
    description = escape(file.findtext('comment', default=''))
    pub_date = format_rfc822(file.findtext('mtime', default='0'))

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
# Build the full RSS feed
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
# Write the RSS feed to a file
# ----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(rss_feed)

print(f"RSS feed generated: {OUTPUT_FILE}")
