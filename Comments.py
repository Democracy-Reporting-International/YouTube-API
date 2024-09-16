# This script was used in the 2024 DD investigation into disinformation on YouTube during the EP elections.
# Specifically, this section retrieves the top 100 comments from a specific video. This script can be easily modified to repeat this process for each video ID in a list.

# DEFINE FUNCTIONS

def get_video_comments(video_id, api_key):
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Request to get the comments on a video
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,  # Adjust this value to fetch more comments per page
        textFormat="plainText"
    )

    # Execute the request and fetch the response
    response = request.execute()

    comments = []

    # Extract the comments and statistics
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'like_count': comment['likeCount'],
                'published_at': comment['publishedAt']
            })

        # Check if there are more pages of comments
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                pageToken=response['nextPageToken']
            ).execute()
        else:
            break
          
# RUN FUNCTIONS

  if __name__ == "__main__":
    # Replace with your actual API key and video ID
    api_key = "AIzaSyDfTTNMiXIW1nrPkX2SOFNgpPDdQqHsW2E"
    video_id = "x48oGp8FmhY"

    # Get comments in a DataFrame
    df_comments = get_video_comments(video_id, api_key)

    # Display the first few rows of the DataFrame
    print(df_comments.head())

    # Convert the list of comments to a DataFrame
    df_comments = pd.DataFrame(comments)

    return df_comments
