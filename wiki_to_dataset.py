import wave
import requests
import re
from html.parser import HTMLParser
from multiprocessing.dummy import Pool as ThreadPool
import os
import sys
import time

# based on https://stackoverflow.com/a/34482761
class progressbar_obj:
    def __init__(self, count, prefix="", size=60, out=sys.stdout):
        self.count = count
        self.next = 0
        self.prefix = prefix
        self.size = size
        self.out = out
        self.start = time.time() # time estimate start
        self.show(0.1) # avoid div/0
    def show(self, j):
        x = int(self.size*j/self.count)
        # time estimate calculation and string
        if j == 0:
            remaining = 0
        else:
            remaining = ((time.time() - self.start) / j) * (self.count - j)        
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(f"{self.prefix}[{u'█'*x}{('.'*(self.size-x))}] {j}/{self.count} Est wait {time_str}", end='\r', file=self.out, flush=True)
        if j == self.count:
            print("\n", flush=True, file=self.out)
    def show_next(self):
        self.next = self.next + 1
        self.show(self.next)

def check_it(replica: str, link: str):
    if 'potatos' in link:
        return False
    if '[' in replica or ']' in replica:
        return False
    if 'НЕТ!' in replica or 'А-а!' in replica:
        return  False
    if 'GLaDOS_sp_catapult_fling_sphere_peek_failuretwo02_ru' in link:
        return False
    return True

if __name__ == '__main__':
    # First, get HTML for parsing
    res = requests.get("https://theportalwiki.com/wiki/GLaDOS_voice_lines/ru#Portal_2")
    # Now lets initialize  and use parser
    replicas, urls = [], []
    class MyHTMLParser(HTMLParser):
        start_tag=False
        replica = ""
        is_portal2=False
        def handle_starttag(self, tag, attrs):
            if not self.is_portal2:
                if tag == "h2":
                    list_id = [item for item in attrs if item[0] == 'id']
                    if len(list_id) != 0:
                        if list_id[0][1] == 'Portal_2':
                            self.is_portal2 =True
                return
            else:
                if tag == "li":
                    self.start_tag=True
                if tag == "a":
                    # https://stackoverflow.com/a/2191707
                    list_href = [item for item in attrs if item[0] == 'href']
                    if len(list_href) != 0:
                        link = re.findall(r'^(https://[\w\/.\:]+.wav)$', list_href[0][1])
                        if len(link) != 0:
                            if self.replica not in replicas and check_it(self.replica, link[0]):
                                replicas.append(self.replica.replace('»', '').replace('«', '').replace('"', ''))
                                urls.append(link[0])
        def handle_data(self, data):
            if self.start_tag:
                self.replica = data
                self.start_tag=False
    parser = MyHTMLParser()
    parser.feed(res.text)

    dest_folder='wav'
    csv_file=""
    files = []
    progress = progressbar_obj(len(urls), prefix="Downloading: ")
    def download_it(i: int):
        if not os.path.exists(files[i]):
            file = requests.get(urls[i])
            tmp_name = files[i]+'.part'
            open(tmp_name, 'wb').write(file.content)
            os.rename(tmp_name, files[i])
        progress.show_next()
    for i in range(len(replicas)):
        replica = replicas[i]
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
    # verify all files are downloaded
    progress = progressbar_obj(len(files), prefix="Verifying: ")
    for i in range(len(files)):
        progress.show_next()
        if not os.path.exists(files[i]):
            raise FileNotFoundError(f"Error downloading file: {files[i]}")
        else:
            with wave.open(files[i]) as wav_file:
                metadata = wav_file.getparams()
                if metadata.nchannels != 1 or metadata.sampwidth != 2 or metadata.framerate != 44100:
                    raise ValueError(f"File {files[i]} has incorrect format: {metadata}")
    print("All files downloaded and verified successfully.")