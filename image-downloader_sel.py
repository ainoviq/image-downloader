import os
import sys
import time
import pandas as pd
import json
import argparse
import requests


python_version = sys.version_info.major
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

if python_version == 3:
    import urllib.parse
    import urllib.request
    urljoin = urllib.parse.urljoin
    urlretrieve = urllib.request.urlretrieve
    quote = urllib.parse.quote

    # configure headers
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)
else:
    from urllib.parse import urlparse
    import urllib
    urljoin = urlparse.urljoin
    urlretrieve = urllib.urlretrieve
    quote = urllib.quote

    # configure headers
    class AppURLopener(urllib.FancyURLopener):
        version = user_agent
    urllib._urlopener = AppURLopener()


def fix_url(url):
    url = quote(str(url), safe="%/:=&?~#+!$,;'@()*[]")
    return url


headers = {
    'User-Agent': "insomnia/2022.5.1",
    'Content-Type': "application/json",
    "Accept": "*/*"
}


def download(url, opt):
    link = fix_url(url)
    # link = f'https:{link}'
    try:
        print(f'Info: downloading from {link}')
        with requests.get(url=link, data="", headers=headers, stream=True) as res:
            content_type = res.headers.get('Content-Type')
            if content_type == 'image/jpeg' or content_type == 'image/jpg':
                ext = 'jpg'
            elif content_type == 'image/png':
                ext = 'png'
            elif content_type == 'image/gif':
                ext = 'gif'
            elif content_type == 'image/webp':
                ext = 'webp'
            else:
                print("Warning: unknown image content type %s" % content_type)
                return
            filename = f'{int(time.time_ns())}'
            with open(os.path.join(opt.output, f'{filename}.{ext}'), "wb") as img_file:
                for chunk in res.iter_content(chunk_size=None):
                    img_file.write(chunk)
    except Exception as e:
        print(f'Warning: failed to download. See log: \n{e}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str,
                        default=None, help='input json file')
    parser.add_argument('-o', '--output', type=str,
                        default='output', help='output directory')
    opt = parser.parse_args()
    print(opt)

    if os.path.exists(opt.output):
        print('Info: output directory exists')
    else:
        os.makedirs(opt.output)
        print('Info: output directory created as %s' % opt.output)

    with open(opt.file, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())

        dataframe = pd.DataFrame(data=data)
        img_urls = dataframe["imgs_src"]

        for url_li in img_urls:
            for url in url_li:
                # url =  url[2:]
                download(url=url, opt=opt)
