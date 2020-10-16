-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: uni
-- ------------------------------------------------------
-- Server version	8.0.21

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

--
-- Table structure for table `course_list`
--

DROP TABLE IF EXISTS `course_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_list` (
  `cid` int NOT NULL,
  `cname` varchar(45) DEFAULT NULL,
  `room` varchar(45) DEFAULT NULL,
  `hours` varchar(45) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `sem` int DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_list`
--

LOCK TABLES `course_list` WRITE;
/*!40000 ALTER TABLE `course_list` DISABLE KEYS */;
INSERT INTO `course_list` VALUES (1,'DBMS','A101','12',2020,3),(2,'MATH','A103','30',2020,3),(3,'OS','A105','10',2020,3);
/*!40000 ALTER TABLE `course_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enroll`
--

DROP TABLE IF EXISTS `enroll`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enroll` (
  `sid` int NOT NULL,
  `cid` int NOT NULL,
  `grade` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`sid`,`cid`),
  KEY `cid_idx` (`cid`),
  CONSTRAINT `` FOREIGN KEY (`sid`) REFERENCES `student` (`sid`),
  CONSTRAINT `cid` FOREIGN KEY (`cid`) REFERENCES `course_list` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enroll`
--

LOCK TABLES `enroll` WRITE;
/*!40000 ALTER TABLE `enroll` DISABLE KEYS */;
INSERT INTO `enroll` VALUES (190001029,1,'A'),(190001029,2,'A'),(190001090,2,'AB'),(190001090,3,'B');
/*!40000 ALTER TABLE `enroll` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `fid` int NOT NULL,
  `fname` varchar(45) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `salary` int DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `password` varchar(45) NOT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Robert Williams','9999282822','221b , Baker street',50000,'aba@abc.in','1986-01-16','81dc9bdb52d04dc20036dbd8313ed055','Male','Associate Professor'),(110109,'krishanu',NULL,NULL,NULL,NULL,NULL,'56536b749a7fe62da7f62a04563acf32',NULL,NULL),(190001029,'krishanu',NULL,NULL,NULL,NULL,NULL,'56536b749a7fe62da7f62a04563acf32',NULL,NULL);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_cid`
--

DROP TABLE IF EXISTS `room_cid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_cid` (
  `room` varchar(45) NOT NULL,
  `time` int NOT NULL,
  `day` int NOT NULL,
  `ccid` int DEFAULT NULL,
  PRIMARY KEY (`room`,`time`,`day`),
  KEY `cid_idx` (`ccid`),
  KEY `cid_idx2` (`ccid`),
  KEY `cid_idx3` (`ccid`),
  CONSTRAINT `ccid` FOREIGN KEY (`ccid`) REFERENCES `course_list` (`cid`),
  CONSTRAINT `room` FOREIGN KEY (`room`) REFERENCES `room_list` (`room`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_cid`
--

LOCK TABLES `room_cid` WRITE;
/*!40000 ALTER TABLE `room_cid` DISABLE KEYS */;
INSERT INTO `room_cid` VALUES ('A101',7,1,1),('A101',7,2,1),('A101',7,4,1),('A101',7,6,1),('A103',8,6,2),('A103',13,1,2),('A103',13,3,2),('A103',16,3,3);
/*!40000 ALTER TABLE `room_cid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room_list`
--

DROP TABLE IF EXISTS `room_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room_list` (
  `room` varchar(45) NOT NULL,
  PRIMARY KEY (`room`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room_list`
--

LOCK TABLES `room_list` WRITE;
/*!40000 ALTER TABLE `room_list` DISABLE KEYS */;
INSERT INTO `room_list` VALUES ('A101'),('A102'),('A103');
/*!40000 ALTER TABLE `room_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `sid` int NOT NULL,
  `sname` varchar(45) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `cpi` decimal(4,2) DEFAULT NULL,
  `class` varchar(45) DEFAULT NULL,
  `program` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dob_dd` int DEFAULT NULL,
  `dob_mm` int DEFAULT NULL,
  `dob_yy` int DEFAULT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'avc','122','sada',9.90,'sda','dad','asda@ada.in',2,4,1986,'81dc9bdb52d04dc20036dbd8313ed055'),(190001010,'kuldeep',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'a8029adfae3bca6d42ac99453b200db9'),(190001011,'abc',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'900150983cd24fb0d6963f7d28e17f72'),(190001029,'krishanu','123456789','100-flats',9.00,'2','cse','email@email.com',1,1,2001,'56536b749a7fe62da7f62a04563acf32'),(190001090,'monu','9134530222','123-lankenshire',9.67,'2','cse','cse190001030@iiti.ac.in',38,8,2001,'root');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_dept`
--

DROP TABLE IF EXISTS `student_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_dept` (
  `sid` int NOT NULL,
  `dname` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  UNIQUE KEY `dname_UNIQUE` (`dname`),
  CONSTRAINT `sid` FOREIGN KEY (`sid`) REFERENCES `student` (`sid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_dept`
--

LOCK TABLES `student_dept` WRITE;
/*!40000 ALTER TABLE `student_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `student_dept` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-12 21:01:20
