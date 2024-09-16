# This script is from the 2024 EP elections investigation into disinformation on YouTube. 
# This section specifically retrieves the transcripts of a list of YouTube videos as generated by closed captions.

# Note: not all videos on YouTube have auto-generated captions (the uploader can turn them off). This script accounts for this.

import pandas as pd
import os
from googleapiclient.discovery import build

PATH = "/content/drive/MyDrive/" #if using Google Collab

# Set up API details and access
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
api_key = "API key" #replace with the key retrieved from the Google developer page
youtube = build(api_service_name, api_version, developerKey=api_key)

# need to install this package to access the transcripts
pip install youtube-transcript-api
from youtube_transcript_api import YouTubeTranscriptApi

# DEFINE FUNCTIONS

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript
    except Exception as e:
        return f"Error: {str(e)}"

# Function to process the DataFrame and add transcript columns
def add_transcripts_to_dataframe(df):
    # Apply the function to fetch transcripts for both video columns
    df['Transcript1'] = df['Video1ID'].apply(get_youtube_transcript)
    df['Transcript2'] = df['Video2ID'].apply(get_youtube_transcript)
    return df

# LOAD DATASET AND RUN FUNCTIONS

if __name__ == "__main__":
    # Load the Excel file into a DataFrame
    df = pd.read_excel(PATH+'data.xlsx')

    # Add transcripts to the DataFrame
    df_with_transcripts = add_transcripts_to_dataframe(df)

    # Save the updated DataFrame back to an Excel file
    df_with_transcripts.to_excel('path_to_save_updated_file.xlsx', index=False)

    # Optional: Print the first few rows to verify
    print(df_with_transcripts.head())

