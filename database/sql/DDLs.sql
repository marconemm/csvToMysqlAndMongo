DROP DATABASE `projeto_database_db`;
CREATE DATABASE IF NOT EXISTS `projeto_database_db` DEFAULT CHARACTER SET utf8mb4 COLLATE 'utf8mb4_general_ci';
-- ****
-- Seguir a seguinte ordem de criação das tabelas:
-- 1-) Criar tabela type_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`type_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idtype_tbl_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `type_UNIQUE` (`type` ASC) VISIBLE)
ENGINE = InnoDB;
-- 2-) Criar tabela rating_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`rating_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `rating_UNIQUE` (`rating` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;
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
  INDEX `fk_type_id` (`type_id` ASC) VISIBLE,
  INDEX `fk_rating_id` (`rating_id` ASC) VISIBLE,
  CONSTRAINT `fk_type_id`
    FOREIGN KEY (`type_id`)
    REFERENCES `projeto_database_db`.`type_tbl` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_rating_id`
    FOREIGN KEY (`rating_id`)
    REFERENCES `projeto_database_db`.`rating_tbl` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;
-- 4-) Criar tabela diretor_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`director_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `director` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;
-- 5-) Criar tabela cast_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`cast_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cast` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;
-- 6-) Criar tabela country_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`country_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `country` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `nome_UNIQUE` (`country` ASC) VISIBLE)
ENGINE = InnoDB;
-- 7-) Criar tabela listed_in_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`listed_in_tbl` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `listed_in` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `nome_UNIQUE` (`listed_in` ASC) VISIBLE)
ENGINE = InnoDB;
-- 8-) Criar tabela listed_in_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`show_director_tbl` (
  `id_show` INT NOT NULL,
  `id_director` INT NOT NULL,
  INDEX `fk_show_director_tbl_1_idx` (`id_director` ASC) VISIBLE,
  INDEX `fk_show_director_tbl_2_idx` (`id_show` ASC) VISIBLE,
  CONSTRAINT `fk_show_director_tbl_1`
    FOREIGN KEY (`id_director`)
    REFERENCES `projeto_database_db`.`director_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_show_director_tbl_2`
    FOREIGN KEY (`id_show`)
    REFERENCES `projeto_database_db`.`show_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
-- 9-) Criar tabela show_cast_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`show_cast_tbl` (
  `id_show` INT NOT NULL,
  `id_cast` INT NOT NULL,
  INDEX `fk_show_cast_tbl_1_idx` (`id_show` ASC) VISIBLE,
  INDEX `fk_show_cast_tbl_2_idx` (`id_cast` ASC) VISIBLE,
  CONSTRAINT `fk_show_cast_tbl_1`
    FOREIGN KEY (`id_show`)
    REFERENCES `projeto_database_db`.`show_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_show_cast_tbl_2`
    FOREIGN KEY (`id_cast`)
    REFERENCES `projeto_database_db`.`cast_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
-- 10-) Criar tabela show_country_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`show_country_tbl` (
  `id_show` INT NOT NULL,
  `id_country` INT NOT NULL,
  INDEX `fk_show_id_idx` (`id_show` ASC) VISIBLE,
  INDEX `fk_country_id_idx` (`id_country` ASC) VISIBLE,
  CONSTRAINT `fk_show_id`
    FOREIGN KEY (`id_show`)
    REFERENCES `projeto_database_db`.`show_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_country_id`
    FOREIGN KEY (`id_country`)
    REFERENCES `projeto_database_db`.`country_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
-- 11-) Criar tabela show_listed_in_tbl:
CREATE TABLE IF NOT EXISTS `projeto_database_db`.`show_listed_in_tbl` (
  `id_show` INT NOT NULL,
  `id_listedin` INT NOT NULL,
  INDEX `fk_listedin_id_idx` (`id_listedin` ASC) VISIBLE,
  INDEX `fk_show_id_idx` (`id_show` ASC) VISIBLE,
  CONSTRAINT `fk_listedin_id`
    FOREIGN KEY (`id_listedin`)
    REFERENCES `projeto_database_db`.`listed_in_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_show_listedin_id`
    FOREIGN KEY (`id_show`)
    REFERENCES `projeto_database_db`.`show_tbl` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;
