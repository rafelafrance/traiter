PRAGMA foreign_keys = ON;


CREATE TABLE sexes (sex TEXT PRIMARY KEY);
INSERT INTO sexes VALUES ('female'), ('male'), ('hermaphrodite');

CREATE TABLE quality_classes (quality_class TEXT PRIMARY KEY);
INSERT INTO quality_classes VALUES ('high'), ('medium'), ('low');

CREATE TABLE reference_types (reference_type TEXT PRIMARY KEY);
INSERT INTO reference_types VALUES ('journal'), ('book'), ('dataset');

CREATE TABLE "references" (
    reference_id    BLOB PRIMARY KEY,
    reference_type  TEXT REFERENCES reference_types (reference_type),
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
    reference_id          BLOB REFERENCES "references" (reference_id),
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
    higher_taxon_concept_id  BLOB REFERENCES taxon_concepts (taxon_concept_id),
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

CREATE TABLE entity_scopes (entity_scope TEXT PRIMARY KEY);
INSERT INTO entity_scopes VALUES ('individual'), ('population'), ('species'), ('clade');

CREATE TABLE entities (
    entity_id         BLOB PRIMARY KEY,
    taxon_concept_id  BLOB REFERENCES taxon_concepts (taxon_concept_id),
    entity_scope      TEXT REFERENCES entity_scopes  (entity_scope),
    sex               TEXT REFERENCES sexes          (sex),
    life_stage        TEXT,
    count             REAL,
    remarks           TEXT,
    entered_by        TEXT,
    date_entered      TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX entities_taxon_concept_id ON entities (taxon_concept_id);

CREATE TABLE evidence (
    evidence_id         BLOB PRIMARY KEY,
    entity_id           BLOB REFERENCES entities      (entity_id),
    dataset_id          BLOB REFERENCES datasets      (dataset_id),
    source_evidence_id  BLOB REFERENCES evidence      (evidence_id),
    reference_id        BLOB REFERENCES "references"  (reference_id),
    entity_scope        TEXT REFERENCES entity_scopes (entity_scope),
    specimen_id         BLOB,
    artifact_id         BLOB,
    remarks             TEXT,
    "count"             REAL,
    entered_by          TEXT,
    date_entered        TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX evidence_entity_id          ON evidence (entity_id);
CREATE INDEX evidence_dataset_id         ON evidence (dataset_id);
CREATE INDEX evidence_source_evidence_id ON evidence (source_evidence_id);
CREATE INDEX evidence_reference_id       ON evidence (reference_id);

CREATE TABLE associated_records (
    associated_record_id  BLOB PRIMARY KEY,
    evidence_id           BLOB REFERENCES evidence (evidence_id),
    uri                   TEXT,
    association_type      TEXT,
    external_id           TEXT,
    remarks               TEXT
);
CREATE INDEX associated_records_evidence_id ON associated_records (evidence_id);

CREATE TABLE planned_process_types (planned_process_type TEXT PRIMARY KEY);
INSERT INTO planned_process_types VALUES ('observation'), ('data_manipulation');

CREATE TABLE planned_processes (
    planned_process_id    BLOB PRIMARY KEY,
    reference_id          BLOB REFERENCES "references"          (reference_id),
    planned_process_type  TEXT REFERENCES planned_process_types (planned_process_type),
    date_time             TEXT,
    date_time_max         TEXT,
    remarks               TEXT,
    entered_by            TEXT,
    date_entered          TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX planned_processes_reference_id ON planned_processes (reference_id);

CREATE TABLE process_evidence (
    evidence_id               BLOB REFERENCES evidence          (evidence_id),
    planned_process_id        BLOB REFERENCES planned_processes (planned_process_id)
);
CREATE INDEX process_evidence_evidence_id        ON process_evidence (evidence_id);
CREATE INDEX process_evidence_planned_process_id ON process_evidence (planned_process_id);

CREATE TABLE traits (
    trait_id          BLOB PRIMARY KEY,
    reference_id      BLOB REFERENCES "references"   (reference_id),
    taxon_concept_id  BLOB REFERENCES taxon_concepts (taxon_concept_id),
    trait             TEXT,
    definition        TEXT,
    role              TEXT,
    sex               TEXT REFERENCES sexes (sex),
    life_stage        TEXT,
    uri               TEXT,
    remarks           TEXT
);
CREATE INDEX traits_reference_id     ON traits (reference_id);
CREATE INDEX traits_taxon_concept_id ON traits (taxon_concept_id);

CREATE TABLE value_types (value_type TEXT PRIMARY KEY);
INSERT INTO value_types VALUES ('numeric'), ('integer'), ('range'), ('vocabulary'), ('text'), ('object');

CREATE TABLE measurement_standards (
    measurement_standard_id  BLOB PRIMARY KEY,
    trait_id                 BLOB REFERENCES traits       (trait_id),
    reference_id             BLOB REFERENCES "references" (reference_id),
    title                    TEXT,
    value_type               TEXT REFERENCES value_types  (value_type),
    method                   TEXT,
    equation                 TEXT,
    units                    TEXT,
    quality                  TEXT REFERENCES quality_classes (quality),
    value_min                REAL,
    value_max                REAL,
    accuracy                 REAL,
    remarks                  TEXT
);
CREATE INDEX measurement_standards_reference_id ON measurement_standards (reference_id);
CREATE INDEX measurement_standards_trait_id     ON measurement_standards (trait_id);
CREATE INDEX measurement_standards_value_type   ON measurement_standards (value_type);

CREATE TABLE measurement_vocabulary (
    measurement_vocabulary_id  BLOB PRIMARY KEY,
    measurement_standard_id    BLOB REFERENCES measurement_standards (measurement_standard_id),
    word                       TEXT
);
CREATE INDEX measurement_vocabulary_standard_id ON measurement_vocabulary (measurement_standard_id);
CREATE INDEX measurement_vocabulary_word        ON measurement_vocabulary (word);

CREATE TABLE measurements (
    measurement_id           BLOB PRIMARY KEY,
    planned_process_id       BLOB REFERENCES planned_processes     (planned_process_id),
    measurement_standard_id  BLOB REFERENCES measurement_standards (measurement_standard_id),
    value                    REAL,
    value_min                REAL,
    value_max                REAL,
    value_accuracy           REAL,
    value_word               TEXT REFERENCES measurement_vocabulary (measurement_vocabulary_id),
    value_text               TEXT,
    value_object             BLOB,
    quality                  TEXT REFERENCES quality_classes (quality_class),
    remarks                  TEXT,
    entered_by               TEXT,
    date_entered             TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX measurements_planned_process_id      ON measurements (planned_process_id);
CREATE INDEX measurements_measurement_standard_id ON measurements (measurement_standard_id);
CREATE INDEX measurements_value                   ON measurements (value);
CREATE INDEX measurements_value_max               ON measurements (value_max);
CREATE INDEX measurements_value_text              ON measurements (value_text);
CREATE INDEX measurements_value_object            ON measurements (value_object);

