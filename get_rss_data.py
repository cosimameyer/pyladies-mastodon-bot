from bs4 import BeautifulSoup
import requests
import json
import re
import json
import requests
import pickle

# Get data from GitHub
def get_json_file_names(BASE_URL, GITHUB_RAW_URL):
    result = requests.get(BASE_URL)

    soup = BeautifulSoup(result.text, 'html.parser')
    json_files = soup.find_all(title=re.compile("\.json$"))

    filename = [ ]
    for i in json_files:
            filename.append(f"{GITHUB_RAW_URL}/{i.extract().get_text()}")
            
    return filename

def get_json_data(BASE_URL, GITHUB_RAW_URL):
    json_files = get_json_file_names(BASE_URL, GITHUB_RAW_URL)
    contents_list = []

    for json_file in json_files:
        response = requests.get(json_file).text
        json_response = json.loads(response)
        contents_list.append(json_response)
        
    return contents_list
    
def extract_info(content):
    if 'rss_feed' in content:
        rss_feed = content['rss_feed']
        name = content['authors'][0]['name']
        if 'mastodon' in content['authors'][0]['social_media'][0].keys():
            mastodon = content['authors'][0]['social_media'][0]['mastodon']
        else:
            mastodon = ''
    
        return {"name": name, "rss_feed": rss_feed, "mastodon": mastodon}
    
def get_meta_data(contents_list):
    meta_data = [] 
    for content in contents_list:
        content_data = extract_info(content)
        if content_data != None:
            
            meta_data.append(content_data)
    return meta_data

if __name__ == "__main__":
    BASE_URL = "https://github.com/cosimameyer/awesome-rladies-blogs/tree/feature/mastodon-bot-compatibility/blogs"
    #"https://github.com/rladies/awesome-rladies-blogs/tree/main/blogs"
    GITHUB_RAW_URL = "https://raw.githubusercontent.com/cosimameyer/awesome-rladies-blogs/feature/mastodon-bot-compatibility/blogs"
    # "https://raw.githubusercontent.com/rladies/awesome-rladies-blogs/main/blogs"
    PICKLE_FILE = 'meta_data.pkl'
    contents_list = get_json_data(BASE_URL, GITHUB_RAW_URL)
    meta_data = get_meta_data(contents_list)
    
    with open(PICKLE_FILE, 'wb') as fp:
        pickle.dump(meta_data, fp)
    print(f'Meta data was saved successfully to file {PICKLE_FILE}')
