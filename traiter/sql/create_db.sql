drop table if exists metadata;
create table metadata (
    label text primary key,
    datum text
);
insert into metadata (label, datum) values ('traiter', 'true');
insert into metadata (label, datum) values ('version', '0.8');


drop table if exists docs;
create table docs (
    doc_id    text primary key,
    path      text,
    loaded    text,
    edited    text,
    extracted text,
    method    text,
    raw       text,
    edits     text
);


drop table if exists scripts;
create table scripts (
    script_id text primary key,
    action    text
);
insert into scripts (script_id, action) values ('sed s/¼/=/', 'sed s/¼/=/');
insert into scripts (script_id, action) values (
    'remove page numbers',
    'sed -r /^[[:space:]]*[[:digit:]]{1,4}[[:space:]]*$/d');


drop table if exists pipes;
create table pipes (
    pipe_id   text primary key,
    script_id text,
    order_    integer
);


drop table if exists traits;
create table traits (
    trait_id integer primary key,
    doc_id   text,
    trait    text,
    start    integer,
    end_     integer
);
create index traits_doc_id on traits (doc_id);
create index traits_trait on traits (trait);
create index traits_pos on traits (start, end_);


drop table if exists props;
create table props (
    prop_id   integer primary key,
    trait_id  integer,
    name      text,
    val       blob
);
create index props_trait_id on props (trait_id);
create index props_name on props (name);
create index props_val_int   on props (cast(val as integer));
create index props_val_text  on props (cast(val as text));
create index props_val_real  on props (cast(val as real));
