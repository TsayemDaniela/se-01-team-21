CREATE DATABASE  IF NOT EXISTS `SEG21TEST` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `SEG21TEST`;
-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: SEG21
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `instructor_id` int NOT NULL,
  `factory_id` int NOT NULL,
  `distributor_id` int NOT NULL,
  `wholesaler_id` int DEFAULT NULL,
  `retailer_id` int DEFAULT NULL,
  `session_length` int NOT NULL DEFAULT '26',
  `rounds_completed` int NOT NULL DEFAULT '0',
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `info_sharing` tinyint(1) NOT NULL DEFAULT '0',
  `holding_cost` double NOT NULL DEFAULT '0.5',
  `backlog_cost` double NOT NULL DEFAULT '1',
  `info_delay` int NOT NULL DEFAULT '2',
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `game_id_UNIQUE` (`game_id`),
  KEY `fk_instructor_idx` (`instructor_id`),
  KEY `fk_distributor_idx` (`distributor_id`),
  KEY `fk_factory_idx` (`factory_id`),
  KEY `fk_retailer_idx` (`retailer_id`),
  KEY `fk_wholesaler_idx` (`wholesaler_id`),
  CONSTRAINT `fk_distributor` FOREIGN KEY (`distributor_id`) REFERENCES `player_session` (`player_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_factory` FOREIGN KEY (`factory_id`) REFERENCES `player_session` (`player_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_instructor` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`),
  CONSTRAINT `fk_retailer` FOREIGN KEY (`retailer_id`) REFERENCES `player_session` (`player_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_wholesaler` FOREIGN KEY (`wholesaler_id`) REFERENCES `player_session` (`player_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `instructor_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `hash` binary(60) NOT NULL,
  PRIMARY KEY (`instructor_id`),
  UNIQUE KEY `instructor_id_UNIQUE` (`instructor_id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `instructor_session`
--

DROP TABLE IF EXISTS `instructor_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor_session` (
  `session_id` binary(44) NOT NULL,
  `instructor_id_fk` int NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`session_id`),
  UNIQUE KEY `session_id_UNIQUE` (`session_id`),
  KEY `fk_instructor_session_idx` (`instructor_id_fk`),
  CONSTRAINT `fk_instructor_session` FOREIGN KEY (`instructor_id_fk`) REFERENCES `instructor` (`instructor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_session`
--

DROP TABLE IF EXISTS `player_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_session` (
  `player_id` int NOT NULL AUTO_INCREMENT,
  `session_id` binary(44) NOT NULL,
  `game_id` int DEFAULT NULL,
  `password` varchar(45) NOT NULL,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `player_id_UNIQUE` (`player_id`),
  KEY `fk_player_session_1_idx` (`game_id`),
  CONSTRAINT `fk_game_id` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-09 19:22:17