``` python
#!/usr/bin/env python3
import requests
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom
import os

# === CONFIG ===
API_KEY = 'redacted'  # Replace with your AbuseIPDB API key
OUTPUT_FILE = '/var/ossec/etc/lists/malicious_ips_list.xml'  # Adjust path if needed

# AbuseIPDB blacklist endpoint
URL = '[https://api.abuseipdb.com/api/v2/blacklist](https://api.abuseipdb.com/api/v2/blacklist)'

headers = {
    'Accept': 'application/json',
    'Key': API_KEY
}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    new_ips = [entry['ipAddress'] for entry in data['data']]

    # Load existing XML if it exists
    existing_ips = set()
    if os.path.exists(OUTPUT_FILE):
        tree = parse(OUTPUT_FILE)
        root = tree.getroot()
        for value in root.findall('value'):
            existing_ips.add(value.text)

    # Merge new IPs with existing ones
    all_ips = existing_ips.union(new_ips)

    # Create XML structure
    root = Element('list', name="malicious_ips_list", key="srcip")
    for ip in sorted(all_ips):
        SubElement(root, 'value').text = ip

    # Pretty print XML
    xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="  ")

    # Write to file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(xml_str)

    print(f"[+] Saved {len(all_ips)} malicious IPs to {OUTPUT_FILE}")

except Exception as e:
    print(f"[-] Error fetching or saving data: {e}")

```
