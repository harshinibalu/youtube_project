import mysql.connector
import streamlit as st
from googleapiclient.discovery import build
import pprint

# %%
#API key connection

def Api_connect():
    Api_id ="AIzaSyBYj0dYy9Nt_Zds0rKzBBk9sNA5Pd8tOX8"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(api_service_name,api_version,developerKey=Api_id)

    return youtube

youtube_test = Api_connect()

 


# %%
#API key connection

def Api_connect():
    Api_id ="AIzaSyBYj0dYy9Nt_Zds0rKzBBk9sNA5Pd8tOX8"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(api_service_name,api_version,developerKey=Api_id)

    return youtube

youtube_test = Api_connect()

 


# %%
    #we need to create the upper code as function to execute for all the channels we are going to take in future

# This function fetches channel data from the YouTube API
def fetch_channel_info(channel_id):
    request = youtube_test.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()

    for i in response['items']:
        data = dict(Channel_Name=i['snippet']['title'],
                    Publish_Date=i['snippet']['publishedAt'],
                    Playlist_id=i['contentDetails']['relatedPlaylists']['uploads'],
                    sub_count=i['statistics']['subscriberCount'],
                    vid_count=i['statistics']['videoCount'])
    return data

        

# %%
#like this we can get other channel details also
channel_id ="UChGd9JY4yMegY6PxqpBjpRA"

channel_details=(channel_id)

# %%
channel_details 

# %%
#get video ids

#we need playlist id to get video ids

response = youtube_test.channels().list(id ="UChGd9JY4yMegY6PxqpBjpRA",
                                        part = 'ContentDetails').execute()

#Playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# %%
response

# %%
#get video ids

#we need playlist id to get video ids

videos_ids =[] #creating list for getting the ids

response = youtube_test.channels().list(id ="UChGd9JY4yMegY6PxqpBjpRA",
                                        part = 'ContentDetails').execute()

Playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

next_page_token = None

