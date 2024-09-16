#This script will demonstrate how to retrieve statistics about a single channel or group of channels, as well as the videos uploaded by that channel

import pandas
import seaborn
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

# Replace with your own API Key
api_key = 'API KEY'

# Make a list of the channels you want to analyse
# channel ids can be aquired via the url in the channel of interest, or through third party websites like:
# https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/

channel_ids = ['______',
               '______',
               '______',
              ]

youtube = build('youtube', 'v3', developerKey=api_key)

# FUNCTION FOR RETREIVING A SINGLE CHANNEL STATS

def get_1channel_stats(youtube, channel_id):
  Request = youtube.channels().list(
      part = 'snippet,contentDetails,statistics',
      id = channel_id)
  response = Request.execute()

  return response

# Run the function
channel_id = '_____'
get_1channel_stats(youtube, channel_id)

# FUNCTION TO GET MULTIPLE CHANNELS' STATISTICS

def get_channel_stats(youtube, channel_ids):

  all_data = []

  request = youtube.channels().list(
      part = 'snippet,contentDetails,statistics',
      id = ','.join(channel_ids))
  response = request.execute()

  for i in range(len(response['items'])):

     data = dict(Channel_name = response['items'][i]['snippet']['title'],
               views = response['items'][i]['statistics']['viewCount'],
               subscribers = response['items'][i]['statistics']['subscriberCount'],
               total_videos = response['items'][i]['statistics']['videoCount'],
                 playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
     all_data.append(data)


  return all_data

# Run the function, convert to dataframe
channel_statistics = get_channel_stats(youtube, channel_ids)
channel_data = pd.DataFrame(channel_statistics)
channel_data

channel_data['subscribers'] = pd.to_numeric(channel_data['subscribers'])
channel_data['views'] = pd.to_numeric(channel_data['views'])
channel_data['total_videos'] = pd.to_numeric(channel_data['total_videos'])
channel_data.dtypes


# OPTIONAL: VISUALISE DATA IN GRAPHS

sns.set(rc={'figure.figsize':(10,8)})
ax = sns.barplot(x='Channel_name', y='total_videos', data=channel_data)

# OPTIONAL: GET THE VIDEOS FROM A CHANNEL AND THEIR STATS

#access the playlist id for the particular channel
playlist_id = channel_data.loc[channel_data['Channel_name'] == '_____', 'playlist_id'].iloc[0]
playlist_id

#Fetch all the video ids for a particular channel
def get_video_ids(youtube, playlist_id):
  request = youtube.playlistItems().list(
      part = 'contentDetails',
      playlistId = playlist_id,
      maxResults = 50)
  response = request.execute()

  video_ids = []  #list to store video ids

  for i in range(len(response['items'])):
    video_ids.append(response['items'][i]['contentDetails']['videoId'])

  #need to paginate if there are more than 50 videos, this loop will make sure we get them all
  next_page_token = response.get('nextPageToken')
  more_pages = True

  while more_pages:
    if next_page_token is None:
      more_pages = False
    else:
        request = youtube.playlistItems().list(
            part = 'contentDetails',
            playlistId = playlist_id,
            maxResults = 50,
            pageToken = next_page_token)
        response = request.execute()

        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
  return video_ids


#put all the video ids in a list
video_ids = get_video_ids(youtube, playlist_id)
video_ids

# GET DETAILS ON EACH VIDEO

def get_video_details(youtube, video_ids):

  all_video_stats = []

  #limit of 50 videos per request via Youtube API
  for i in range(0, len(video_ids), 50):
    request = youtube.videos().list(
        part = 'snippet,statistics',
        id = ','.join(video_ids[i:i+50]))
    response = request.execute()

    #for each 50 videos, get all their info
    for video in response['items']:
      video_stats = dict(Title = video['snippet']['title'],
                        Published_date = video['snippet']['publishedAt'],
                        Views = video['statistics']['viewCount'],
                        Likes = video['statistics']['likeCount'],
                        Comments = video['statistics']['commentCount']
      )
      all_video_stats.append(video_stats)

  return all_video_stats


video_details = get_video_details(youtube, video_ids)
video_data = pd.DataFrame(video_details)

#make sure the numerical values are ints
video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
video_data['Comments'] = pd.to_numeric(video_data['Comments'])
video_data.dtypes

# OPTIONAL: RETREIVE AND VISUALISE TOP 10 VIDEOS

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)
top10_videos
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)

#sort data by most recent uploads
video_data['Month'] = pd.to_datetime(video_data['Published_date']).dt.strftime('%b')
video_data

videos_per_month = video_data.groupby('Month', as_index=False).size()
videos_per_month

sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
videos_per_month.index = pd.CategoricalIndex(videos_per_month['Month'], categories=sort_order, ordered=True)
videos_per_month = videos_per_month.sort_index()

ax2 = sns.barplot(x='Month', y='size', data=videos_per_month)
