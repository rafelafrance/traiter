#package VertNet::Parse;

use strict;
use warnings FATAL => 'utf8';
use feature qw( switch say );
use open    qw( :std :utf8 );
use re      '/xi';

use JSON;
use Text::CSV_XS;
use Data::Dumper;

my $input_file = $ARGV[0];
my $output_file = $input_file . '.csv'; # TODO Get from argv[1]

#############################################################################
# Pull sex out when there is a key=value pair

my $SEX_KEYED = qr{
    \b (?<key> sex) \b \W* (?<value> \w+ )
};

#----------------------------------------------------------------------------
# If the keyed version fails see if we can find unkeyed versions

my $SEX_UNKEYED = qr{
    \b (?<value> (?: males? | females? | m (?! \.) | f (?! \.) ) ) \b
};

#############################################################################
# Pull life stage out when there is a key=value pair

my $LIFE_STAGE_KEYED = qr{
    \b (?<key> life \s* stage
             | age \s* class
             | age \s* in \s* (?: hour | day ) s?
             | age
       )
       \W+
       (?<value> \w+ (?: \s+ (?: year | recorded ) )? )
};

#----------------------------------------------------------------------------
# If the keyed version fails see if we can find unkeyed versions

my $LIFE_STAGE_UNKEYED = qr{
  (?<value> (?: after \s+ )?
            (?: first | second | third | fourth | hatching )
            \s+ year
  )
};

#############################################################################
# Common regular subexpressions for parsing both total length and body mass

my $DEFINES = qr/
    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? )
        (?<range>   (?&quanity) (?: \s* (?: - | to ) \s* (?&quanity) )? (?! \s* - ))

        (?<shorthand_typos> mesurements | Measurementsnt | et )
        (?<len_shorthand_keys> (?&len_key) | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<wt_shorthand_keys>  (?&wt_key)  | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<shorthand_sep>   [ : = , \/ \- ]+ )
        (?<len_shorthand>   (?: (?&shorthand_sep) (?&quanity) ){3,} )
        (?<wt_shorthand>    (?: (?&quanity) (?&shorthand_sep) ){3,} )
        (?<shorthand_words> on \s* tag
                          | specimens?
                          | catalog (?&shorthand_sep)
                          | measurements (?: \s+ \w+)* \s* (?&shorthand_sep)
                          | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                          | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                          | [mf]
                          | \b (?: male | female ) \s* (?&shorthand_sep)
        )

        (?<key_units_req> measurements? )
        (?<key_sep>       \s* [^ \w . ]* \s* )
        (?<key_word_sep>  (?: \s | [ \- ])? )

        (?<len_key> total (?&key_word_sep) length (?&key_word_sep) in (?&key_word_sep) mm
                  | snout (?&key_word_sep) vent (?&key_word_sep) lengths? (?: \s* in \s* mm )?
                  | length (?&key_word_sep) in (?&key_word_sep) millimeters
                  | head (?&key_word_sep) body (?&key_word_sep) length (?&key_word_sep) in (?&key_word_sep) millimeters
                  | (?: total | max | fork | mean | standard )? (?&key_word_sep) lengths?
                  | tag
                  | t \.? l \.?
                  | s \.? v \.? l \.?
        )
        (?<len_key_as_suffix> (?: in )? t \.? l \.? )
        (?<len_in_phrase>     total \s+ lengths? | snout \s+ vent \s+ lengths? )
        (?<len_units>         (?&len_units_word) | (?&len_units_abbrev) )
        (?<len_units_word>    (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )
        (?<len_units_abbrev>  (?: [cm] \.? m | in | ft ) \.? s? )

        (?<wt_key> weightingrams
                 | (?: body | dead | full | live | observed )? \.? \s* weights?
                 | w \.? t s? \.?
        )
        (?<wt_key_as_suffix> (?: oz ))
        (?<wt_in_phrase>     (?: total \s+ wights? ))
        (?<wt_units>         (?: (?&wt_units_word) | (?&wt_units_abbrev) ))
        (?<wt_units_word>    (?: gram | milligram | kilogram | pound | ounce ) s? )
        (?<wt_units_abbrev>  (?: [mk]? \.? g | lb | oz ) \.? s? )
    )
/;

#############################################################################
# Go thru the total length regular expressions in array order

my @TOTAL_LENGTH = (
    qr{ \b (?<key>   (?&len_key))        (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))?        \b $DEFINES },
    qr{ \b (?<key>   (?&key_units_req))  (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))         \b $DEFINES },
    qr{ \b (?<key>   (?&len_in_phrase))  \D+         (?<value> (?&range))      \s* (?<units> (?&len_units))?        \b $DEFINES },
    qr{ \b (?<value> (?&range))          \s*         (?<units> (?&len_units))? \s* (?<key>   (?&len_key_as_suffix)) \b $DEFINES },
    qr{ \b (?<key>   (?&len_shorthand_keys)) (?&key_sep) (?<value> (?&quanity)) (?&len_shorthand) \b $DEFINES },
    qr{ \b                                               (?<value> (?&quanity)) (?&len_shorthand) \b $DEFINES },
);

#############################################################################
# Go thru the body mass regular expressions in array order

my @BODY_MASS = (
    qr{ \b (?<key> (?&wt_key))         (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&wt_units))?        \b $DEFINES },
    qr{ \b (?<key> (?&key_units_req))  (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&wt_units))         \b $DEFINES },
    qr{ \b (?<key> (?&wt_in_phrase))   \D+         (?<value> (?&range))      \s* (?<units> (?&wt_units))?        \b $DEFINES },
    qr{ \b (?<value> (?&range))        \s*         (?<units> (?&wt_units))?  \s* (?<key>   (?&wt_key_as_suffix)) \b $DEFINES },
    qr{ \b (?<key> (?&wt_shorthand_keys)) (?&key_sep) (?&wt_shorthand) (?<value> (?&quanity)) \b $DEFINES },
    qr{ \b                                            (?&wt_shorthand) (?<value> (?&quanity)) \b $DEFINES },
);

#############################################################################
# So we can loop thru the parsing functions

my %new_columns = (
    dwc_sex          => \&dwc_sex,
    dwc_life_stage   => \&dwc_life_stage,
    vto_total_length => \&vto_total_length,
    vto_body_mass    => \&vto_body_mass,
);

#----------------------------------------------------------------------------
# Columns being searched

my @scan_columns = qw( dynamicproperties occurrenceremarks fieldnotes );

#############################################################################

MAIN: {
    my $csv = Text::CSV_XS->new ({ binary => 1, auto_diag => 1 });
    open my $fh_in,  '<', $input_file  or die $!;
    open my $fh_out, '>', $output_file or die $!;

    my $column_names = $csv->getline($fh_in);
    push @$column_names, sort keys %new_columns;
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
    if ( my @matches = ($row->{$col} =~ $LIFE_STAGE_UNKEYED) ) {
        return { key => '', value => \@matches };
    }
}

sub vto_total_length {
    my ($row, $col) = @_;
    for my $regex ( @TOTAL_LENGTH ) {
        if ( $row->{$col} =~ $regex ) {
            my ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
            my ($suffix) = ($key =~ m/( mm | millimeters ) $/);
            return { key => $key || '', value => $value // '', units => $units || $suffix || '' };
        }
    }
}

sub vto_body_mass {
    my ($row, $col) = @_;
    for my $regex ( @BODY_MASS ) {
        if ( $row->{$col} =~ $regex ) {
            my ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
            my ($suffix) = ($key =~ m/ ( grams ) $/);
            return { key => $key || '', value => $value // '', units => $units || $suffix || '' };
        }
    }
}

1;

