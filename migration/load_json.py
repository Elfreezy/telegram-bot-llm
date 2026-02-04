import os
import json 

from config import settings
from app.db_handler import PostgreSQLHandler 

file_name = "videos.json"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)

def load_json(file_path: str):
    videos, videos_snap = [], []

    with open(file_path, "r") as file:
        data = json.load(file)

        for video in data.get("videos"):
            for snapshot in video.get("snapshots"):
                videos_snap.append((snapshot))
            
            video = dict(video)

            if video.get("snapshots"):
                del video["snapshots"]
            videos.append(video)


    with PostgreSQLHandler(settings.DB_URI) as session:
        sql_create_tables = """
            CREATE TABLE videos (
                id VARCHAR(36) primary key,
                creator_id VARCHAR(32),
                video_created_at TIMESTAMP,
                views_count INT,
                likes_count INT,
                comments_count INT,
                reports_count INT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            );


            CREATE TABLE video_snapshots (
                id VARCHAR(32) PRIMARY KEY,
                video_id VARCHAR(36),
                views_count INT,
                likes_count INT,
                comments_count INT,
                reports_count INT,
                delta_views_count INT,
                delta_likes_count INT,
                delta_comments_count INT,
                delta_reports_count INT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            );
        """
        session.init_tables(sql_create_tables)

        sql_insert_videos = """
            INSERT INTO videos (id, 
                        creator_id,
                        video_created_at, 
                        views_count,
                        likes_count,
                        comments_count,
                        reports_count, 
                        created_at,
                        updated_at)
            VALUES (%(id)s,
                    %(creator_id)s,
                    %(video_created_at)s,
                    %(views_count)s,
                    %(likes_count)s,
                    %(comments_count)s,
                    %(reports_count)s,
                    %(created_at)s,
                    %(updated_at)s)
        """
        session.insert_rows(sql_insert_videos, params=videos)

        sql_insert_video_snapshots = """
            INSERT INTO video_snapshots (id, 
                        video_id,
                        views_count, 
                        likes_count,
                        reports_count,
                        comments_count,
                        delta_views_count, 
                        delta_likes_count,
                        delta_comments_count,
                        delta_reports_count,
                        created_at,
                        updated_at)
            VALUES (%(id)s,
                    %(video_id)s,
                    %(views_count)s,
                    %(likes_count)s,
                    %(reports_count)s,
                    %(comments_count)s,
                    %(delta_views_count)s,
                    %(delta_likes_count)s,
                    %(delta_comments_count)s,
                    %(delta_reports_count)s,
                    %(created_at)s,
                    %(updated_at)s)
        """

        session.insert_rows(sql_insert_video_snapshots, params=videos_snap)



load_json(file_path)