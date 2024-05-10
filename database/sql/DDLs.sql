DROP DATABASE `projeto_database_db`;
CREATE DATABASE IF NOT EXISTS `projeto_database_db` DEFAULT CHARACTER SET utf8mb4;
-- ****
-- Seguir a seguinte ordem de criação das tabelas:
-- 1-) Criar tabela type_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`type_tbl` (
  `idtype_tbl` INT NOT NULL,
  `type` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`idtype_tbl`),
  UNIQUE INDEX `idtype_tbl_UNIQUE` (`idtype_tbl` ASC) VISIBLE,
  UNIQUE INDEX `type_UNIQUE` (`type` ASC) VISIBLE
) ENGINE = InnoDB;
-- 2-) Criar tabela rating_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`rating_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rating_UNIQUE` (`rating` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE
) ENGINE = InnoDB;
-- 3-) Criar tabela show_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`show_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `date_added` DATE NULL,
  `release_year` INT NOT NULL,
  `duration` VARCHAR(50) NULL,
  `description` VARCHAR(500) NOT NULL,
  `type_id` INT NOT NULL,
  `rating_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_type_id_idx` (`type_id` ASC) VISIBLE,
  INDEX `fk_rating_id_idx` (`rating_id` ASC) VISIBLE,
  CONSTRAINT `fk_type_id` FOREIGN KEY (`type_id`) REFERENCES `projeto_databse_db`.`type_tbl` (`idtype_tbl`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_rating_id` FOREIGN KEY (`rating_id`) REFERENCES `projeto_databse_db`.`rating_tbl` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;