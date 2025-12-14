import json 

from config import settings
from app.db_handler import PostgreSQLHandler 



def load_json(file_name):
    videos, videos_snap = [], []

    with open(file_name, "r") as file:
        data = json.load(file)

        for video in data.get("videos"):
            
            for snapshot in video.get("snapshots"):
                videos_snap.append((snapshot))
            
            video = dict(video)

            if video.get("snapshots"):
                del video["snapshots"]
            videos.append(video)


    with PostgreSQLHandler(settings.DB_URI) as session:
        sql_exec = """
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
        session.insert_rows(sql_exec, params=videos)

    with PostgreSQLHandler(settings.DB_URI) as session:
        sql_exec = """
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

        session.insert_rows(sql_exec, params=videos_snap)



load_json("migration//videos.json")