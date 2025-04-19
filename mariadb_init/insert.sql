INSERT INTO registi (nome_completo, eta)
VALUES (
    'Christopher Nolan',
    54
);
INSERT INTO film (
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

INSERT INTO film (
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

DELETE FROM film;
DELETE FROM registi;
