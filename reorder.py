import xml.etree.ElementTree as ET
import os
from urllib.parse import unquote  # to decode %20 → space
import re

# Paths
rss_file = 'podcast.rss'           # original RSS file
audio_dir = '/home/parms/cumtown/toxictethers-cum-town-archive/Cum Town Archive/1) Cum Town Archive'            # directory with audio files
output_rss = 'podcast_ordered.xml' # new RSS file

def leading_number(name: str) -> int:
    match = re.match(r'\s*(\d+)', name)
    return int(match.group(1)) if match else float('inf')

files_in_dir = sorted(os.listdir(audio_dir), key=leading_number)

# Load the RSS XML
tree = ET.parse(rss_file)
root = tree.getroot()
channel = root.find('channel')

# Map filenames from <enclosure> URLs to their <item> elements
filename_to_item = {}
for item in channel.findall('item'):
    enclosure = item.find('enclosure')
    if enclosure is not None:
        file_url = enclosure.attrib.get('url', '')
        filename = unquote(os.path.basename(file_url))
        print(filename)
        filename_to_item[filename] = item

# Remove all <item> elements from the channel
for item in channel.findall('item'):
    channel.remove(item)

# Re-add items in the same order as the directory files
for filename in files_in_dir:
    if filename in filename_to_item:
        item = filename_to_item[filename]
        channel.append(item)  # no skipping

# Save the reordered RSS feed
tree.write(output_rss, encoding='utf-8', xml_declaration=True)
print(f"Reordered RSS saved to {output_rss}")
