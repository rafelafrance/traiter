package VertNet::Parse;

use strict;
use warnings FATAL => 'utf8';
use feature qw( switch say );
use open    qw( :std :utf8 );
use re      '/xi';

use JSON;
use Text::CSV_XS;
use Data::Dumper;

my $input_file = $ARGV[0];
my $output_file = $input_file . '.csv';

# Pull sex out when there is a key=value pair
my $SEX_KEYED = qr{
    \b (?<key> sex|gender ) \b
    \W*
    (?<value> \w+ )
};

# If the keyed version fails see if we can find unkeyed versions
my $SEX_UNKEYED = qr{
    \b (?<value> (?:   males?
                     | females? 
                     | m (?&no_trailing_period)
                     | f (?&no_trailing_period)
       )) \b
    (?(DEFINE)
        (?<no_trailing_period> (?! \.) )
    )
};


# Pull life stage out when there is a key=value pair
my $LIFE_STAGE_KEYED = qr{
    \b (?<key> life \s* stage | age (?: class )? )
    \W*
    (?<value> \w+ )
};

# If the keyed version fails see if we can find unkeyed versions
my $LIFE_STAGE_UNKEYED = qr{
  (?<value> (?: after \s+ )?
            (?: first | second | third | fourth | hatching ) \s+ \w+)
};

my $TOTAL_LENGTH = qr/
    \b (?: (?<key> (?&shorthand_keys)) (?&key_sep) \s* (?<value> (?&quanity)) (?&shorthand)
         | (?<key> (?&len_key))        (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))?
         | (?<key> (?&key_units_req))  (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))
         | (?<key> (?&len_in_phrase))  \D+         (?<value> (?&range))      \s* (?<units> (?&len_units))?
         | (?<value> (?&range))        \s*         (?<units> (?&len_units))? \s* (?<key>   (?&len_key_as_suffix))
         | (?<prev_word> [^\d\s]* )    \s*         (?<value>(?&quanity))     (?&shorthand)
       )
    \b

    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? )
        (?<range>   (?&quanity) (?: \s* (?: - | to ) \s* (?&quanity) )? (?! \s* - ))
        (?<len_key> totallengthinmm
                  | snoutventlengthinmm
                  | lengthinmillimeters
                  | headbodylengthinmillimeters
                  | total \s* lengths?
                  | snout \s* vent \s* lengths?
                  | max \s* length
                  | fork \s* length
                  | lengths?
                  | tag
                  | s \.? v \.? l \.?
                  | (?&len_units_abbrev)? (?&tl_abbrev) (?&len_units_abbrev)?
        )
        (?<shorthand_sep>   [:=,-]?)
        (?<shorthand_words> on \s* tag
                          | specimens?
                          | catalog (?&shorthand_sep)
                          | measurements (?: \s+ \w+)* \s* (?&shorthand_sep)
                          | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                          | et
                          | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                          | [mf]
                          | \b (?: male | female ) \s* (?&shorthand_sep)
        )
        (?<shorthand_typos>   mesurements | Measurementsnt )
        (?<shorthand_keys>    (?&len_key) | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<shorthand>         (?: [=\/-] (?&quanity)){3,} )
        (?<len_key_as_suffix> (?: in )? (?&tl_abbrev) )
        (?<key_units_req>     measurements? )
        (?<len_in_phrase>     (?: total \s+ lengths? | snout \s+ vent \s+ lengths? ))
        (?<key_sep>           [^ \w . ]* )
        (?<tl_abbrev>         t \.? l \.? \s* [_-]? )
        (?<len_units>         (?: (?&len_units_word) | (?&len_units_abbrev) ))
        (?<len_units_word>    (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )
        (?<len_units_abbrev>  (?: m \.? m | c \.? m | in | ft ) \.? s? )
    )
/;

