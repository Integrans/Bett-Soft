-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: bettsoft
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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Administrador General','admin@bettsoft.com','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),(2,'Admin','admin@fes.mx','$2b$12$Kjin68rQeUt50IXS4jKceuCd5mNid2jWEoi4DGIZTrktRkf4BmTXi'),(3,'Omar','fes@acatlan.unam.mx','$2b$12$j1Z8pXp847Tp9O44agykj.1gCNaJZwT62upTMddjd3vWgqIaPspQ.');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banos`
--

LOCK TABLES `banos` WRITE;
/*!40000 ALTER TABLE `banos` DISABLE KEYS */;
INSERT INTO `banos` VALUES (1,'A1-A2',1,'M',0,1),(2,'A1-A2',2,'H',1,1),(3,'A3-A4',1,'M',0,1),(4,'A3-A4',2,'H',1,1),(5,'A5-A6',1,'M',0,1),(6,'A5-A6',2,'H',1,1),(7,'A7-A8',1,'M',0,1),(8,'A7-A8',2,'Mixto',0,1),(9,'A9-A10',1,'M',0,1),(10,'A9-A10',2,'H',1,1),(11,'A11-A12',1,'M',0,1),(12,'A11-A12',2,'H',1,1),(13,'Idiomas',1,'H',1,1),(14,'Idiomas',1,'M',0,1),(15,'Idiomas',2,'H',1,1),(16,'Idiomas',2,'M',0,1),(17,'A15',0,'H',1,1),(18,'A15',0,'M',0,1),(19,'A15',1,'H',1,1),(20,'A15',1,'M',0,1),(21,'A15',2,'H',1,1),(22,'A15',2,'M',0,1);
/*!40000 ALTER TABLE `banos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_incidente`
--

DROP TABLE IF EXISTS `categorias_incidente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_incidente` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `prioridad_default` enum('alta','media','baja') NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_incidente`
--

LOCK TABLES `categorias_incidente` WRITE;
/*!40000 ALTER TABLE `categorias_incidente` DISABLE KEYS */;
INSERT INTO `categorias_incidente` VALUES (1,'fuga','Fuga de agua o tuberías','alta'),(2,'taza_tapada','Taza de baño tapada','alta'),(3,'orinal_tapado','Orinal tapado','alta'),(4,'no_papel','No hay papel en dispensador','media'),(5,'no_jabon','No hay jabón en dispensador','media'),(6,'suciedad','Sanitario o área sucia','baja'),(7,'mal_olor','Presencia de malos olores','baja');
/*!40000 ALTER TABLE `categorias_incidente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_reporte`
--

DROP TABLE IF EXISTS `estados_reporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_reporte` (
  `id_estado` int NOT NULL AUTO_INCREMENT,
  `nombre` enum('en_proceso','resuelto','descartado') NOT NULL,
  PRIMARY KEY (`id_estado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_reporte`
--

LOCK TABLES `estados_reporte` WRITE;
/*!40000 ALTER TABLE `estados_reporte` DISABLE KEYS */;
INSERT INTO `estados_reporte` VALUES (1,'en_proceso'),(2,'resuelto'),(3,'descartado');
/*!40000 ALTER TABLE `estados_reporte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_reportes`
--

DROP TABLE IF EXISTS `historial_reportes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_reportes` (
  `id_historial` int NOT NULL AUTO_INCREMENT,
  `id_reporte` int NOT NULL,
  `id_admin` int NOT NULL,
  `campo_modificado` varchar(50) NOT NULL,
  `valor_anterior` varchar(100) DEFAULT NULL,
  `valor_nuevo` varchar(100) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT NULL,
  PRIMARY KEY (`id_historial`),
  KEY `id_reporte` (`id_reporte`),
  KEY `id_admin` (`id_admin`),
  KEY `ix_historial_reportes_id_historial` (`id_historial`),
  CONSTRAINT `historial_reportes_ibfk_1` FOREIGN KEY (`id_reporte`) REFERENCES `reportes` (`id_reporte`),
  CONSTRAINT `historial_reportes_ibfk_2` FOREIGN KEY (`id_admin`) REFERENCES `admins` (`id_admin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_reportes`
--

LOCK TABLES `historial_reportes` WRITE;
/*!40000 ALTER TABLE `historial_reportes` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_reportes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reportes`
--

DROP TABLE IF EXISTS `reportes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reportes` (
  `id_reporte` int NOT NULL AUTO_INCREMENT,
  `folio` varchar(20) NOT NULL,
  `numero_cuenta` varchar(50) NOT NULL,
  `id_bano` int NOT NULL,
  `id_categoria` int NOT NULL,
  `id_estado` int NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `es_anonimo` int DEFAULT NULL,
  `prioridad_asignada` enum('alta','media','baja') DEFAULT NULL,
  `imagen_url` varchar(300) DEFAULT NULL,
  `taza_o_orinal` enum('taza','orinal') DEFAULT NULL,
  `pasillo` enum('frente','atras') DEFAULT NULL,
  `tipo_reporte` enum('fuga','taza_tapada','orinal_tapado','no_papel','no_jabon','suciedad','mal_olor') NOT NULL,
  `edificio` varchar(50) NOT NULL,
  `sexo` enum('H','M','Mixto') NOT NULL,
  PRIMARY KEY (`id_reporte`),
  UNIQUE KEY `folio` (`folio`),
  KEY `id_bano` (`id_bano`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_estado` (`id_estado`),
  KEY `ix_reportes_id_reporte` (`id_reporte`),
  CONSTRAINT `reportes_ibfk_1` FOREIGN KEY (`id_bano`) REFERENCES `banos` (`id_bano`),
  CONSTRAINT `reportes_ibfk_2` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_incidente` (`id_categoria`),
  CONSTRAINT `reportes_ibfk_3` FOREIGN KEY (`id_estado`) REFERENCES `estados_reporte` (`id_estado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reportes`
--

LOCK TABLES `reportes` WRITE;
/*!40000 ALTER TABLE `reportes` DISABLE KEYS */;
INSERT INTO `reportes` VALUES (1,'INC-20251207-0001','123789',4,3,1,'2025-12-07 01:33:17',0,'media',NULL,'orinal','frente','orinal_tapado','A3-A4','H'),(2,'INC-20251207-0002','789',1,1,1,'2025-12-07 01:39:13',0,'alta',NULL,'taza','frente','fuga','A1-A2','M');
/*!40000 ALTER TABLE `reportes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-08  1:10:49
