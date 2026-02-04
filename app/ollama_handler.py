import requests

from config import settings


class OllamaHelper:
    def __init__(self, url):
        self.url = url

    def get_response(self, text: str):
        payload = self.generate_payload(text)
        response = requests.post(self.url, json=payload)
        return response

    def get_sql(self, text: str):
        response = self.get_response(text)
        result = response.json()
        return str(result["response"]).replace("sql", "").replace("`", "")

    def generate_payload(self, text: str) -> dict:
        payload = {
            "model": "qwen2.5:7b",
            "prompt": f"""
                ### Task
                Ты эксперт по SQL. Сгенерируй точный и оптимизированный SQL-запрос, который решит задачу {text}.
                Ответ должен содержать только SQL код без объяснений.

                ### Database Schema
                CREATE TABLE videos (
                    id VARCHAR(36) primary key,     // идентификатор видео
                    creator_id VARCHAR(32),         // идентификатор креатора (автора)
                    video_created_at TIMESTAMP,     // дата и время публикации видео
                    views_count INT,                // финальное количество просмотров
                    likes_count INT,                // финальное количество лайков
                    comments_count INT,             // финальное количество комментариев
                    reports_count INT,              // финальное количество жалоб
                    created_at TIMESTAMP,           // дата и время создания
                    updated_at TIMESTAMP            // дата и время обновления
                );


                CREATE TABLE video_snapshots (
                    id VARCHAR(32) PRIMARY KEY,     // идентификатор снапшота
                    video_id VARCHAR(36),           // ссылка на соответствующее видео
                    views_count INT,                // текущие значения просмотров
                    likes_count INT,                // текущие значения лайков
                    comments_count INT,             // текущие значения комментариев
                    reports_count INT,              // текущие значения жалоб
                    delta_views_count INT,          // приращение значения просмотров (насколько изменилось значение с прошлого замера)
                    delta_likes_count INT,          // приращение значения лайков (насколько изменилось значение с прошлого замера)
                    delta_comments_count INT,       // приращение значения комментариев (насколько изменилось значение с прошлого замера)
                    delta_reports_count INT,        // приращение значения жалоб (насколько изменилось значение с прошлого замера)
                    created_at TIMESTAMP,           // дата и время создания (насколько изменилось значение с прошлого замера)
                    updated_at TIMESTAMP            // дата и время обновления (насколько изменилось значение с прошлого замера)
                );

                ### Table Relationship
                videos.id -> video_snapshots.video_id

                ### Table Rules (ОБЯЗАТЕЛЬНО СЛЕДОВАТЬ)
                - Alias у таблицы videos -> v, у таблицы video_snapshots -> vs.
                - Таблица videos содержит статистику по каждому видео (просмотры, лайки, комментарии). 
                - Таблица video_snapshots содержит почасовые «снапшоты» статистики по каждому видео. 
                - Прирост (просмотры, лайки, комментарии, жалобы) основывается на таблице video_snapshots + столбцы delta_<название столбца>.
                - Динамика изменений основывается на таблице video_snapshots + столбцы delta_<название столбца>.
                - Если необходимо оценить итоговые количественные параметры используй таблицу videos.

                ### Requirements
                - Используй JOIN только где нужно.
                - Добавь WHERE для фильтров.
                - Если информации хватает в одной таблице, не используй JOIN.
                - Группируй и агрегируй данные правильно (GROUP BY, HAVING).
                - Если при сравнении дат важна только дата, не учитывай время (DATE).
                - В ответе ожидается одно число.

                ### SQL Examples
                Запрос: "Сколько видео у креатора с id <user_id> набрали больше 10 000 просмотров по итоговой статистике?"
                SQL: SELECT COUNT(*) FROM videos v WHERE v.creator_id = '<user_id>' AND v.views_count > 10000
				
				Запрос: "Сколько разных видео получали новые просмотры <date>?"
                SQL: SELECT COUNT(DISTINCT v.id) FROM videos v JOIN video_snapshots vs ON v.id = vs.video_id WHERE DATE(vs.created_at) = '<date>' and vs.delta_views_count > 0

                """,
            "stream": False,
            "temperature": 0.1,
            "top_p": 0.9,
        }
        return payload

ollama_helper = OllamaHelper(settings.LLM_URI)