# This is for debugging/development only
my $SKIP_PREV_WORD = qr/
      date= | \?- | had | on | exhibit\( | cew | wing | nuttalli | nov
    | uam | incisors, | primaries | americana | carolinensis | mark
/;

my $BODY_MASS = qr/
    \b (?: (?<key> (?&shorthand_keys)) (?&key_sep) \s* (?<value> (?&quanity)) (?&shorthand)
         | (?<key> (?&len_key))           (?&key_sep) (?<value> (?&range))       \s* (?<units> (?&len_units))?
         | (?<key> (?&key_units_req)) (?&key_sep) (?<value> (?&range))       \s* (?<units> (?&len_units))
         | (?<key> (?&len_in_phrase))     \D+         (?<value> (?&range))       \s* (?<units> (?&len_units))?
         | (?<value> (?&range))           \s*         (?<units> (?&len_units))?  \s* (?<key>   (?&len_key_as_suffix))
         | (?<prev_word> [^\d\s]* ) \s* (?<value>(?&quanity)) (?&shorthand)
       )
    \b

    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? )
        (?<range>   (?&quanity) (?: \s* (?: - | to ) \s* (?&quanity) )? (?! \s* - ))
        (?<len_key> weightingrams
                  | snoutventlengthinmm
                  | lengthinmillimeters
                  | headbodylengthinmillimeters
                  | total \s* lengths?
                  | snout \s* vent \s* lengths?
                  | max \s* length
                  | fork \s* length
                  | lengths?
                  | tag
                  | s \.? v \.? l \.?
                  | (?&len_units_abbrev)? (?&tl_abbrev) (?&len_units_abbrev)?
        )
        (?<shorthand_sep>   [:=,-]?)
        (?<shorthand_words> on \s* tag
                          | specimens?
                          | catalog (?&shorthand_sep)
                          | measurements (?: \s+ \w+)* \s* (?&shorthand_sep)
                          | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                          | et
                          | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                          | [mf]
                          | \b (?: male | female ) \s* (?&shorthand_sep)
        )
        (?<shorthand_typos>   mesurements | Measurementsnt )
        (?<shorthand_keys>    (?&len_key) | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<shorthand>         (?: [=\/-] (?&quanity)){3,} )
        (?<len_key_as_suffix> (?: in )? (?&tl_abbrev) )
        (?<key_units_req>     measurements? )
        (?<len_in_phrase>     (?: total \s+ lengths? | snout \s+ vent \s+ lengths? ))
        (?<key_sep>           [^ \w . ]* )
        (?<tl_abbrev>         t \.? l \.? \s* [_-]? )
        (?<len_units>         (?: (?&len_units_word) | (?&len_units_abbrev) ))
        (?<len_units_word>    (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )
        (?<len_units_abbrev>  (?: m \.? m | c \.? m | in | ft ) \.? s? )
    )
/;

# So we can loop thru the parsing functions
my %new_columns = (
    dwc_sex          => \&dwc_sex,
    dwc_life_stage   => \&dwc_life_stage,
    vto_total_length => \&vto_total_length,
    vto_body_mass    => \&vto_body_mass,
);

# Columns being searched
my @scan_columns = qw( dynamicproperties occurrenceremarks fieldnotes );

MAIN: {
    my $csv = Text::CSV_XS->new ({ binary => 1, auto_diag => 1 });
    open my $fh_in,  '<', $input_file  or die $!;
    open my $fh_out, '>', $output_file or die $!;

    my $column_names = $csv->getline($fh_in);
    push @$column_names, keys %new_columns;
    $csv->say($fh_out, $column_names);
    $csv->column_names( @$column_names );

    while ( my $row = $csv->getline_hr($fh_in) ) {
        say $csv->record_number();
        for my $new_col ( keys %new_columns ) {
            my $new_value = {};
            for my $scan_col ( @scan_columns ) {
                if ($row->{$scan_col} ) {
                    my $parsed = &{$new_columns{$new_col}}( $row, $scan_col );
                    $new_value->{$scan_col} = $parsed if $parsed;
                }
            }
            $row->{$new_col} = to_json( $new_value ) if keys %$new_value;
        }
        $csv->print_hr($fh_out, $row);
        print $fh_out "\n";
    }
}

sub dwc_sex {
    my ($row, $col) = @_;
    if ( $row->{$col} =~ $SEX_KEYED ) {
        return { key => $+{key}, value => $+{value} };
    }
    if ( my @matches = ($row->{$col} =~ /$SEX_UNKEYED/g) ) {
        return { key => '', value => \@matches };
    }
}

sub dwc_life_stage {
    my ($row, $col) = @_;
    if ( $row->{$col} =~ $LIFE_STAGE_KEYED ) {
        return { key => $+{key}, value => $+{value} };
    }
    return { key => $+{key}, value => $+{value} };
}

sub vto_total_length {
    my ($row, $col) = @_;
    #print "$col: $row->{$col}\n";
    if ( $row->{$col} =~ $TOTAL_LENGTH ) {
        my ($key, $value, $units, $prev_word) = ($+{key}, $+{value}, $+{units}, $+{prev_word});
        #return if ($key eq '' || $value eq '') && ($prev_word eq '' || $prev_word =~ $SKIP_PREV_WORD);
        my ($suffix) = ($key =~ m/(mm|millimeters)$/i);
        $units ||= $suffix;
        #say "$key, $value, $units";
        #say "$prev_word";
        #die $prev_word . "\n" if (! $key || ! $value ) && $prev_word !~ /[;,.:]$/;
        return { key => $key, value => $value, units => $units };
    }
}

sub vto_body_mass {
    # my ($row, $col) = @_;
}

1;

