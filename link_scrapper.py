import urllib.parse
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

class_id = {
    "bbc": "sc-eb7bd5f6-0 fYAfXe",
    "timesofindia":"_s30J clearfix",
    "cnn": "paragraph inline-placeholder vossi-paragraph-primary-core-light",
    "indianexpress":"story_details"
}

def find_value_in_url(url):
    # Parse the URL to get the path and query parameters
    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.split('/')
    domain_name = parsed_url.netloc.lower()
    
    # Check if the domain name contains any of the keys
    for key in class_id.keys():
        if domain_name.find(key)!= -1:
            return class_id[key]
    
    # Flatten the query parameters
    query_params_flat = [param for sublist in urllib.parse.parse_qs(parsed_url.query).values() for param in sublist]
    
    # Combine path components and flattened query parameters into a single list
    url_parts = path_components + query_params_flat
    
    # Convert the combined list to lowercase
    url_parts = [part.lower() for part in url_parts]
    
    # Iterate through the keys of the dictionary
    for key in class_id.keys():
        # Check if the key exists in the URL parts
        if key in url_parts:
            # Return the value associated with the found key
            return class_id[key]
    
    # If none of the keys were found, return None
    return None

# Example usage
# url = 'https://www.bbc.com/news/articles/cw55lgpnxgdo'
# url ='https://edition.cnn.com/2024/05/23/asia/china-military-drills-taiwan-second-day-intl-hnk/index.html'
# url ='https://timesofindia.indiatimes.com/city/kolkata/betrayal-honeytrap-skinning-the-what-why-and-how-of-bangladesh-mps-murder-in-kolkata/articleshow/110393250.cms'
# url ='https://indianexpress.com/article/political-pulse/pm-modi-kartarpur-gurdwara-1971-9349708/'
def scrapenews(url):
    value = find_value_in_url(url)
    news=[]
# print(value)  # This should now correctly print the value associated with the key found in the URL, or None if no key is found

    response = requests.get(url)
    

    # displaying the title
    # print("Title of the website is : ")
    

    if response.status_code == 200:
        # Parse the webpage content with BeautifulSoup
        soup1 = BeautifulSoup(urlopen(url),features="html.parser")
        news.append(soup1.title.get_text())
        # print(soup1.title.get_text())
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find elements with the specified class name
        elements_with_class = soup.find_all(class_=value)
        
        # Extract and print the text content of each element
        for element in elements_with_class:
            news.append(element.text.strip())
            # print(element.text.strip())
        return news
    else:
        return []

# scrapenews(url)