-- Comandos de manipula do banco de dados:
USE `projeto_database_db`;
SELECT *
FROM `type_tbl`;
select id
FROM `type_tbl`
WHERE type = "Movie";
SELECT *
FROM `rating_tbl`;
SELECT *
FROM `director_tbl`;
SELECT COUNT(*)
FROM `director_tbl`;
SELECT *
FROM `cast_tbl`;
SELECT id
FROM `cast_tbl`
WHERE `cast` = 'Ayça İnci';
SELECT *
FROM `cast_tbl`
WHERE id = 1710;
SELECT *
FROM `country_tbl`;
SELECT *
FROM `listed_in_tbl`;
SELECT *
FROM `show_tbl`;
SELECT id
FROM `show_tbl`
WHERE `title` = 'Dick Johnson Is Dead';
SELECT id
FROM `director_tbl`
WHERE `director` = 'Kirsten Johnson';
SELECT id
FROM `listed_in_tbl`
WHERE `listed_in` = 'Documentaries';
INSERT INTO `show_listed_in_tbl` (id_show, id_listed_in)
VALUES (1, 16);
-- Inner Joins:
-- Primeira consulta: monta a base do objeto "show".
SELECT s.id,
    s.title,
    s.release_year,
    s.date_added,
    s.description,
    s.duration,
    t.type,
    r.rating
FROM projeto_database_db.show_tbl AS s
    INNER JOIN projeto_database_db.type_tbl AS t ON s.type_id = t.id
    INNER JOIN projeto_database_db.rating_tbl AS r ON s.rating_id = r.id
WHERE s.id = 2;

-- Segunda consulta: alimentar a propriedade director_list do objeto show.
SELECT d.director
FROM projeto_database_db.show_tbl AS s
    INNER JOIN projeto_database_db.show_director_tbl AS sd ON s.id = sd.id_show
    INNER JOIN projeto_database_db.director_tbl AS d ON sd.id_director = d.id
WHERE s.id = 2;

-- Terceira consulta: alimenta a propriedade country_list do objeto show.
SELECT c.country
FROM projeto_database_db.show_tbl AS s
    INNER JOIN projeto_database_db.show_country_tbl AS sc ON s.id = sc.id_show
    INNER JOIN projeto_database_db.country_tbl AS c ON c.id = sc.id_country
WHERE s.id = 2;

-- Quarta consulta: alimenta a propriedade listed_in_list do objeto show.
SELECT li.listed_in
FROM projeto_database_db.show_tbl AS s
    INNER JOIN projeto_database_db.show_listed_in_tbl AS sli ON sli.id_show = s.id
    INNER JOIN projeto_database_db.listed_in_tbl AS li ON li.id = sli.id_listed_in
WHERE s.id = 2;
-- Quinta consulta: alimenta a propriedade cast_list do objeto show.
SELECT c.cast
FROM projeto_database_db.show_tbl AS s
    INNER JOIN projeto_database_db.show_cast_tbl AS sc ON sc.id_show = s.id
    INNER JOIN projeto_database_db.cast_tbl AS c ON c.id = sc.id_cast
WHERE s.id = 2;