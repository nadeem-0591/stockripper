-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema stockripper
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema stockripper
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `stockripper` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `stockripper` ;

-- -----------------------------------------------------
-- Table `stockripper`.`dailyruns`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`dailyruns` (
  `ticker` VARCHAR(10) NOT NULL,
  `startdate` DATE NOT NULL,
  `enddate` DATE NOT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`earningcalender`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`earningcalender` (
  `ticker` VARCHAR(20) NOT NULL,
  `company` VARCHAR(300) NULL DEFAULT NULL,
  `startdatetime` DATETIME NULL DEFAULT NULL,
  `datetimetype` VARCHAR(10) NULL DEFAULT NULL,
  `epsestimate` DECIMAL(10,2) NULL DEFAULT NULL,
  `epsactual` DECIMAL(10,2) NULL DEFAULT NULL,
  `epssurpricepct` DECIMAL(10,2) NULL DEFAULT NULL,
  `timezone` VARCHAR(5) NULL DEFAULT NULL,
  `gmtoffsetmilliseconds` INT NULL DEFAULT NULL,
  `quotetype` VARCHAR(45) NULL DEFAULT NULL,
  `date` DATE NOT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`earningestimate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`earningestimate` (
  `ticker` VARCHAR(20) NOT NULL,
  `quarter` VARCHAR(45) NULL DEFAULT NULL,
  `noofanalyst` DECIMAL(10,2) NULL DEFAULT NULL,
  `avgestimate` DECIMAL(10,2) NULL DEFAULT NULL,
  `lowestimate` DECIMAL(10,2) NULL DEFAULT NULL,
  `highestimate` DECIMAL(10,2) NULL DEFAULT NULL,
  `yearagoeps` DECIMAL(10,2) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`earninghistory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`earninghistory` (
  `ticker` VARCHAR(20) NOT NULL,
  `quarter` VARCHAR(45) NULL DEFAULT NULL,
  `esteps` DECIMAL(10,2) NULL DEFAULT NULL,
  `actualeps` DECIMAL(10,2) NULL DEFAULT NULL,
  `difference` DECIMAL(10,2) NULL DEFAULT NULL,
  `surprise` DECIMAL(10,2) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`epsrevisions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`epsrevisions` (
  `ticker` VARCHAR(20) NOT NULL,
  `quarter` VARCHAR(45) NULL DEFAULT NULL,
  `uplast7days` DECIMAL(10,2) NULL DEFAULT NULL,
  `uplast30days` DECIMAL(10,2) NULL DEFAULT NULL,
  `downlast7days` DECIMAL(10,2) NULL DEFAULT NULL,
  `downlast30days` DECIMAL(10,2) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`epstrend`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`epstrend` (
  `ticker` VARCHAR(20) NOT NULL,
  `quarter` VARCHAR(45) NULL DEFAULT NULL,
  `currentestimate` DECIMAL(10,2) NULL DEFAULT NULL,
  `7daysago` DECIMAL(10,2) NULL DEFAULT NULL,
  `30daysago` DECIMAL(10,2) NULL DEFAULT NULL,
  `60daysago` DECIMAL(10,2) NULL DEFAULT NULL,
  `90daysago` DECIMAL(10,2) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`growthestimates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`growthestimates` (
  `ticker` VARCHAR(20) NOT NULL,
  `division` VARCHAR(45) NULL DEFAULT NULL,
  `currqtr` DECIMAL(10,2) NULL DEFAULT NULL,
  `nextqtr` DECIMAL(10,2) NULL DEFAULT NULL,
  `curryear` DECIMAL(10,2) NULL DEFAULT NULL,
  `nextyear` DECIMAL(10,2) NULL DEFAULT NULL,
  `next5years` DECIMAL(10,2) NULL DEFAULT NULL,
  `past5years` DECIMAL(10,2) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`history`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`history` (
  `Ticker` VARCHAR(20) NOT NULL,
  `Date` DATE NULL DEFAULT NULL,
  `Open` DECIMAL(10,2) NULL DEFAULT NULL,
  `Close` DECIMAL(10,2) NULL DEFAULT NULL,
  `High` DECIMAL(10,2) NULL DEFAULT NULL,
  `Low` DECIMAL(10,2) NULL DEFAULT NULL,
  `Adj_close` DECIMAL(10,2) NULL DEFAULT NULL,
  `Volume` DECIMAL(15,2) NULL DEFAULT NULL,
  `dffrnc_btn_prvsdy_cls` FLOAT NULL DEFAULT NULL,
  `is_prvsdy_dffrnc_cls_pstv` TINYINT(1) NULL DEFAULT NULL,
  `dffrnc_btn_prvsdy_volume` DECIMAL(10,2) NULL DEFAULT NULL,
  `is_prvsdy_dffrnc_vlme_pstv` TINYINT(1) NULL DEFAULT NULL,
  `cdate` DATE NOT NULL,
  `meanvolume` DECIMAL(15,2) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `stockripper`.`revenueestimates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stockripper`.`revenueestimates` (
  `ticker` VARCHAR(20) NOT NULL,
  `quarter` VARCHAR(45) NULL DEFAULT NULL,
  `noofanalyst` INT NULL DEFAULT NULL,
  `avgestimate` VARCHAR(20) NULL DEFAULT NULL,
  `lowestimate` VARCHAR(20) NULL DEFAULT NULL,
  `highestimate` VARCHAR(20) NULL DEFAULT NULL,
  `yearagosales` VARCHAR(20) NULL DEFAULT NULL,
  `date` DATE NULL DEFAULT NULL,
  `salesgrowthpercent` DECIMAL(10,2) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
