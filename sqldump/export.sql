-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: test1
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
  `credits` decimal(3,2) DEFAULT NULL,

  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_list`
--

LOCK TABLES `course_list` WRITE;
/*!40000 ALTER TABLE `course_list` DISABLE KEYS */;
INSERT INTO `course_list` VALUES (1,'DBMS','A101','12',2020,3,4.00),(2,'MATH','A103','30',2020,3,3.00),(3,'OS','A105','10',2020,3,3.00);
/*!40000 ALTER TABLE `course_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `did` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `dname` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `building` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `budget` int DEFAULT NULL,
  `contactno` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `fid` int DEFAULT NULL,
  `since` date DEFAULT NULL,
  PRIMARY KEY (`did`),
  KEY `managed_by_idx` (`fid`),
  CONSTRAINT `managed_by` FOREIGN KEY (`fid`) REFERENCES `faculty` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES ('CE','Civil Engineering','Pod 1D',800000,'9675854417',190001029,NULL),('CS','Computer Science','Pod 1A',1000000,'9876543201',1,NULL),('EE','Electrical Engineering','Pod 1B',900000,'2812729',2,NULL),('ME','Mechanical Engineering','Pod 1C',900000,'6282829',NULL,NULL);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `departmentview`
--

DROP TABLE IF EXISTS `departmentview`;
/*!50001 DROP VIEW IF EXISTS `departmentview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `departmentview` AS SELECT 
 1 AS `did`,
 1 AS `dname`,
 1 AS `building`,
 1 AS `budget`,
 1 AS `contactno`,
 1 AS `fid`,
 1 AS `fname`,
 1 AS `phone`,
 1 AS `address`,
 1 AS `since`*/;
SET character_set_client = @saved_cs_client;

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
  `grade_endsem` varchar(2) DEFAULT NULL,
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
INSERT INTO `enroll` VALUES (190001029,1,'A','AA'),(190001029,2,'A','AA'),(190001090,2,'AB','BB'),(190001090,3,'B','B');
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
  `fname` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `address` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `salary` int DEFAULT '45000',
  `email` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `password` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `gender` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `position` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Robert Williams','9999282822','221b , Baker street',50000,'aba@abc.in','1986-01-16','81dc9bdb52d04dc20036dbd8313ed055','Male',' Professor'),(2,'Helium','None','None',45000,'helium@institute.in','1994-01-13','81dc9bdb52d04dc20036dbd8313ed055','Female','Assistant Professor'),(3,'Freeman','None','None',45000,'freeman@bmail.com','2020-10-01','81dc9bdb52d04dc20036dbd8313ed055','Male','Visting Professor'),(110109,'krishanu',NULL,NULL,53000,NULL,NULL,'56536b749a7fe62da7f62a04563acf32','Male','Associate Professor'),(190001029,'krishanu',NULL,NULL,45000,NULL,NULL,'56536b749a7fe62da7f62a04563acf32','Male',NULL);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `has`
--

DROP TABLE IF EXISTS `has`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `has` (
  `has_did` varchar(45) COLLATE latin1_bin NOT NULL,
  `has_pid` int NOT NULL,
  `date_implemented` date NOT NULL,
  PRIMARY KEY (`has_did`,`has_pid`),
  KEY `has_pid` (`has_pid`),
  CONSTRAINT `has_did` FOREIGN KEY (`has_did`) REFERENCES `department` (`did`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `has_pid` FOREIGN KEY (`has_pid`) REFERENCES `program` (`program_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `has`
--

LOCK TABLES `has` WRITE;
/*!40000 ALTER TABLE `has` DISABLE KEYS */;
/*!40000 ALTER TABLE `has` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `program_id` int NOT NULL,
  `program_name` varchar(45) COLLATE latin1_bin DEFAULT NULL,
  `program_duration` int DEFAULT NULL,
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
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
  `sname` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `address` varchar(200) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `cpi` decimal(4,2) DEFAULT NULL,
  `class` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `program` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `dob_dd` int DEFAULT NULL,
  `dob_mm` int DEFAULT NULL,
  `dob_yy` int DEFAULT NULL,
  `password` varchar(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `did` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `is_in_idx` (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'avc','122','sada',9.90,'2','B Tech','asda@ada.in',2,4,1986,'81dc9bdb52d04dc20036dbd8313ed055','CS'),(190001010,'kuldeep',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'a8029adfae3bca6d42ac99453b200db9','EE'),(190001011,'abc',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'900150983cd24fb0d6963f7d28e17f72','CE'),(190001029,'krishanu','123456789','100-flats',9.00,'2','cse','email@email.com',1,1,2001,'56536b749a7fe62da7f62a04563acf32','CS'),(190001090,'monu','9134530222','123-lankenshire',9.67,'2','cse','cse190001030@iiti.ac.in',38,8,2001,'root','EE');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaches`
--

DROP TABLE IF EXISTS `teaches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teaches` (
  `fid` int NOT NULL,
  `cid` int NOT NULL,
  PRIMARY KEY (`fid`,`cid`),
  KEY `cid_teaches_idx` (`cid`),
  CONSTRAINT `cid_teaches` FOREIGN KEY (`cid`) REFERENCES `course_list` (`cid`),
  CONSTRAINT `fid_teaches` FOREIGN KEY (`fid`) REFERENCES `faculty` (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaches`
--

LOCK TABLES `teaches` WRITE;
/*!40000 ALTER TABLE `teaches` DISABLE KEYS */;
INSERT INTO `teaches` VALUES (1,1),(1,2),(2,3);
/*!40000 ALTER TABLE `teaches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works_in`
--

DROP TABLE IF EXISTS `works_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `works_in` (
  `fid` int NOT NULL,
  `did` varchar(45) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`fid`,`did`),
  KEY `did_idx` (`did`),
  CONSTRAINT `did` FOREIGN KEY (`did`) REFERENCES `department` (`did`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fid` FOREIGN KEY (`fid`) REFERENCES `faculty` (`fid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works_in`
--

LOCK TABLES `works_in` WRITE;
/*!40000 ALTER TABLE `works_in` DISABLE KEYS */;
INSERT INTO `works_in` VALUES (1,'CS',NULL),(2,'CS',NULL),(3,'CS',NULL),(110109,'ME',NULL),(190001029,'EE',NULL);
/*!40000 ALTER TABLE `works_in` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `departmentview`
--

/*!50001 DROP VIEW IF EXISTS `departmentview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_bin */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `departmentview` AS select `department`.`did` AS `did`,`department`.`dname` AS `dname`,`department`.`building` AS `building`,`department`.`budget` AS `budget`,`department`.`contactno` AS `contactno`,`faculty`.`fid` AS `fid`,`faculty`.`fname` AS `fname`,`faculty`.`phone` AS `phone`,`faculty`.`email` AS `address`,`department`.`since` AS `since` from (`department` left join `faculty` on((`department`.`fid` = `faculty`.`fid`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-29 17:35:08
