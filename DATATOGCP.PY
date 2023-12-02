import pandas as pd
from googleapiclient.discovery import build
from pandas_gbq import to_gbq  



API_KEY = ""
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

PROJECT_ID = ""
DATASET_ID = ""
TABLE_ID = ""


video_ids = ["MWL8rtquLAE", "yVJ5Qt5tGvE", "zq-way2eZ1c"]


def fetch_comments(video_id):
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

    comments_data = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=10000,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            comments_data.append({
                "VideoID": video_id,
                "CommentID": item["id"],
                "Author": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "Comments": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                "PublishedAt": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                "LikeCount": item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments_data


while True:
    all_comments_data = []

    for video_id in video_ids:
        comments_data = fetch_comments(video_id)
        all_comments_data.extend(comments_data)

   
    all_comments_df = pd.DataFrame(all_comments_data)
   
    to_gbq(all_comments_df, f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", if_exists='replace')
   
    print(f"All comments saved to BigQuery table {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")


  