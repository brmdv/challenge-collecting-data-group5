import os.path

from scrapers.immoweb import ImmoWebList

# from scrapers.immoweb import ImmoWebList

# Output files
output_path = os.path.abspath("./data")

# Collect links from immoweb.be
page_url = "https://www.immoweb.be/en"
immoweb_links = ImmoWebList(page_url)
immoweb_links.scrape()

# write links to file
with open(os.path.join(output_path, "immoweb_links.txt"), "w") as file:
    for link in immoweb_links._links:
        file.write(link + "\n")
