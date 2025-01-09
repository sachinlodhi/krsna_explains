import requests
from bs4 import BeautifulSoup
import json


# function to assign data to the dictionary
def assign_to_dict(shloka_num, shloka_dev, shloka_en, shloka_translation, shloka_purport):
    my_dict = {}
    # print(shloka_num)
    # generating chapter num
    chapter = shloka_num.split(".")[1].rsplit()[0]
    shloka = shloka_num.split(".")[2]

    my_dict = {'chapter' : chapter, 'shloka' : shloka, 'sanskrit' : shloka_dev,
               'english': shloka_en, 'translation' : shloka_translation, 
              'purport': shloka_purport}
    return my_dict


def start():
    # Getting all the response from the main page
    response = requests.get('https://vedabase.io/en/library/bg/')
    if response.status_code == 200:
        print("yes")

    # creating bs4 object
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    sources = soup.find_all('a')
    chapter_links = []
    shlokas_links = []
    shlokas_dict_list = []
    dict_list = []
    # ctr = 0 
    # link to the chapters
    for source in sources:
        if "/en/library/bg/" in source['href'] and "Chapter" in source.text: # this is kinda static condition
            
            # print(source)
            url = "https://www.vedabase.io" + source['href']
            # print(url)
            
            # trying to check the status for the shlokas
            print(f"checking response for chepter: {url.split('/')[-2]}")
            
            # link to the verses
            response = requests.get(url)
            
            # extracting each verse l
            verse_soup = BeautifulSoup(response.content, "html.parser")
            # print(verse_soup.prettify())
    
            # getting verses links
            verses_links = verse_soup.find_all('a')
            # iterate over the links that contains the links to the shloka
            ctr = 0
            for verse in verses_links:
                if "TEXT" in verse.text:
    
                    # generate the url to get the content from each shloka
                    verse_url = "https://vedabase.io" + verse['href'] 
                    resp = requests.get(verse_url)
                    shloka_soup = BeautifulSoup(resp.content, "html.parser")
                    ctr+=1
                    # if ctr == 4:
                        # print(shloka_soup.find(id='content'))
                    for br in shloka_soup.find_all('br'):
                        br.replace_with('\n')
                    
                    
                    # get the whole section of shloka, meaning and purport
                    shloka_num = shloka_soup.find(id='content').find('h1').text
                    shloka_dev = shloka_soup.find(class_ = 'r r-devanagari').text
                    shloka_en = shloka_soup.find(class_ = 'r r-lang-en r-verse-text').text
                    shloka_translation = shloka_soup.find(class_ = 'r r-lang-en r-translation').text
    
                    # assign first 
                    # sometimes there is no purport for very simple and factual shlokas in that case assign none 
                    # shloka_purport = shloka_soup.find(class_ ='r r-lang-en r-paragraph')
                    # print(repr(shloka_dev))
                    print(f"Processing {shloka_num}")
                    try:
                        shloka_purport = shloka_soup.find(class_ ='r r-lang-en r-paragraph').text
                        
                    except:
                        print(f"No purport for {shloka_num}")
                        shloka_purport = None
                    # print(verse_url)
                    # this returns the dictionary
                    data = assign_to_dict(shloka_num, shloka_dev, shloka_en, shloka_translation, shloka_purport)
                    dict_list.append(data)
    
                    # print(shloka_purport, "\n")
                    # print(f"{shloka_num} \n{shloka_dev} {shloka_en} {shloka_translation} {shloka_purport}")
    
    # now dumping it in a file
    with open("data_collection/bhagavad_gita.json", "w", encoding="utf-8") as json_file:
        json.dump(dict_list, json_file, ensure_ascii=False, indent=4)              



if __name__ == "__main__":
    start()
                    
                
            
    
                
                                
    
