CREATE DATABASE IF NOT EXISTS text_to_sql_DB;
USE text_to_sql_DB;

-- CREATE TABLE registi(
--     id_regista INT AUTO_INCREMENT PRIMARY KEY,
--     nome_completo VARCHAR(200) NOT NULL,
--     eta INT NOT NULL check(eta>0)
-- );

-- CREATE TABLE movies(
--     titolo VARCHAR(100) NOT NULL PRIMARY KEY,
--     regista INT NOT NULL,
--     anno INT NOT NULL check(anno>0),
--     genere VARCHAR(100) NOT NULL,
--     piattaforma_1 VARCHAR(200),
--     piattaforma_2 VARCHAR(200),
--     CONSTRAINT fk_film FOREIGN KEY(regista) REFERENCES registi(id_regista) ON DELETE CASCADE ON UPDATE RESTRICT
-- );

CREATE TABLE movies(
    titolo VARCHAR(100),
    regista VARCHAR(200) NOT NULL,
    eta_autore INT NOT NULL,
    anno INT NOT NULL check(anno>0),
    genere VARCHAR(100) NOT NULL,
    piattaforma_1 VARCHAR(200),
    piattaforma_2 VARCHAR(200),
    UNIQUE(titolo),
    PRIMARY KEY(regista, anno)
);