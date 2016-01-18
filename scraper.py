import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
from bs4 import BeautifulSoup as bs
import re
from mutagen.mp3 import MP3
import urllib
from urllib import urlretrieve
import json
import math
import itertools
import wave
import scraperwiki

ua = {'User-agent': 'Mozilla/5.0'}
# proxies = {'http': 'http://66.76.24.115:3128'}
def scrape_page(base_url):
        page = requests.get(base_url, headers= ua)
        soup = bs(page.text, 'lxml')

        links = soup.find('table', 'archives').find_all('a')
        for link in links:
            title_link = 'http://www.dailywav.com'+link['href']
            title_page = requests.get(title_link, headers= ua)
            title_soup = bs(title_page.text, 'lxml')
            files_links = title_soup.find('table', 'views-view-grid cols-3').find_all('a')

            for files_link in files_links:
                print files_link['href']
                movie_link = 'http://www.dailywav.com'+files_link['href']
                movie_name = files_link.text.strip()
                movie_page = requests.get(movie_link, headers= ua)
                movie_soup = bs(movie_page.text, 'lxml')
                next_link = ''
                try:
                    next_link = movie_soup.find('li', 'pager-next').find('a')['href']
                except:
                    pass
                if not next_link:
                    image_url = ''
                    try:
                        image_url = movie_soup.find('div', 'coverArt2').find('img')['src']
                    except:
                        try:
                            image_url = movie_soup.find('div', 'content quotes').find('img')['src']
                        except:
                            pass

                    nodes = movie_soup.find_all('article', 'node node-quotes node-promoted node-teaser clearfix')
                    for node in nodes:

                        file_url = node.find('div', 'content quotes').find('div', 'field field-name-field-quote-text field-type-text-long field-label-hidden').find_previous('a')['href']
                        transcript = node.find('div', 'content quotes').find('p').text.strip()
                        file_type = file_url.split('.')[-1]
                        tags = []
                        try:
                            tags = node.find('nav', 'taxonomy').find_all('div', 'field-item')
                        except:
                            pass
                        tagslist = []
                        for tag in tags:
                            tagslist.append(tag.find('span').text.strip().split('#')[-1].encode('utf-8'))
                        Tags = ', '.join(tagslist)
                        categories = 'Shows'
                        try:
                        #     opener = urllib.FancyURLopener(proxies)
                            filename, headers = urlretrieve(file_url)
                            sizeInBytes = headers['Content-Length']
                            audio = MP3(filename[0])
                            if audio.info.length < 1:
                                length = int(math.ceil(audio.info.length))
                            else:
                                length = int(round(audio.info.length))
                            duration = length
                        except:
                            try:
                                #  opener = urllib.FancyURLopener(proxies)
                                 filename, headers = urlretrieve(file_url)
                                 sizeInBytes = headers['Content-Length']
                                 wfile = wave.open (filename, "r")
                                 time = (1.0 * wfile.getnframes()) / wfile.getframerate()
                                 if time < 1:
                                     length = int(math.ceil(time))
                                 else:
                                     length = int(round(time))
                                 duration = length
                            except:
                                 duration = ''
                                 sizeInBytes = ''
                        
                        print movie_name.encode('utf-8'), transcript.encode('utf-8'), Tags
                        scraperwiki.sqlite.save(unique_keys=['fileUrl'], data={"sourceUrl": unicode(movie_link), "movie name": unicode(movie_name), "transcript": unicode(transcript), "fileType": file_type, "fileUrl":file_url, "duration":duration, "categories":categories, "imageUrl":image_url,"sizeInBytes" : sizeInBytes, "tags": unicode(Tags)})
                        yield movie_link, movie_name, transcript,  file_type, file_url, duration, categories, image_url, sizeInBytes

                else:
                    image_url = ''
                    try:
                        image_url = movie_soup.find('div', 'coverArt2').find('img')['src']
                    except:
                        try:
                            image_url = movie_soup.find('div', 'content quotes').find('img')['src']
                        except:
                            pass

                    nodes = movie_soup.find_all('article', 'node node-quotes node-promoted node-teaser clearfix')
                    for node in nodes:

                        file_url = node.find('div', 'content quotes').find('div', 'field field-name-field-quote-text field-type-text-long field-label-hidden').find_previous('a')['href']
                        transcript = node.find('div', 'content quotes').find('p').text.strip()
                        file_type = file_url.split('.')[-1]
                        categories = 'Shows'
                        tags = []
                        try:
                            tags = node.find('nav', 'taxonomy').find_all('div', 'field-item')
                        except:
                            pass
                        tagslist = []
                        for tag in tags:
                            tagslist.append(tag.find('span').text.strip().split('#')[-1].encode('utf-8'))
                        Tags = ', '.join(tagslist)
                        try:
                        #     opener = urllib.FancyURLopener(proxies)
                            filename,headers = urlretrieve(file_url)
                            sizeInBytes = headers['Content-Length']
                            audio = MP3(filename[0])
                            if audio.info.length < 1:
                                length = int(math.ceil(audio.info.length))
                            else:
                                length = int(round(audio.info.length))
                            duration = length
                        except:
                            try:
                                #  opener = urllib.FancyURLopener(proxies)
                                 filename, headers = urlretrieve(file_url)
                                 sizeInBytes = headers['Content-Length']
                                 wfile = wave.open (filename, "r")
                                 time = (1.0 * wfile.getnframes()) / wfile.getframerate()
                                 if time < 1:
                                     length = int(math.ceil(time))
                                 else:
                                     length = int(round(time))
                                 duration = length
                            except:
                                 duration = ''
                                 sizeInBytes = ''
                        print movie_name.encode('utf-8'), transcript.encode('utf-8'), Tags
                        scraperwiki.sqlite.save(unique_keys=['fileUrl'], data={"sourceUrl": unicode(movie_link), "movie name": unicode(movie_name), "transcript": unicode(transcript), "fileType": file_type, "fileUrl":file_url, "duration":duration, "categories":categories, "imageUrl":image_url, "sizeInBytes":sizeInBytes, "tags": unicode(Tags)})
                        yield movie_link, movie_name, transcript,  file_type, file_url, duration, categories, image_url, sizeInBytes

                    for paged in itertools.count():
                        movie_page = requests.get(movie_link+'?page={}'.format(paged+1), headers= ua)
                        print movie_link+'?page={}'.format(paged+1)
                        movie_soup = bs(movie_page.text, 'lxml')
                        find_node = ''
                        try:
                            find_node = movie_soup.find('div', 'content quotes')
                        except:
                            pass
                        if not find_node:
                            break
                        image_url = ''
                        try:
                            image_url = movie_soup.find('div', 'coverArt2').find('img')['src']
                        except:
                            try:
                                image_url = movie_soup.find('div', 'content quotes').find('img')['src']
                            except:
                                pass

                        nodes = movie_soup.find_all('article', 'node node-quotes node-promoted node-teaser clearfix')
                        for node in nodes:

                            file_url = node.find('div', 'content quotes').find('div', 'field field-name-field-quote-text field-type-text-long field-label-hidden').find_previous('a')['href']
                            transcript = node.find('div', 'content quotes').find('p').text.strip()
                            file_type = file_url.split('.')[-1]
                            tags = []
                            try:
                                tags = node.find('nav', 'taxonomy').find_all('div', 'field-item')
                            except:
                                pass
                            tagslist = []
                            for tag in tags:
                                tagslist.append(tag.find('span').text.strip().split('#')[-1].encode('utf-8'))
                            Tags = ', '.join(tagslist)
                            categories = 'Shows'
                            try:
                                # opener = urllib.FancyURLopener(proxies)
                                filename, headers = urlretrieve(file_url)
                                sizeInBytes = headers['Content-Length']
                                audio = MP3(filename[0])
                                if audio.info.length < 1:
                                    length = int(math.ceil(audio.info.length))
                                else:
                                    length = int(round(audio.info.length))
                                duration = length
                            except:
                                try:
                                #      opener = urllib.FancyURLopener(proxies)
                                     filename, headers = urlretrieve(file_url)
                                     sizeInBytes = headers['Content-Length']
                                     wfile = wave.open (filename, "r")
                                     time = (1.0 * wfile.getnframes()) / wfile.getframerate()
                                     if time < 1:
                                         length = int(math.ceil(time))
                                     else:
                                         length = int(round(time))
                                     duration = length
                                except:
                                     duration = ''
                                     sizeInBytes = ''
                            print movie_name.encode('utf-8'), transcript.encode('utf-8'), Tags
                            scraperwiki.sqlite.save(unique_keys=['fileUrl'], data={"sourceUrl": unicode(movie_link), "movie name": unicode(movie_name), "transcript": unicode(transcript), "fileType": file_type, "fileUrl":file_url, "duration":duration, "categories":categories, "imageUrl":image_url, "sizeInBytes":sizeInBytes, "tags": unicode(Tags)})
                            yield movie_link, movie_name, transcript,  file_type, file_url, duration, categories, image_url, sizeInBytes


def scrape():
   with open('data7.json', 'w') as outfile:
        sounds = {}
        lists = []
        base_url = 'http://www.dailywav.com/archives/shows/'
        s = scrape_page(base_url)
        for l in s:
            json_dic = {}
            json_dic['sourceUrl']=l[0]
            json_dic['movie name']=l[1]
            json_dic['transcript']=l[2]
            json_dic['fileType']=l[3]
            json_dic['fileUrl']=l[4]
            json_dic['duration']=l[5]
            json_dic['categories']=l[6]
            json_dic['imageUrl']=l[7]
            json_dic['sizeInBytes'] = l[8]
            #json_dic['tags'] = l[9]
            # print json_dic['movie name']
            lists.append(json_dic)
        sounds['sounds'] = lists
        json.dump(sounds, outfile, indent = 4)



if __name__ == '__main__':
    scrape()
