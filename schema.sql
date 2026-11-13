-- Pet Adoption Finder - PostgreSQL 18 schema
-- Creates the 5 tables, their fields and the relationships between them.
-- initialise_db.py runs this file automatically.

CREATE TABLE shelters (
    shelter_id  SERIAL       NOT NULL,
    name        VARCHAR(100) NOT NULL,
    address     VARCHAR(255) NOT NULL,
    town        VARCHAR(50)  NOT NULL,
    county      VARCHAR(30)  NOT NULL,
    latitude    NUMERIC(9,6),
    longitude   NUMERIC(9,6),
    phone       VARCHAR(20),
    email       VARCHAR(100) NOT NULL,
    PRIMARY KEY (shelter_id)
);

CREATE TABLE users (
    user_id       SERIAL       NOT NULL,
    first_name    VARCHAR(50)  NOT NULL,
    last_name     VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(15)  NOT NULL DEFAULT 'adopter',
    shelter_id    INTEGER,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE animals (
    animal_id      SERIAL      NOT NULL,
    shelter_id     INTEGER     NOT NULL,
    name           VARCHAR(50) NOT NULL,
    species        VARCHAR(10) NOT NULL,
    breed          VARCHAR(60),
    age_months     INTEGER     NOT NULL,
    sex            VARCHAR(6)  NOT NULL,
    size           VARCHAR(6)  NOT NULL,
    good_with_kids BOOLEAN DEFAULT FALSE,
    description    TEXT,
    image_url      VARCHAR(255),
    status         VARCHAR(10) NOT NULL DEFAULT 'available',
    date_listed    DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (animal_id)
);

CREATE TABLE favourites (
    favourite_id SERIAL  NOT NULL,
    user_id      INTEGER NOT NULL,
    animal_id    INTEGER NOT NULL,
    saved_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (favourite_id),
    UNIQUE (user_id, animal_id)
);

CREATE TABLE enquiries (
    enquiry_id   SERIAL      NOT NULL,
    user_id      INTEGER     NOT NULL,
    animal_id    INTEGER     NOT NULL,
    message      TEXT        NOT NULL,
    status       VARCHAR(10) NOT NULL DEFAULT 'new',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (enquiry_id)
);

-- Relationships
ALTER TABLE users      ADD CONSTRAINT fk_users_shelter     FOREIGN KEY (shelter_id) REFERENCES shelters (shelter_id);
ALTER TABLE animals    ADD CONSTRAINT fk_animals_shelter   FOREIGN KEY (shelter_id) REFERENCES shelters (shelter_id);
ALTER TABLE favourites ADD CONSTRAINT fk_favourites_user   FOREIGN KEY (user_id)    REFERENCES users (user_id);
ALTER TABLE favourites ADD CONSTRAINT fk_favourites_animal FOREIGN KEY (animal_id)  REFERENCES animals (animal_id);
ALTER TABLE enquiries  ADD CONSTRAINT fk_enquiries_user    FOREIGN KEY (user_id)    REFERENCES users (user_id);
ALTER TABLE enquiries  ADD CONSTRAINT fk_enquiries_animal  FOREIGN KEY (animal_id)  REFERENCES animals (animal_id);
