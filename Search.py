# This script is from an August 2024 DD research project into disinformation on YouTube in the leadup to the EP elections.
# In in, we performed a series of keyword-search queries to the YouTube API, appending a list with the videos returned from the API after each request.
# This query was also limited to videos uploaded within a specific time frame and queried from a specific country region.

# IMPORT PACKAGES

import pandas as pd
import os
from googleapiclient.discovery import build

#Create a dataframe that will be appended with the necessary information of each video returned by each query
all_videos_df = pd.DataFrame(columns=["Title", "Published At", "Channel", "Description", "Video ID", "Video URL"])


#DEFINE SEARCH FUNCTION

def fetch_videos(query, published_after, published_before):
    global all_videos_df

    # Set up API details
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyAxa45p95rs9b8rR1JZpTfV6W9kfggSSGE"
    #"AIzaSyBbFjui_l3LQSYs-60so4VFZ2aryX-E7Jo" #"AIzaSyAxa45p95rs9b8rR1JZpTfV6W9kfggSSGE" AIzaSyDfTTNMiXIW1nrPkX2SOFNgpPDdQqHsW2E

    youtube = build(api_service_name, api_version, developerKey=api_key)

    max_results_per_page = 50
    region_code = "DE"
    next_page_token = None

    while True:
        # Make the API request
        request = youtube.search().list(
            part="snippet",
            channelType="any",
            eventType="none",
            maxResults=max_results_per_page,
            order="viewCount",
            publishedAfter=published_after,
            publishedBefore=published_before,
            q=query,
            pageToken=next_page_token,
            regionCode=region_code  # Uncomment and set if needed
        )
        response = request.execute()

        # Extract video information and create a temporary DataFrame
        video_data = [
            {
                "Title": item['snippet']['title'],
                "Published At": item['snippet']['publishedAt'],
                "Channel": item['snippet']['channelTitle'],
                "Description": item['snippet']['description'],
                "Video ID": item['id']['videoId'],
                "Video URL": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in response['items']
        ]

        temp_df = pd.DataFrame(video_data)

        # Concatenate the temporary DataFrame with the main one
        all_videos_df = pd.concat([all_videos_df, temp_df], ignore_index=True)

        # Check if there is another page of results
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

# RUN THE FUNCTION

if __name__ == "__main__":
    # Example: Fetch videos with a specific query, adjust as needed
    fetch_videos("Europe immigration exposed", "2024-04-01T00:00:00Z", "2024-06-30T00:00:00Z")

# Drop all instances of the same videos being returned
df_cleaned = all_videos_df.drop_duplicates(subset=['Video ID'])

# Display data frame
all_videos_df