#snippet used for geting video ids
#part,playlistId etc are parameters of youtube api - u can refer from youtube api key reference
#while use for going to next token automatically for whole vds
while True:
    response1 = youtube_test.playlistItems().list(
                                            part ='snippet',
                                            playlistId = Playlist_id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
    #for getting 50 vds we are using for loop
    for i in range(len(response1['items'])):
        videos_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
    #get used for getting the remaining  eg 34 videos #values iruntha eduthu kudukum ilana none nu return panum
    next_page_token=response1.get('nextPageToken')

    if next_page_token is None:
      break




# %%
#get video ids

#creating function for all channels to get video id

def get_videos_ids(channel_id):
    videos_ids =[] #creating list for getting the ids

    response = youtube_test.channels().list(id =channel_id,
                                            part = 'ContentDetails').execute()

    Playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token = None

    #snippet used for geting video ids
    #part,playlistId etc are parameters of youtube api - u can refer from youtube api key reference
    #while use for going to next token automatically for whole vds
    while True:
        response1 = youtube_test.playlistItems().list(
                                                part ='snippet',
                                                playlistId = Playlist_id,
                                                maxResults=50,
                                                pageToken=next_page_token).execute()
        #for getting 50 vds we are using for loop
        for i in range(len(response1['items'])):
            videos_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        #get used for getting the remaining  eg 34 videos #values iruntha eduthu kudukum ilana none nu return panum
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
            break
    
    return videos_ids



# %%
#checking the function 

checking_video_ids = get_videos_ids("UChGd9JY4yMegY6PxqpBjpRA")

# %%
videos_ids

# %%
#get video information

    #we are creating the list so we get all the video details otherwise last vd detail only will show in the output
video_data = []
for checking_video_ids in videos_ids:
    request = youtube_test.videos().list(
        part ="snippet,ContentDetails,statistics",
        id = checking_video_ids
    ) 
    response = request.execute()

   #we are using get function  eg: comment is not there for that vd means it will show none instead of throwing the error
    for item in response['items']:
        #we want in json format so we are creating dict as follows so that we can impoprt easily in the mysql database
        data = dict(Channel_Name = item['snippet']['channelTitle'],
                    channel_id = item['snippet']['channelId'],
                    Video_Id =item['id'],
                    Title = item['snippet']['title'],
                    #Tags=item['snippet']['tags'],
                    Thumbnails = item['snippet']['thumbnails'],
                    Description = item['snippet']['description'],
                    Published_Date = item['snippet']['publishedAt'],
                    Duration = item['contentDetails']['duration'],
                   Views = item.get('viewCount'),
                    Likes = item.get('likeCount'),
                    Favourite_Count = item.get('favoriteCount'),
                    Comments = item.get('commentCount'),
                    Definition = item['contentDetails']['definition'],
                    Caption_Status = item['contentDetails']['caption'])
        video_data.append(data)

# 

# %%
#creating as function --get video information

    #we are creating the list so we get all the video details otherwise last vd detail only will show in the output
def get_video_info(Videos_Ids):
    video_data = []
    for checking_video_ids in Videos_Ids:
        request = youtube_test.videos().list(
            part ="snippet,ContentDetails,statistics",
            id = checking_video_ids
        ) 
        response = request.execute()

    #we are using get function  eg: comment is not there for that vd means it will show none instead of throwing the error
        for item in response['items']:
            statistics = item.get('statistics', {})
            snippet = item.get('snippet', {})
            content = item.get('contentDetails', {})
            #we want in json format so we are creating dict as follows so that we can impoprt easily in the mysql database
             
            data = {
                "channel_name": snippet.get("channelTitle"),
                "video_id": item.get("id"),
                "title": snippet.get("title"),
                "published_date": snippet.get("publishedAt"),
                "duration": content.get("duration"),
                "views": int(statistics.get("viewCount", 0)),
                "likes": int(statistics.get("likeCount", 0)),
                "comments": int(statistics.get("commentCount", 0))
            }
            video_data.append(data)
    return video_data

# %%
video_details = get_video_info(videos_ids)

# %%
video_details

# %%
#get comment information


def get_comment_info(Video_Ids): #nama vekara name this video id name
    comment_data = []
    try:
        for video_id in Video_Ids:
            request = youtube_test.commentThreads().list(
                    part = 'snippet',
                    videoId = video_id,
                    maxResults = 50
                )
            response = request.execute()

            for item in response['items']:
                data = dict(
                    Comment_Id = item['snippet']['topLevelComment']['id'],
                    Video_Id = item['snippet']['videoId'],
                    Comment_Text = item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    Comment_Author = item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    Comment_Published = item['snippet']['topLevelComment']['snippet']['publishedAt'])
                comment_data.append(data)
    except:
     pass
    return comment_data


  

# %%
comment_detail = get_comment_info(videos_ids)


# %%
#get playlist videos

def get_playlist_info(channel_id):

        next_page_token = None
        Playlist_Data = []
        while True:
                request = youtube_test.playlists().list(
                    part = 'snippet,contentDetails',
                    channelId = channel_id,
                    maxResults = 50,
                    pageToken = next_page_token

                )

                response = request.execute()

                for item in response['items']:
                    data = dict(Playlist_Id = item['id'],
                                Title = item['snippet']['title'],
                                Channel_Id = item['snippet']['channelId'],
                                Published_At = item['snippet']['publishedAt'],
                                Videos_Count = item['contentDetails']['itemCount']
                                )
                    Playlist_Data.append(data)

                next_page_token = response.get('nextPageToken')
                if next_page_token is None:
                    break
        return Playlist_Data

# %%
playlist_details = get_playlist_info('UChGd9JY4yMegY6PxqpBjpRA')

# %%
playlist_details

# %%
response

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 database ='youtube_project'

 )

cursor = mydb.cursor() #cursor is to run python in sql command
mydb.commit() # Commit is to execute the command written for SQL and run via python

# %%
#DROP TABLE IF EXISTS channel_info;


# %%
cursor.execute('''create table if not exists channel_info(Channel_Name VARCHAR(225),
                                                            Publish_Date VARCHAR(225),
                                                            Playlist_id VARCHAR(225),
                                                            sub_count VARCHAR(225),
                                                            vid_count VARCHAR(225))''')
