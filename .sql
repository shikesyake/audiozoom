DROP TABLE IF EXISTS `jobs`;
CREATE TABLE `jobs` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `job_name` varchar(10) DEFAULT NULL,
  `vitality` int(11) DEFAULT NULL,
  `strength` int(11) DEFAULT NULL,
  `agility` int(11) DEFAULT NULL,
  `intelligence` int(11) DEFAULT NULL,
  `luck` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `jobs` (`id`, `job_name`, `vitality`, `strength`, `agility`, `intelligence`, `luck`) VALUES
(1, 'admin', 1, 1, 4, 4, 3),
(2, '', 3, 3, 8, 5, 7),
(3, '視聴者', 5, 5, 7, 5, 4),
(4, '魔法使い', 3, 2, 6, 8, 6),
(5, '僧侶', 5, 5, 3, 7, 5),
(6, '勇者', 10, 10, 10, 10, 10),
(7, '忍者', 3, 3, 8, 5, 10);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (`id`, `name`, `level`, `job_id`) VALUES
(1, 'python', 12, 6),
(2, 'ケン', 7, 2),
(3, 'リン', 1, 1),
(4, 'ユウ', 3, 3),
(5, 'クレア', 10, 4),
(6, 'ショウ', 5, 2),
(7, 'さくら', 7, 1),
(8, 'ジャック', 5, 4),
(9, 'ロック', 12, 6),
(10, 'じゅん', 1, NULL);




-- 配信サーバー管理テーブル（クライアント側）
CREATE TABLE `broadcast_servers` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `server_name` varchar(100) NOT NULL COMMENT '配信サーバー名',
  `server_address` varchar(255) NOT NULL UNIQUE COMMENT '配信サーバーのアドレス（例：http://192.168.1.100）',
  `base_path` varchar(255) DEFAULT '/live' COMMENT 'メディア保存のベースパス',
  `description` text DEFAULT NULL COMMENT '説明',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '有効フラグ',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配信サーバー管理テーブル';

-- 配信チャンネル/ストリーム管理テーブル
CREATE TABLE `broadcast_streams` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `server_id` int(11) NOT NULL COMMENT '配信サーバーID',
  `stream_name` varchar(100) NOT NULL COMMENT '配信名（チャンネル名）',
  `stream_id` varchar(50) NOT NULL COMMENT 'ストリームID（フォルダ名等）',
  `description` text DEFAULT NULL COMMENT '説明',
  `thumbnail_url` varchar(512) DEFAULT NULL COMMENT 'サムネイルURL',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '有効フラグ',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  UNIQUE KEY `unique_stream` (`server_id`, `stream_id`),
  FOREIGN KEY (`server_id`) REFERENCES `broadcast_servers`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配信チャンネル・ストリーム管理テーブル';

-- 配信メディアファイル管理テーブル
CREATE TABLE `broadcast_media` (
  `id` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `stream_id` int(11) NOT NULL COMMENT '配信ストリームID',
  `media_name` varchar(255) NOT NULL COMMENT 'メディアファイル名',
  `media_type` enum('video', 'audio', 'hls') NOT NULL COMMENT 'メディアタイプ',
  `relative_path` varchar(512) NOT NULL COMMENT '配信サーバーの/live からの相対パス',
  `file_format` varchar(50) DEFAULT NULL COMMENT 'ファイル形式（mp4, m3u8等）',
  `is_live` tinyint(1) DEFAULT 0 COMMENT 'ライブストリーム配信フラグ',
  `is_active` tinyint(1) DEFAULT 1 COMMENT '有効フラグ',
  `description` text DEFAULT NULL COMMENT '説明',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  FOREIGN KEY (`stream_id`) REFERENCES `broadcast_streams`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配信メディアファイル管理テーブル';

-- 配信サーバーのサンプルデータ
INSERT INTO `broadcast_servers` (`id`, `server_name`, `server_address`, `base_path`, `description`, `is_active`) VALUES
(1, 'メインサーバー', 'http://192.168.1.100', '/live', 'メイン配信サーバー', 1),
(2, 'サブサーバー', 'http://192.168.1.101', '/live', 'サブ配信サーバー', 1),
(3, 'テストサーバー', 'http://localhost:8080', '/live', 'ローカルテストサーバー', 1);

-- 配信チャンネルのサンプルデータ
INSERT INTO `broadcast_streams` (`id`, `server_id`, `stream_name`, `stream_id`, `description`, `is_active`) VALUES
(1, 1, 'ライブカメラ1', 'camera1', 'オフィスの監視カメラ', 1),
(2, 1, 'ライブカメラ2', 'camera2', 'エントランスの監視カメラ', 1),
(3, 1, 'オーディオストリーム1', 'audio_stream1', 'スタジオのマイク入力', 1),
(4, 2, 'イベント配信', 'event_conference', 'イベント配信用チャンネル', 1),
(5, 3, 'テスト配信', 'test_stream', 'テスト用配信', 1);

-- 配信メディアのサンプルデータ
INSERT INTO `broadcast_media` (`id`, `stream_id`, `media_name`, `media_type`, `relative_path`, `file_format`, `is_live`, `is_active`) VALUES
(1, 1, 'カメラ1ライブ', 'hls', 'camera1/stream.m3u8', 'm3u8', 1, 1),
(2, 1, 'カメラ1録画', 'video', 'camera1/recorded/20260203_001.mp4', 'mp4', 0, 1),
(3, 2, 'カメラ2ライブ', 'hls', 'camera2/stream.m3u8', 'm3u8', 1, 1),
(4, 3, 'オーディオライブ', 'hls', 'audio_stream1/audio.m3u8', 'm3u8', 1, 1),
(5, 4, 'イベント配信HLS', 'hls', 'event_conference/stream.m3u8', 'm3u8', 1, 1),
(6, 5, 'テスト動画', 'video', 'test_stream/sample.mp4', 'mp4', 0, 1);