-- MySQL dump 10.13  Distrib 9.5.0, for macos26.1 (arm64)
--
-- Host: localhost    Database: user
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'e6a0ed3e-cf1c-11f0-ae85-3015d8fc6813:1-56';

--
-- Table structure for table `broadcast_media`
--

DROP TABLE IF EXISTS `broadcast_media`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `broadcast_media` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stream_id` int DEFAULT NULL,
  `media_name` varchar(255) NOT NULL COMMENT 'メディアファイル名',
  `server_address` varchar(255) DEFAULT NULL COMMENT 'サーバーIPアドレス/URL',
  `media_type` enum('video','audio','hls') NOT NULL COMMENT 'メディアタイプ',
  `relative_path` varchar(512) NOT NULL COMMENT '配信サーバーの/live からの相対パス',
  `file_format` varchar(50) DEFAULT NULL COMMENT 'ファイル形式（mp4, m3u8等）',
  `is_live` tinyint(1) DEFAULT '0' COMMENT 'ライブストリーム配信フラグ',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '有効フラグ',
  `description` text COMMENT '説明',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`id`),
  KEY `stream_id` (`stream_id`),
  CONSTRAINT `broadcast_media_ibfk_1` FOREIGN KEY (`stream_id`) REFERENCES `broadcast_streams` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配信メディアファイル管理テーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `broadcast_media`
--

LOCK TABLES `broadcast_media` WRITE;
/*!40000 ALTER TABLE `broadcast_media` DISABLE KEYS */;
INSERT INTO `broadcast_media` VALUES (1,1,'カメラ1ライブ',NULL,'hls','video/stream.m3u8','m3u8',1,1,NULL,'2026-02-05 06:47:34','2026-02-05 08:59:46'),(2,1,'カメラ1録画',NULL,'video','camera1/recorded/20260203_001.mp4','mp4',0,1,NULL,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(3,2,'カメラ2ライブ',NULL,'hls','camera2/stream.m3u8','m3u8',1,1,NULL,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(4,3,'オーディオライブ',NULL,'hls','audio_stream1/audio.m3u8','m3u8',1,1,NULL,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(5,4,'イベント配信HLS',NULL,'hls','event_conference/stream.m3u8','m3u8',1,1,NULL,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(6,5,'テスト動画',NULL,'video','test_stream/sample.mp4','mp4',0,1,NULL,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(7,NULL,'14.514.1919.81 - /live/stram.m3u8',NULL,'hls','/live/stram.m3u8','hls',0,1,NULL,'2026-02-05 07:41:19','2026-02-05 07:41:19'),(8,NULL,'114.514.1919.810 - /live/stream.m3u8 aaaa',NULL,'hls','/live/stream.m3u8','hls',0,1,NULL,'2026-02-05 07:46:13','2026-02-05 08:32:18'),(10,NULL,'114.514.1919.810 - /live/stream.m3u8',NULL,'hls','/live/stream.m3u8','hls',0,1,NULL,'2026-02-05 08:51:59','2026-02-05 08:51:59'),(11,NULL,'0.0.0.0:8080','0.0.0.0','hls','/live/stream.m3u8','hls',0,1,NULL,'2026-02-05 08:52:04','2026-02-05 09:05:31');
/*!40000 ALTER TABLE `broadcast_media` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `broadcast_servers`
--

DROP TABLE IF EXISTS `broadcast_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `broadcast_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `server_name` varchar(100) NOT NULL COMMENT '配信サーバー名',
  `server_address` varchar(255) NOT NULL COMMENT '配信サーバーのアドレス（例：http://192.168.1.100）',
  `base_path` varchar(255) DEFAULT '/live' COMMENT 'メディア保存のベースパス',
  `description` text COMMENT '説明',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '有効フラグ',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`id`),
  UNIQUE KEY `server_address` (`server_address`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配信サーバー管理テーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `broadcast_servers`
--

LOCK TABLES `broadcast_servers` WRITE;
/*!40000 ALTER TABLE `broadcast_servers` DISABLE KEYS */;
INSERT INTO `broadcast_servers` VALUES (1,'メインサーバー','http://192.168.1.100','/live','メイン配信サーバー',1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(2,'サブサーバー','http://192.168.1.101','/live','サブ配信サーバー',1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(3,'テストサーバー','http://localhost:8080','/live','ローカルテストサーバー',1,'2026-02-05 06:47:34','2026-02-05 06:47:34');
/*!40000 ALTER TABLE `broadcast_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `broadcast_streams`
--

DROP TABLE IF EXISTS `broadcast_streams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `broadcast_streams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `server_id` int NOT NULL COMMENT '配信サーバーID',
  `stream_name` varchar(100) NOT NULL COMMENT '配信名（チャンネル名）',
  `stream_id` varchar(50) NOT NULL COMMENT 'ストリームID（フォルダ名等）',
  `description` text COMMENT '説明',
  `thumbnail_url` varchar(512) DEFAULT NULL COMMENT 'サムネイルURL',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '有効フラグ',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_stream` (`server_id`,`stream_id`),
  CONSTRAINT `broadcast_streams_ibfk_1` FOREIGN KEY (`server_id`) REFERENCES `broadcast_servers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配信チャンネル・ストリーム管理テーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `broadcast_streams`
--

LOCK TABLES `broadcast_streams` WRITE;
/*!40000 ALTER TABLE `broadcast_streams` DISABLE KEYS */;
INSERT INTO `broadcast_streams` VALUES (1,1,'ライブカメラ1','camera1','オフィスの監視カメラ',NULL,1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(2,1,'ライブカメラ2','camera2','エントランスの監視カメラ',NULL,1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(3,1,'オーディオストリーム1','audio_stream1','スタジオのマイク入力',NULL,1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(4,2,'イベント配信','event_conference','イベント配信用チャンネル',NULL,1,'2026-02-05 06:47:34','2026-02-05 06:47:34'),(5,3,'テスト配信','test_stream','テスト用配信',NULL,1,'2026-02-05 06:47:34','2026-02-05 06:47:34');
/*!40000 ALTER TABLE `broadcast_streams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,'admin'),(2,'配信'),(3,'クライアント'),(4,'テスト1'),(5,'テスト2'),(6,'テスト3'),(7,'テスト4');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `level` int DEFAULT NULL,
  `job_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'python',12,6),(3,'リン',1,1),(4,'ユウ',3,3),(11,'s',1,1),(12,'a',1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-05 18:19:07
