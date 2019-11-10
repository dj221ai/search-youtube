import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from isodate import parse_duration


def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        search_param = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',

        }

        search_req = requests.get(search_url, params=search_param)
        s_results = search_req.json()['items']
        video_ids = []
        for result in s_results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'direct':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
        elif request.POST['submit'] is None:
            return HttpResponse("please type something")

        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        video_param = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(video_ids),
            'maxResults': 9,

        }

        vid_req = requests.get(video_url, params=video_param)
        v_results = vid_req.json()['items']

        for result in v_results:
            vid_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': parse_duration(result['contentDetails']['duration']).total_seconds() // 60,
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }
            videos.append(vid_data)

    context = {
        'videos': videos
    }

    return render(request, 'searcher/index.html', context)
