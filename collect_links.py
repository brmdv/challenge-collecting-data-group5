import os.path

from scrapers.immohans import ImmoHansList

# from scrapers.immoweb import ImmoWebList

# Output files
output_path = os.path.abspath("./data")

# Collect links from immohans.be
hans_links = []
for page_num in range(1, 100):
    # try until page x is no longer available
    page_url = "https://www.hansimmo.be/te-koop/pagina-" + str(page_num)
    new_list = ImmoHansList(page_url)
    try:
        hans_links += new_list.get_links()
    except:
        break

# write links to file
with open(os.path.join(output_path, "hans_links.txt"), "w") as file:
    for link in hans_links:
        file.write(link + "\n")
