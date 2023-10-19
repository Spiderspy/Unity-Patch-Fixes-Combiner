import requests
from bs4 import BeautifulSoup
import time
import webbrowser

# Define the Unity version
unity_version = "2023.1"  # Change this variable as needed

# Define the starting and ending patch versions
start_version = "10"  # Change these variables as needed
end_version = "15"    # Change these variables as needed

# Initialize an empty dictionary to store list items grouped by category
grouped_list_items = {}

# Loop through the patch versions
for version in range(int(start_version), int(end_version) + 1):
    version_string = f"{unity_version}.{version}"
    print(f"Started processing version {version_string}...")

    url = f"https://unity.com/releases/editor/whats-new/{version_string}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all headers and check if they contain "Fixes"
        for header in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
            if "Fixes" in header.get_text():
                print("Found 'Fixes' header.")
                start_time = time.time()  # Start timing
                # Find the nearest ul element
                ul_element = header.find_next('ul')
                if ul_element:
                    # Find all list items within the ul element
                    list_items = ul_element.find_all('li')
                    list_item_texts = [item.get_text(strip=True) for item in list_items]
                    if version_string not in grouped_list_items:
                        grouped_list_items[version_string] = []
                    grouped_list_items[version_string].extend(list_item_texts)
                end_time = time.time()
                processing_time = end_time - start_time
                print(f"Processed in {processing_time:.2f} seconds.")

    print(f"Finished processing version {version_string}.")

# Organize list items into groups based on the text before ":"
grouped_list = {}
for version, list_items in grouped_list_items.items():
    for item in list_items:
        item_category = item.split(":")[0]
        if item_category not in grouped_list:
            grouped_list[item_category] = []
        grouped_list[item_category].append(item)

# Create an HTML file with the organized list items
html_content = f"<html><body><h1>List of Unity Fixes</h1>"
html_content += f"<h2>Unity {unity_version}.{start_version} <span>&#10140;</span> {unity_version}.{end_version}</h2>"

for category, items in grouped_list.items():
    html_content += f"<h3>{category} Fixes</h3><ul>"
    for item in items:
        html_content += f"<li>{item}</li>"
    html_content += "</ul>"

html_content += "</body></html>"

with open(f"unity_{unity_version}_{start_version}_{end_version}_fixes.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_content)

# Open the HTML file in a web browser
webbrowser.open(f"unity_{unity_version}_{start_version}_{end_version}_fixes.html")

print(f"HTML file created and opened in a web browser for Unity {unity_version}.")
print("Wishlist Midnight Horde ;)")
