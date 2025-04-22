
INSERT INTO registi (nome_completo, eta)
VALUES (
    'Christopher Nolan',
    54
);
INSERT INTO movies (
    titolo,
    regista,
    anno,
    genere,
    piattaforma_1,
    piattaforma_2
 )
VALUES (
    'Inception',
    1,
    2010,
    'Fantascienza',
    'Amazon Prime Video',
    'NOW'
 );

INSERT INTO movies (
    titolo,
    regista,
    anno,
    genere,
    piattaforma_1,
    piattaforma_2
 )
VALUES (
    'Interstellar',
    1,
    2014,
    'Fantascienza',
    'Paramount+',
    'Amazon Prime Video'
);

DELETE FROM registi;

DROP DATABASE text_to_sql_DB;

DELETE FROM movies;

INSERT INTO movies(titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2) VALUES
("Inception", "Christopher Nolan", 54, 2010, "Fantascienza", "Amazon Prime Video", "NOW");