from googleapiclient.discovery import build
import re
import os
from datetime import timedelta

api_key = 'AIzaSyBT7bZphu0H5ngPAksDz157w0TLinlcPvc'

youtube = build('youtube', 'v3', developerKey=api_key )
#pylint: disable=maybe-no-member
request = youtube.channels().list(
    #pylint: disable=maybe-no-member
    part='contentDetails,statistics',
    forUsername='sadhguru'
)
response = request.execute()
#print(response)

pl_request = youtube.playlists().list(
    part='contentDetails, snippet',
    channelId="UCcYzLCs3zrQIBVHYA1sK2sw"
)

pl_response = pl_request.execute()
#print(pl_response)

#for items in pl_response['items']:
    #print(items)
    #print()

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

totalSeconds = 0
nextPagetoken=None
while True:
    plitem_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId='PL3uDtbb3OvDNjBOVcje1UjX0X7ubGSMuR',
        maxResults = 50,
        pageToken=nextPagetoken
    )

    plitem_response = plitem_request.execute()
    #print(plitem_response)
    
    vid_id=[]
    for items in plitem_response['items']:
        vid_id.append(items['contentDetails']['videoId'])
        
    #print(','.join(vid_id))


    vid_requests = youtube.videos().list(
        part = 'contentDetails',
        id = ','.join(vid_id)
    )

    vid_response = vid_requests.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']
        #print(duration)

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        #print(hours, minutes, seconds)


        video_second = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()    
        
        #print(video_second)
        totalSeconds += video_second
    
    nextPagetoken = plitem_response.get('nextPagetoken')
    if not nextPagetoken:
        break

totalSeconds = int(totalSeconds)

minutes, seconds = divmod(totalSeconds, 60)
hours, minutes = divmod(minutes, 60)
print(f'{hours}:{minutes}:{seconds}')



