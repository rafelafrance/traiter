/*
psql --dbname=traits --file=tables.sql

CREATE EXTENSION "uuid-ossp";

DROP ROLE traits_user;
CREATE ROLE traits_user NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
GRANT traits_user TO user_name;

DROP DATABASE traits;
DATABASE traits
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

DROP SCHEMA public;
CREATE SCHEMA public AUTHORIZATION postgres;
GRANT ALL ON SCHEMA public TO traits_user;
*/

DROP TABLE IF EXISTS measurements CASCADE;
DROP TABLE IF EXISTS associated_records CASCADE;
DROP TABLE IF EXISTS process_evidence CASCADE;
DROP TABLE IF EXISTS evidence CASCADE;
DROP TABLE IF EXISTS datasets CASCADE;
DROP TABLE IF EXISTS entities CASCADE;
DROP TABLE IF EXISTS planned_processes CASCADE;
DROP TABLE IF EXISTS measurement_standards CASCADE;
DROP TABLE IF EXISTS traits CASCADE;
DROP TABLE IF EXISTS taxon_concepts CASCADE;
DROP TABLE IF EXISTS "references" CASCADE;

DROP TYPE IF EXISTS reference_types CASCADE;
DROP TYPE IF EXISTS entity_scopes CASCADE;
DROP TYPE IF EXISTS sexes CASCADE;
DROP TYPE IF EXISTS planned_process_types CASCADE;
DROP TYPE IF EXISTS quality_classes CASCADE;
DROP TYPE IF EXISTS value_types CASCADE;

CREATE TYPE reference_types AS ENUM ('journal', 'book', 'dataset');
CREATE TYPE entity_scopes AS ENUM ('individual', 'population', 'species', 'clade');
CREATE TYPE sexes AS ENUM ('female', 'male', 'hermaphrodite');
CREATE TYPE planned_process_types AS ENUM ('observation', 'data_manipulation');
CREATE TYPE quality_classes AS ENUM ('high', 'medium', 'low');
CREATE TYPE value_types AS ENUM ('numeric', 'integer', 'range', 'enumeration', 'text', 'object');

CREATE TABLE "references" (
    reference_id    UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    reference_type  reference_types,
    bibtex          TEXT,
    title           TEXT,
    authors         TEXT,
    year            INT,
    journal         TEXT,
    volume          TEXT,
    issue           TEXT,
    pages           TEXT,
    doi             TEXT,
    uri             TEXT,
    remarks         TEXT
);

CREATE TABLE datasets (
    dataset_id            UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    reference_id          UUID REFERENCES "references",
    contributor           TEXT,
    institution           TEXT,
    collection            TEXT,
    license               TEXT,
    rights_holder         TEXT,
    information_withheld  TEXT,
    name                  TEXT,
    uri                   TEXT,
    contact_email         TEXT,
    remarks               TEXT
);
CREATE INDEX ON datasets (reference_id);

CREATE TABLE taxon_concepts (
    taxon_concept_id         UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    higher_taxon_concept_id  UUID REFERENCES taxon_concepts,
    taxon_concept            TEXT,
    taxonomic_rank           TEXT,
    accepted_usage_name      TEXT,
    original_name_usage      TEXT,
    name_according_to        TEXT,
    vernacular_names         TEXT,
    nomenclatural_code       TEXT,
    nomenclatural_status     TEXT,
    remarks                  TEXT
);
CREATE INDEX ON taxon_concepts (higher_taxon_concept_id);
CREATE INDEX ON taxon_concepts (taxon_concept);
CREATE INDEX ON taxon_concepts (taxonomic_rank);

CREATE TABLE entities (
    entity_id         UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    taxon_concept_id  UUID REFERENCES taxon_concepts,
    entity_scope      entity_scopes,
    sex               sexes,
    life_stage        TEXT,
    count             NUMERIC,
    remarks           TEXT,
    entered_by        TEXT,
    date_entered      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ON entities (taxon_concept_id);

CREATE TABLE evidence (
    evidence_id         UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    entity_id           UUID REFERENCES entities,
    dataset_id          UUID REFERENCES datasets,
    source_evidence_id  UUID REFERENCES evidence,
    reference_id        UUID REFERENCES "references",
    entity_scope        entity_scopes,
    specimen_id         UUID,
    artifact_id         UUID,
    remarks             TEXT,
    "count"             NUMERIC,
    entered_by          TEXT,
    date_entered        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ON evidence (entity_id);
CREATE INDEX ON evidence (dataset_id);
CREATE INDEX ON evidence (source_evidence_id);
CREATE INDEX ON evidence (reference_id);

CREATE TABLE associated_records (
    associated_record_id  UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    evidence_id           UUID REFERENCES evidence,
    uri                   TEXT,
    association_type      TEXT,
    external_id           TEXT,
    remarks               TEXT
);
CREATE INDEX ON associated_records (evidence_id);

CREATE TABLE planned_processes (
    planned_process_id    UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    reference_id          UUID REFERENCES "references",
    planned_process_type  planned_process_types,
    date_time             TIMESTAMP,
    date_time_max         TIMESTAMP,
    remarks               TEXT,
    entered_by            TEXT,
    date_entered          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ON planned_processes (reference_id);

CREATE TABLE process_evidence (
    evidence_id               UUID REFERENCES evidence,
    planned_process_id        UUID REFERENCES planned_processes
);
CREATE INDEX ON process_evidence (evidence_id);
CREATE INDEX ON process_evidence (planned_process_id);

CREATE TABLE traits (
    trait_id          UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    reference_id      UUID REFERENCES "references",
    taxon_concept_id  UUID REFERENCES taxon_concepts,
    trait             TEXT,
    definition        TEXT,
    role              TEXT,
    sex               sexes,
    life_stage        TEXT,
    uri               TEXT,
    remarks           TEXT
);
CREATE INDEX ON traits (reference_id);
CREATE INDEX ON traits (taxon_concept_id);

CREATE TABLE measurement_standards (
    measurement_standard_id  UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    trait_id                 UUID REFERENCES traits,
    reference_id             UUID REFERENCES "references",
    title                    TEXT,
    value_type               value_types,
    method                   TEXT,
    equation                 TEXT,
    units                    TEXT,
    quality                  quality_classes,
    value_enums              VARCHAR[],
    value_min                NUMERIC,
    value_max                NUMERIC,
    accuracy                 NUMERIC,
    remarks                  TEXT
);
CREATE INDEX ON measurement_standards (reference_id);
CREATE INDEX ON measurement_standards (trait_id);
CREATE INDEX ON measurement_standards (value_type);

CREATE TABLE measurements (
    measurement_id           UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
    planned_process_id       UUID REFERENCES planned_processes,
    measurement_standard_id  UUID REFERENCES measurement_standards,
    value                    NUMERIC,
    value_max                NUMERIC,
    value_accuracy           NUMERIC,
    value_enums              VARCHAR[],
    value_text               TEXT,
    value_object             UUID,
    quality                  quality_classes,
    remarks                  TEXT,
    entered_by               TEXT,
    date_entered             TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ON measurements (planned_process_id);
CREATE INDEX ON measurements (measurement_standard_id);
CREATE INDEX ON measurements (value);
CREATE INDEX ON measurements (value_max);
CREATE INDEX ON measurements (value_text);
CREATE INDEX ON measurements (value_object);