mydb.commit()
 
 
cursor.execute('''create table if not exists video_ids(video_id VARCHAR(150))''')
mydb.commit()
 
 
cursor.execute(''' CREATE TABLE if not exists video_detail (channel_name     VARCHAR(255),
                                                           video_id         VARCHAR(50) PRIMARY KEY,
                                                            title            TEXT,
                                                            published_date   DATETIME,
                                                            duration         VARCHAR(20),
                                                            views            INT,
                                                            likes            INT,
                                                            comments         INT)''')
mydb.commit()
 
 
cursor.execute('''create table if not exists comment_detail(comment_Text text,
                                                            comment_Author VARCHAR(225),
                                                            comment_Published VARCHAR(225),
                                                            video_id VARCHAR(225))''')
mydb.commit()

# %%
def get_channel_info(channel_id):
    channel_data = fetch_channel_info(channel_id)  # ✅ Now calling the correct function
    cursor = mydb.cursor()

    sql_ch = '''INSERT INTO channel_info(Channel_Name ,
                                         Publish_at,
                                         Playlist_id ,
                                         sub_count ,
                                         vid_count) VALUES (%s,%s,%s,%s,%s)'''
    val_ch = tuple(channel_data.values())
    cursor.execute(sql_ch, val_ch)
    mydb.commit()


# %%
get_channel_info(channel_id)

# %%
def comment_tables():
    comment_detail = get_comment_info(videos_ids)
    cursor = mydb.cursor()

    sql_co = '''INSERT INTO comment_detail(Comment_Text,
                                           Comment_Author,
                                           Comment_Published,
                                           Video_Id) VALUES (%s,%s,%s,%s)'''

    for comment in comment_detail:
        val = (
            comment['Comment_Text'],
            comment['Comment_Author'],
            comment['Comment_Published'],
            comment['Video_Id']
        )
        cursor.execute(sql_co, val)

    mydb.commit()
    return comment_detail


# %%
comment_tables()

# %%
# for row in video_details:
#     print(type(row), row)
#     assert isinstance(row, tuple), "Each row must be a tuple"


# %%
# def video_tables(channel_id):
#     video_ids = get_videos_ids(channel_id)
#     video_data = get_video_info(video_ids)

#     # Ensure all entries are tuples
#     vid_detail = [tuple(i.values()) for i in video_data]

#     cursor = mydb.cursor()

#     sql_vi = '''INSERT INTO video_detail(channel_name,
#                                          video_id,
#                                          title,
#                                          published_date,
#                                          duration,
#                                          views,
#                                          likes,
#                                          commments) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''

#     cursor.executemany(sql_vi, vid_detail)
#     mydb.commit()
#     return video_data



# %%


def video_tables(channel_id):
    video_ids = get_videos_ids(channel_id)
    video_data = get_video_info(video_ids)

    vid_detail = []
    for i in video_data:
        vid_detail.append((
            i.get("channel_name"),
            i.get("video_id"),
            i.get("title"),
            i.get("published_date"),
            i.get("duration"),
            i.get("views"),
            i.get("likes"),
            i.get("comments")
        ))

    # DEBUG PRINT
    for row in vid_detail:
        print("Inserting row:", row)

    cursor = mydb.cursor()
    sql_vi = '''INSERT INTO video_detail(channel_name,
                                         video_id,
                                         title,
                                         published_date,
                                         duration,
                                         views,
                                         likes,
                                         comments)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.executemany(sql_vi, vid_detail)
    mydb.commit()
    return video_data


# %%
import pprint

# %%
video_tables(channel_id)


# %%
st.write("Hello World")

# %%
channel_id=str(st.text_input("ENTER CHANNEL ID👉: "))
options = ['select option','show channel details','show video details','show comments']
with st.sidebar:
  selected = st.selectbox("Select table to show", options=options)
 
if selected==options[0]:
    None
 
if selected==options[1]:
    data=channel_table(channel_id)
    st.dataframe(data)
 
if selected==options[2]:
    data=video_tables(channel_id)
    st.dataframe(data)    
 
if selected==options[3]:
    data=comment_tables()
    st.dataframe(data)
