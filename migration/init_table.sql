--- Создание таблиц ---

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