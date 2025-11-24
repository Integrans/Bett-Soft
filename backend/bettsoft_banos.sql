-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: bettsoft
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `banos`
--

DROP TABLE IF EXISTS `banos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `banos` (
  `id_bano` int NOT NULL AUTO_INCREMENT,
  `edificio` varchar(50) NOT NULL,
  `nivel` int NOT NULL,
  `sexo` enum('H','M','Mixto') NOT NULL,
  `tiene_orinal` tinyint(1) NOT NULL DEFAULT '0',
  `tiene_taza` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_bano`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banos`
--

LOCK TABLES `banos` WRITE;
/*!40000 ALTER TABLE `banos` DISABLE KEYS */;
INSERT INTO `banos` VALUES (1,'A-1',1,'M',0,1),(2,'A-1',2,'H',1,1),(3,'A-2',1,'M',0,1),(4,'A-2',2,'H',1,1),(5,'A-3',1,'M',0,1),(6,'A-3',2,'H',1,1),(7,'A-4',1,'M',0,1),(8,'A-4',2,'H',1,1),(9,'A-5',1,'M',0,1),(10,'A-5',2,'H',1,1),(11,'A-6',1,'M',0,1),(12,'A-6',2,'H',1,1),(13,'A-7',1,'M',0,1),(14,'A-7',2,'Mixto',0,1),(15,'A-8',1,'M',0,1),(16,'A-8',2,'H',1,1),(17,'A-9',1,'M',0,1),(18,'A-9',2,'H',1,1),(19,'A-10',1,'M',0,1),(20,'A-10',2,'H',1,1),(21,'A-11',1,'M',0,1),(22,'A-11',2,'H',1,1),(23,'A-12',1,'M',0,1),(24,'A-12',2,'H',1,1),(25,'A-13',1,'M',0,1),(26,'A-13',2,'H',1,1),(27,'A-14',1,'M',0,1),(28,'A-14',2,'H',1,1),(29,'A-15',1,'M',0,1),(30,'A-15',1,'H',1,1),(31,'A-15',2,'M',0,1),(32,'A-15',2,'H',1,1);
/*!40000 ALTER TABLE `banos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-22 23:28:23
