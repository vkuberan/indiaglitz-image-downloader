# A small scraper used to download images from IndiaGlitz site
# look out for <input type="hidden" name="qstring" id="qstring" value="lang=tamil&category=1&gid=3129439&cid=8859" />
from helper import *
import os
import glob
import time
import json


project_dirs = {
    'data': 'data',
    'img': 'images'
}

link_data = {}

create_related_dirs(project_dirs)

links = {
    'shivani-narayanan': 'https://www.indiaglitz.com/get_gallery_load_all.php?category=1&cid=8859&start=',
    # 'poonam-bajwa': 'https://www.indiaglitz.com/get_gallery_load_all.php?category=1&cid=4443&start=',
}

clear_screen()

for dirname, data_url in links.items():

    actress_dir = 'images/' + dirname
    actress_data_dir = 'images/' + dirname + '/data'
    actors_dir = {
        'Download Data':  actress_data_dir,
        'Download Images': actress_dir
    }

    # create separate directory for every actress
    create_related_dirs(actors_dir)

    start = 0
    cnt = 1
    load_more = True

    while load_more:
        local_data_file = dirname + '-' + str(cnt) + '.txt'
        data_file = '{}/{}'.format(actress_data_dir, local_data_file)
        fetch_url = '{}{}'.format(data_url, start)

        print_char_under_string(fetch_url, '-')
        print_char_under_string(data_file, '-')

        data = json.loads(fetch_data_from_url(fetch_url, data_file))

        iCnt = 1

        if 'imgSrvr' in data:
            if 'images' in data:
                for image in data['images']:
                    img_url = data['imgSrvr'] + image['image']
                    imagename = actress_dir + '/' + image['image']
                    print('{:>3d}] {}'.format(iCnt, img_url))
                    save_image_to_disk(img_url, imagename)
                    time.sleep(1)
                    iCnt += 1
        else:
            load_more = False

        cnt += 1
        start += 10

        time.sleep(3)
        # input("Press any key to continue...")
        clear_screen()

    print("Program finished.")
