-- Comandos de manipula do banco de dados:
USE `projeto_database_db`;
SELECT * FROM `type_tbl`;
select id FROM `type_tbl` WHERE type = "Movie";
SELECT * FROM `rating_tbl`;
SELECT * FROM `director_tbl`;
SELECT COUNT(*) FROM `director_tbl`;
SELECT * FROM `cast_tbl`;
SELECT id FROM `cast_tbl` WHERE `cast` = 'Ayça İnci';
SELECT * FROM `cast_tbl` WHERE id = 1710;
SELECT * FROM `country_tbl`;
SELECT * FROM `listed_in_tbl`;
SELECT * FROM `show_tbl`;
SELECT id FROM `show_tbl` WHERE `title` = 'Dick Johnson Is Dead';
SELECT id FROM `director_tbl` WHERE `director` = 'Kirsten Johnson';
SELECT id FROM `listed_in_tbl` WHERE `listed_in` = 'Documentaries';
INSERT INTO `show_listed_in_tbl` (id_show, id_listed_in) VALUES (1,	16);

-- Inner Joins:

SELECT show_tbl.id, show_tbl.title, show_tbl.release_year, type_tbl.type, rating_tbl.rating
FROM projeto_database_db.show_tbl
INNER JOIN projeto_database_db.type_tbl ON show_tbl.type_id = type_tbl.id
INNER JOIN projeto_database_db.rating_tbl ON show_tbl.rating_id = rating_tbl.id;



