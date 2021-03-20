from helper import *
import os
import glob
import time
import json

project_dirs = {
    'data': 'data',
    'img': 'images'
}

create_related_dirs(project_dirs)

food_for_bot = {
    'actors': 'https://www.indiaglitz.com/actor-photos',
    'actress': 'https://www.indiaglitz.com/actress-photos'
}

for key, url_link in food_for_bot.items():
    dir_name = 'data/' + key
    file_name = dir_name + '/' + key + '.html'
    data_dir = {
        key: dir_name
    }

    # create separate directory for every actress
    create_related_dirs(data_dir)

    data = fetch_data_from_url(url_link, file_name)

    list_of_url_links = get_list_of_url_links(data)

    input("Press any key to continue...")
