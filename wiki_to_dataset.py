import requests
import re
from html.parser import HTMLParser
from multiprocessing.dummy import Pool as ThreadPool
import os

if __name__ == '__main__':
    # First, get HTML for parsing
    res = requests.get("https://theportalwiki.com/wiki/GLaDOS_voice_lines/ru#Portal_2")
    # Now lets initialize  and use parser
    replicas, urls = [], []
    class MyHTMLParser(HTMLParser):
        start_tag=False
        link = ""
        replica = ""
        is_portal2=False
        def handle_starttag(self, tag, attrs):
            if not self.is_portal2:
                if tag == "span":
                    list_id = [item for item in attrs if item[0] == 'id']
                    if len(list_id) != 0:
                        if list_id[0][1] == 'Portal_2':
                            self.is_portal2 =True
                return
            if tag == "a":
                # https://stackoverflow.com/a/2191707
                list_href = [item for item in attrs if item[0] == 'href']
                if len(list_href) != 0:
                    link = re.findall(r'^(https://[\w\/.\:]+.wav)$', list_href[0][1])
                    if len(link) != 0:
                        self.link = link[0]
                        self.start_tag=True
        def handle_endtag(self, tag):
            if tag == "a" and self.start_tag:
                self.start_tag=False
                if self.replica not in replicas and (not 'potatos' in self.link):
                    replicas.append(self.replica)
                    urls.append(self.link)
                self.replica=""
                self.link=""
        def handle_data(self, data):
            if self.start_tag:
                self.replica = data
    parser = MyHTMLParser()
    parser.feed(res.text)

    dest_folder='wavs'
    csv_file=""
    files = []
    def download_it(i):
        file = requests.get(urls[i])
        open(files[i], 'wb').write(file.content)
    for i in range(len(replicas)):
        replica = replicas[i].replace('"', '').replace('«', '').replace('»', '')
        filename = re.findall(r'(\w+).wav$', urls[i])[0]
        files.append(os.path.join(dest_folder, filename+'.wav'))
        csv_file=csv_file+f'{filename}|{replica}\n'
        if filename == "":
            print(replica)
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
    open('metadata.csv', 'wb').write(csv_file.encode())
    pool = ThreadPool(20)
    results = pool.map(download_it, range(len(urls)))
    pool.close()
    pool.join()