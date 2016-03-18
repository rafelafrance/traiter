PRAGMA foreign_keys = ON;

-- CREATE TYPE reference_types AS ENUM ('journal', 'book', 'dataset');
-- CREATE TYPE entity_scopes AS ENUM ('individual', 'population', 'species', 'clade');
-- CREATE TYPE sexes AS ENUM ('female', 'male', 'hermaphrodite');
-- CREATE TYPE planned_process_types AS ENUM ('observation', 'data_manipulation');
-- CREATE TYPE quality_classes AS ENUM ('high', 'medium', 'low');
-- CREATE TYPE value_types AS ENUM ('numeric', 'integer', 'range', 'enumeration', 'text', 'object');

CREATE TABLE "references" (
    reference_id    BLOB PRIMARY KEY,
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
    dataset_id            BLOB PRIMARY KEY,
    reference_id          BLOB REFERENCES "references",
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
CREATE INDEX datasets_reference_id ON datasets (reference_id);

CREATE TABLE taxon_concepts (
    taxon_concept_id         BLOB PRIMARY KEY,
    higher_taxon_concept_id  BLOB REFERENCES taxon_concepts,
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
CREATE INDEX taxon_concepts_higher_taxon_concept_id ON taxon_concepts (higher_taxon_concept_id);
CREATE INDEX taxon_concepts_taxon_concept           ON taxon_concepts (taxon_concept);
CREATE INDEX taxon_concepts_taxonomic_rank          ON taxon_concepts (taxonomic_rank);

CREATE TABLE entities (
    entity_id         BLOB PRIMARY KEY,
    taxon_concept_id  BLOB REFERENCES taxon_concepts,
    entity_scope      entity_scopes,
    sex               sexes,
    life_stage        TEXT,
    count             NUMERIC,
    remarks           TEXT,
    entered_by        TEXT,
    date_entered      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX entities_taxon_concept_id ON entities (taxon_concept_id);

CREATE TABLE evidence (
    evidence_id         BLOB PRIMARY KEY,
    entity_id           BLOB REFERENCES entities,
    dataset_id          BLOB REFERENCES datasets,
    source_evidence_id  BLOB REFERENCES evidence,
    reference_id        BLOB REFERENCES "references",
    entity_scope        entity_scopes,
    specimen_id         BLOB,
    artifact_id         BLOB,
    remarks             TEXT,
    "count"             NUMERIC,
    entered_by          TEXT,
    date_entered        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX evidence_entity_id          ON evidence (entity_id);
CREATE INDEX evidence_dataset_id         ON evidence (dataset_id);
CREATE INDEX evidence_source_evidence_id ON evidence (source_evidence_id);
CREATE INDEX evidence_reference_id       ON evidence (reference_id);

CREATE TABLE associated_records (
    associated_record_id  BLOB PRIMARY KEY,
    evidence_id           BLOB REFERENCES evidence,
    uri                   TEXT,
    association_type      TEXT,
    external_id           TEXT,
    remarks               TEXT
);
CREATE INDEX associated_records_evidence_id ON associated_records (evidence_id);

CREATE TABLE planned_processes (
    planned_process_id    BLOB PRIMARY KEY,
    reference_id          BLOB REFERENCES "references",
    planned_process_type  planned_process_types,
    date_time             TIMESTAMP,
    date_time_max         TIMESTAMP,
    remarks               TEXT,
    entered_by            TEXT,
    date_entered          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX planned_processes_reference_id ON planned_processes (reference_id);

CREATE TABLE process_evidence (
    evidence_id               BLOB REFERENCES evidence,
    planned_process_id        BLOB REFERENCES planned_processes
);
CREATE INDEX process_evidence_evidence_id        ON process_evidence (evidence_id);
CREATE INDEX process_evidence_planned_process_id ON process_evidence (planned_process_id);

CREATE TABLE traits (
    trait_id          BLOB PRIMARY KEY,
    reference_id      BLOB REFERENCES "references",
    taxon_concept_id  BLOB REFERENCES taxon_concepts,
    trait             TEXT,
    definition        TEXT,
    role              TEXT,
    sex               sexes,
    life_stage        TEXT,
    uri               TEXT,
    remarks           TEXT
);
CREATE INDEX traits_reference_id     ON traits (reference_id);
CREATE INDEX traits_taxon_concept_id ON traits (taxon_concept_id);

CREATE TABLE measurement_standards (
    measurement_standard_id  BLOB PRIMARY KEY,
    trait_id                 BLOB REFERENCES traits,
    reference_id             BLOB REFERENCES "references",
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
CREATE INDEX measurement_standards_reference_id ON measurement_standards (reference_id);
CREATE INDEX measurement_standards_trait_id     ON measurement_standards (trait_id);
CREATE INDEX measurement_standards_value_type   ON measurement_standards (value_type);

CREATE TABLE measurements (
    measurement_id           BLOB PRIMARY KEY,
    planned_process_id       BLOB REFERENCES planned_processes,
    measurement_standard_id  BLOB REFERENCES measurement_standards,
    value                    NUMERIC,
    value_max                NUMERIC,
    value_accuracy           NUMERIC,
    value_enums              VARCHAR[],
    value_text               TEXT,
    value_object             BLOB,
    quality                  quality_classes,
    remarks                  TEXT,
    entered_by               TEXT,
    date_entered             TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX measurements_planned_process_id      ON measurements (planned_process_id);
CREATE INDEX measurements_measurement_standard_id ON measurements (measurement_standard_id);
CREATE INDEX measurements_value                   ON measurements (value);
CREATE INDEX measurements_value_max               ON measurements (value_max);
CREATE INDEX measurements_value_text              ON measurements (value_text);
CREATE INDEX measurements_value_object            ON measurements (value_object);

