from bs4 import BeautifulSoup
import requests
import os
import json

save_file_name = "water_quality_dates.txt"

url = "https://www.waterboards.ca.gov/drinking_water/certlic/drinkingwater/EDTlibrary.html"
response = requests.get(url)


# Step 2: Check if the request was successful (status code 200)
if response.status_code == 200:
    # Step 3: Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific <a> tag
    specific_a_tag = soup.find('a', {'download': True, 'href': 'documents/edtlibrary/sdwis4.zip'})
    p_element = None
    last_update_date = ""

    if specific_a_tag:
        # Find the parent <p> element
        p_element = specific_a_tag.find_parent('p')

        if p_element:
            # Print the content of the <p> element
            last_update_date = p_element.get_text(strip=True)

            start_marker = "SDWIS4.tab"
            end_marker = "SDWIS3.tab"

            start_index = last_update_date.find(start_marker)
            end_index = last_update_date.find(end_marker)

            if start_index != -1 and end_index != -1:
                content_between_markers = last_update_date[start_index + len(start_marker):end_index]

                # Slice to only include the content included in the ()
                start_marker = "("
                end_marker = ")"
                start_index = last_update_date.find(start_marker)
                end_index = last_update_date.find(end_marker)
                if start_index != -1 and end_index != -1:
                    content_between_markers = last_update_date[start_index + len(start_marker):end_index]
                    last_update_date = content_between_markers

                    update_index = last_update_date.find("update")

                    if update_index != -1:
                        content_after_update = last_update_date[update_index + len("update") + 1:]
                        last_update_date = content_after_update
                        print(last_update_date)
                    else:
                        print("Update not found in the string.")
                else:
                    print("Markers for () not found in the string")
            else:
                print("Markers not found in the string.")
        else:
            print("Parent <p> element not found.")
    else:
        print("Specific <a> tag not found.")

    

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")