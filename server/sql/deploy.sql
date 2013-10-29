SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `iu7_step` ;
CREATE SCHEMA IF NOT EXISTS `iu7_step` DEFAULT CHARACTER SET utf8 ;
USE `iu7_step` ;

-- -----------------------------------------------------
-- Table `iu7_step`.`person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`person` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`person` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `first_name` VARCHAR(20) NOT NULL ,
  `second_name` VARCHAR(20) NOT NULL ,
  `surname` VARCHAR(30) NOT NULL ,
  `gender` ENUM('male', 'female') NOT NULL ,
  `email` VARCHAR(128) NOT NULL ,
  `date_of_birth` DATE NOT NULL ,
  `description` TEXT NOT NULL ,
  `address` TEXT NOT NULL ,
  `phone` VARCHAR(20) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`city_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`city_type` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`city_type` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `short_title` VARCHAR(45) NULL ,
  `full_title` VARCHAR(200) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`city`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`city` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`city` (
  `id` INT NOT NULL ,
  `name` VARCHAR(45) NOT NULL ,
  `city_type_id` INT UNSIGNED ZEROFILL NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_city_to_city_type` (`city_type_id` ASC) ,
  CONSTRAINT `fk_city_to_city_type`
    FOREIGN KEY (`city_type_id` )
    REFERENCES `iu7_step`.`city_type` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`school_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`school_type` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`school_type` (
  `id` INT NOT NULL ,
  `short_title` VARCHAR(45) NOT NULL ,
  `full_title` VARCHAR(2048) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`school`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`school` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`school` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `title` VARCHAR(1024) NULL ,
  `number` INT UNSIGNED NULL ,
  `address` TEXT NOT NULL ,
  `city_id` INT NULL ,
  `type_id` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_school_to_city` (`city_id` ASC) ,
  INDEX `fk_school_to_sch_type` (`type_id` ASC) ,
  CONSTRAINT `fk_school_to_city`
    FOREIGN KEY (`city_id` )
    REFERENCES `iu7_step`.`city` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_school_to_sch_type`
    FOREIGN KEY (`type_id` )
    REFERENCES `iu7_step`.`school_type` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`competition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`competition` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`competition` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `year` YEAR NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `year_UNIQUE` (`year` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`criteria_title`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`criteria_title` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`criteria_title` (
  `id` INT NOT NULL ,
  `short_name` VARCHAR(45) NOT NULL ,
  `full_name` TEXT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`criteria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`criteria` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`criteria` (
  `id` INT UNSIGNED NOT NULL ,
  `criteria_title_id` INT NULL ,
  `competition_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_criteria_to_competition` (`competition_id` ASC) ,
  INDEX `fk_criteria_to_crit_title` (`criteria_title_id` ASC) ,
  CONSTRAINT `fk_criteria_to_competition`
    FOREIGN KEY (`competition_id` )
    REFERENCES `iu7_step`.`competition` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_criteria_to_crit_title`
    FOREIGN KEY (`criteria_title_id` )
    REFERENCES `iu7_step`.`criteria_title` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`range`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`range` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`range` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `criteria_number` INT UNSIGNED NOT NULL ,
  `type` ENUM('expert', 'reviewer') NOT NULL ,
  `min_score` TINYINT UNSIGNED NOT NULL ,
  `max_score` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) ,
  CONSTRAINT `fk_range_to_criteria`
    FOREIGN KEY (`criteria_number` )
    REFERENCES `iu7_step`.`criteria` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`role` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`role` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `person_id` INT UNSIGNED NOT NULL ,
  `competition_id` INT UNSIGNED NOT NULL ,
  `role` ENUM('expert', 'reviewer', 'admin', 'participant', 'curator') NOT NULL COMMENT '\n' ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_role_to_peorson` (`person_id` ASC) ,
  INDEX `fk_role_to_compit` (`competition_id` ASC) ,
  CONSTRAINT `fk_role_to_peorson`
    FOREIGN KEY (`person_id` )
    REFERENCES `iu7_step`.`person` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_role_to_compit`
    FOREIGN KEY (`competition_id` )
    REFERENCES `iu7_step`.`competition` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`work`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`work` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`work` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `participant_id` INT UNSIGNED NOT NULL ,
  `school_id` INT UNSIGNED NULL ,
  `curator_id` INT UNSIGNED NULL ,
  `state` ENUM('none', 'passes', 'not passed') NOT NULL ,
  `title` VARCHAR(2048) NOT NULL ,
  `registration_date` DATE NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_work_to_school` (`school_id` ASC) ,
  INDEX `fk_work_to_curator` (`curator_id` ASC) ,
  INDEX `fk_work_to_participant` (`participant_id` ASC) ,
  CONSTRAINT `fk_work_to_school`
    FOREIGN KEY (`school_id` )
    REFERENCES `iu7_step`.`school` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_work_to_curator`
    FOREIGN KEY (`curator_id` )
    REFERENCES `iu7_step`.`role` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_work_to_participant`
    FOREIGN KEY (`participant_id` )
    REFERENCES `iu7_step`.`role` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`score`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`score` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`score` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `work_id` INT UNSIGNED NOT NULL ,
  `expert_id` INT UNSIGNED NOT NULL ,
  `state` ENUM('uncomplete', 'complete') NOT NULL ,
  `date` DATE NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_score_to_work` (`work_id` ASC) ,
  INDEX `fk_score_to_expert` (`expert_id` ASC) ,
  CONSTRAINT `fk_score_to_work`
    FOREIGN KEY (`work_id` )
    REFERENCES `iu7_step`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_score_to_expert`
    FOREIGN KEY (`expert_id` )
    REFERENCES `iu7_step`.`role` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`designition`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`designition` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`designition` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `work_id` INT UNSIGNED NOT NULL ,
  `expert_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_designition_to_expert` (`expert_id` ASC) ,
  INDEX `fk_work` (`work_id` ASC) ,
  CONSTRAINT `fk_designition_to_expert`
    FOREIGN KEY (`expert_id` )
    REFERENCES `iu7_step`.`role` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_work`
    FOREIGN KEY (`work_id` )
    REFERENCES `iu7_step`.`work` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`criteria_score`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`criteria_score` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`criteria_score` (
  `id` INT UNSIGNED NOT NULL ,
  `range_id` INT UNSIGNED NOT NULL ,
  `score_id` INT UNSIGNED NOT NULL ,
  `value` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_criteria_score_to_range` (`range_id` ASC) ,
  INDEX `fk_criteria_score_to_score` (`score_id` ASC) ,
  CONSTRAINT `fk_criteria_score_to_range`
    FOREIGN KEY (`range_id` )
    REFERENCES `iu7_step`.`range` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_criteria_score_to_score`
    FOREIGN KEY (`score_id` )
    REFERENCES `iu7_step`.`score` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `iu7_step`.`account`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `iu7_step`.`account` ;

CREATE  TABLE IF NOT EXISTS `iu7_step`.`account` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL ,
  `password_hash` VARCHAR(128) NOT NULL ,
  `person_id` INT UNSIGNED NOT NULL ,
  `admin_priv` TINYINT(1) NOT NULL DEFAULT false ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_account_to_people` (`person_id` ASC) ,
  UNIQUE INDEX `login_UNIQUE` (`login` ASC) ,
  CONSTRAINT `fk_account_to_people`
    FOREIGN KEY (`person_id` )
    REFERENCES `iu7_step`.`person` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Placeholder table for view `iu7_step`.`total_scores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `iu7_step`.`total_scores` (`work_id` INT, `sum(criteria_score.value)` INT);

-- -----------------------------------------------------
-- View `iu7_step`.`total_scores`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `iu7_step`.`total_scores` ;
DROP TABLE IF EXISTS `iu7_step`.`total_scores`;
USE `iu7_step`;
CREATE  OR REPLACE VIEW `iu7_step`.`total_scores` AS
SELECT score.work_id, sum(criteria_score.value) 

FROM score JOIN criteria_score ON score.id = criteria_score.score_id

GROUP BY score.work_id;

CREATE USER `iu7_dbuser`@`localhost` IDENTIFIED BY 'krakazabra2k';

grant DELETE on TABLE `iu7_step`.`role` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`role` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`role` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`role` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`score` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`score` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`score` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`score` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`school` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`school` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`school` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`school` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`competition` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`competition` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`competition` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`competition` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`designition` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`designition` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`designition` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`designition` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`work` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`work` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`work` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`work` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`person` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`person` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`person` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`person` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`range` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`range` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`range` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`range` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`total_scores` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`total_scores` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`total_scores` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`total_scores` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`criteria_score` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`criteria_score` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`criteria_score` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`criteria_score` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`account` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`account` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`account` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`account` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`criteria_title` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`criteria_title` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`criteria_title` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`criteria_title` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`school_type` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`school_type` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`school_type` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`school_type` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`city` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`city` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`city` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`city` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`city_type` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`city_type` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`city_type` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`city_type` to `iu7_dbuser`@`localhost`;
grant UPDATE on TABLE `iu7_step`.`criteria` to `iu7_dbuser`@`localhost`;
grant SELECT on TABLE `iu7_step`.`criteria` to `iu7_dbuser`@`localhost`;
grant INSERT on TABLE `iu7_step`.`criteria` to `iu7_dbuser`@`localhost`;
grant DELETE on TABLE `iu7_step`.`criteria` to `iu7_dbuser`@`localhost`;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

