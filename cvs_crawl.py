import requests
CVS_ROOT_PATH = "/CVS/Entries"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_endpoints(url):

    endpoints = []
    web_text = requests.get(url+CVS_ROOT_PATH, headers=HEADERS).text
    if "\n" in web_text:
        web_text = web_text.splitlines()
    else:
        web_text = [web_text]
    for entry in web_text:
        if "/" in entry:
            part = entry.split("/")[1]
            part_two = part.split("//")[0]
            endpoints.append(part_two)
    return endpoints

def try_endpoints(url, endpoints):
    nested_endpoints = []
    for end in endpoints:
        full_url = url+"/"+end
        try:
            resp = requests.get(full_url, headers=HEADERS, allow_redirects=False)
            s_code = resp.status_code
            l_text = len(resp.text)
            if s_code == 200 and l_text > 100 and l_text not in [5, 6, 10, 15]:
               print(f"{s_code} - {full_url} - {l_text}")
            new_url = full_url+CVS_ROOT_PATH
            if (s_code == 302 or s_code == 301) and "." not in end:
                if requests.get(new_url, headers=HEADERS).status_code == 200:
                    #print(f"Found endpoint {full_url}")
                    nested_endpoints.append(full_url)
        except Exception as e:
            pass
    return nested_endpoints 
website = input("Enter Website to crawl:  ")
print(f"\n\n\nGetting endpoints for root url: {website}")
endpoints = get_endpoints(website)
print("Found endpoints:")
buffer = try_endpoints(website, endpoints)
while len(buffer) != 0:
    website = buffer.pop()
    print(f"Getting endpoints for {website}")
    endpoints = get_endpoints(website)
    print("Found endpoints....Trying:")
    buffer += try_endpoints(website, endpoints)


    




