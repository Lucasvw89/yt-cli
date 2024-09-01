import requests, re, json
from bs4 import BeautifulSoup

import easy_dict as ed
import TUI


# dict_keys(['videoRenderer'])
# dict_keys(['playlistRenderer'])
# dict_keys(['shelfRenderer'])


# define complex keys for easy access
# search_results_list_key gets a python list of every result, videos, shorts, playlists
search_results_list_key = ['contents', 'twoColumnSearchResultsRenderer', 'primaryContents', 'sectionListRenderer', 'contents', 0, 'itemSectionRenderer', 'contents']

video_data_key = 'videoRenderer'

video_ID_key = ['videoId']
title_key = ['title', 'runs', 0, 'text']

video_thumbnail_url_key = ['thumbnail', 'thumbnails', 0, 'url']
video_thumbnail_width_key = ['thumbnail', 'thumbnails', 0, 'width']
video_thumbnail_height_key = ['thumbnail', 'thumbnails', 0, 'height']

duration_key = ['lengthText', 'simpleText']
num_views_key = ['viewCountText', 'simpleText']

creator_name_key = ['longBylineText', 'runs', 0, 'text']
creator_image_key = ['channelThumbnailSupportedRenderers', 'channelThumbnailWithLinkRenderer', 'thumbnail', 'thumbnails', 0, 'url']
creator_image_width_key = ['channelThumbnailSupportedRenderers', 'channelThumbnailWithLinkRenderer', 'thumbnail', 'thumbnails', 0, 'width']
creator_image_height_key = ['channelThumbnailSupportedRenderers', 'channelThumbnailWithLinkRenderer', 'thumbnail', 'thumbnails', 0, 'height']


def get_info(video):
    if 'videoRenderer' in video.keys():
        video_data = video[video_data_key]

        video_ID = ed.get_data_from(video_data, video_ID_key)
        title = ed.get_data_from(video_data, title_key)

        video_thumbnail_url = ed.get_data_from(video_data, video_thumbnail_url_key)
        video_thumbnail_width = ed.get_data_from(video_data, video_thumbnail_width_key)
        video_thumbnail_height = ed.get_data_from(video_data, video_thumbnail_height_key)

        duration = ed.get_data_from(video_data, duration_key)
        num_views = ed.get_data_from(video_data, num_views_key)
        num_views = num_views.split()[0]

        creator_name = ed.get_data_from(video_data, creator_name_key)
        creator_image = ed.get_data_from(video_data, creator_image_key)
        creator_image_width = ed.get_data_from(video_data, creator_image_width_key)
        creator_image_height = ed.get_data_from(video_data, creator_image_height_key)

        return {
            "creator": creator_name,
            "duration": duration,
            "views": num_views,
            "title": title,
            "ID": video_ID
        }



if __name__ == "__main__":

    busca = TUI.prompt_user()
    search_url = f'https://www.youtube.com/results?search_query={busca}'

    r = requests.get(search_url)    # receive youtube search
    soup = BeautifulSoup(r.text, 'html.parser') # parse HTML

    # search for data JSON
    ytInitialData = soup.find(string=re.compile('ytInitialData'))

    # get JSON string
    ytInitialData = str(ytInitialData).removeprefix("var ytInitialData = ")
    ytInitialData = ytInitialData[:-1]    # [:-1] removes ';' at the end

    # make it a python dict
    ytInitialData = json.loads(ytInitialData)

    video_list = []
    for video in ed.get_data_from(ytInitialData, search_results_list_key):
        video_list.append(get_info(video))

    video_list = [v for v in video_list if v]   # remove None
    prompt_list = ["Quit"] + [f"{video['creator']} - {video['duration']} - {video['views']} - {video['title']}" for video in video_list]

    TUI.app(video_list, prompt_list)
