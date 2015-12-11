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
        (?<number>   [ \[ \( ]? \d+ (?: \. \d* )? [ \] \) ]? [ *]? )
        (?<quantity> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? (?! \s* (?&shorthand_sep) ))

        (?<shorthand_sep>   [ : = , \/ \- ]+ )
        (?<shorthand_typos> mesurements | Measurementsnt | et )
        (?<len_shorthand_keys> (?&total_len_key) | (?&svl_len_key) | (?&other_len_key) | (?&len_key_last)
                             | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<wt_shorthand_keys> (?&total_wt_key) | (?&other_wt_key) | (?&wt_key_word) | (?&key_units_req)
                            | (?&shorthand_words) | (?&shorthand_typos))
        (?<len_shorthand>   (?: (?&shorthand_sep) (?&number) ){3,} )
        (?<wt_shorthand>    (?: (?&number) (?&shorthand_sep) ){4,} )
        (?<shorthand_words> on \s* tag
                          | specimens?
                          | catalog (?&shorthand_sep)
                          | measurements (?: \s+ \w+)* \s* (?&shorthand_sep)
                          | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                          | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
                          | [mf]
                          | \b (?: male | female ) \s* (?&shorthand_sep)
        )
        (?<len_shorthand_euro> hb (?: (?&shorthand_sep) (?&number) [a-z]* ){3,} )
        (?<wt_shorthand_euro>  (?&number) hb (?: (?&shorthand_sep) (?&number) [a-z]* ){3,} = )

        (?<key_units_req> measurements? )
        (?<key_end>       \s* [^ \w . ]* \s* )
        (?<dash>          (?: \s | [ \- ])? )
        (?<dot>           \.? )
        (?<open>          [ \( \[ \{ ]? )
        (?<close>         [ \) \] \} ]? )

        (?<total_len_key> total  (?&dash) length (?&dash) in (?&dash) mm
                        | length (?&dash) in     (?&dash) millimeters
                        | (?: total | max | standard ) (?&dash) lengths?
                        | t [ o . ]? l (?&dot)
        )
        (?<svl_len_key> snout  (?&dash) vent   (?&dash) lengths? (?: (?&dash) in (?&dash) mm )?
                      | s (?&dot) v (?&dot) l (?&dot)
                      | snout \s+ vent \s+ lengths?
        )
        (?<other_len_key> head  (?&dash) body (?&dash) length (?&dash) in (?&dash) millimeters
                        | (?: fork | mean | body ) (?&dash) lengths?
        )
        (?<len_key_last>   (?<![ \- . ] ) \b (?: lengths? | tag ) \b )
        (?<len_key_abbrev> t (?&dot) o? l (?&dot) )
        (?<len_key_suffix> (?: in \s* )? (?&len_key_abbrev) )
        (?<len_in_phrase>  total \s+ lengths? | snout \s+ vent \s+ lengths? )

        (?<len_units>        (?&len_units_word) | (?&len_units_abbrev) )
        (?<len_units_word>   (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )
        (?<len_units_abbrev> (?: [cm] (?&dot) m | in | ft ) (?&dot) s? )

        (?<total_wt_key> weightingrams | massingrams |
                       | (?: body | full | observed | total ) (?&dot) \s* (?&wt_key_word)
        )
        (?<other_wt_key>    (?: dead | live ) (?&dot) \s* (?&wt_key_word) )
        (?<wt_key_word>    weights? | mass | w (?&dot) t s? (?&dot) )
        (?<wt_in_phrase>    total \s+ (?&wt_key_word) )
        (?<wt_units>        (?&wt_units_word) | (?&wt_units_abbrev) )
        (?<wt_units_word>   (?: gram | milligram | kilogram | pound | ounce ) s? )
        (?<wt_units_abbrev> (?: m (?&dot) g | k (?&dot) g | g | lb | oz ) (?&dot) s? )
    )
/;

#############################################################################
# Go thru the total length regular expressions in array order

my @TOTAL_LENGTH = (
    { default_units => '',
      regex => qr{ \b (?<key>   (?&total_len_key))  (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&len_units))?     \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key>   (?&svl_len_key))    (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&len_units))?     \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key>   (?&other_len_key))  (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&len_units))?     \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key>   (?&key_units_req))  (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&len_units))      \b $DEFINES } },
    { default_units => ''
      regex => qr{ \b (?<key>   (?&len_in_phrase))  \D+         (?<value> (?&quantity))   \s* (?<units> (?&len_units))?     \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key>   (?&len_key_abbrev)) \s* (?&open) \s* (?<units> (?&len_units)) \s* (?&close) \s* (?<value> (?&quantity)) \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<value> (?&quantity))       \s*         (?<units> (?&len_units))? \s* (?<key>   (?&len_key_suffix)) \b $DEFINES } },
    { default_units => 'mm',
      regex => qr{ \b (?<key>   (?&len_shorthand_keys)) (?&key_end) (?<value> (?&number)) (?&len_shorthand)      \b $DEFINES } },
    { default_units => 'mm',
      regex => qr{ \b                                               (?<value> (?&number)) (?&len_shorthand)      \b $DEFINES } },
    { default_units => 'mm',
      regex => qr{ \b                                               (?<value> (?&number)) (?&len_shorthand_euro) \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key>   (?&len_key_last))   (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&len_units))?        \b $DEFINES } },
);

#############################################################################
# Go thru the body mass regular expressions in array order

my @BODY_MASS = (
    { default_units => '',
      regex => qr{ \b (?<key> (?&total_wt_key))  (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&other_wt_key))  (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&key_units_req)) (?&key_end) (?<value> (?&quantity))   \s* (?<units> (?&wt_units))  \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&wt_in_phrase))  \D+         (?<value> (?&quantity))   \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&wt_key_word)) \s* (?&open) \s* (?<units> (?&wt_units)) \s* (?&close) \s* (?<value> (?&quantity)) \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&wt_shorthand_keys)) (?&key_end) (?&wt_shorthand)      \s* (?<value> (?&number)) \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b                                            (?&wt_shorthand)      \s* (?<value> (?&number)) \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b                                            (?&wt_shorthand_euro) \s* (?<value> (?&number)) \s* (?<units> (?&wt_units))? \b $DEFINES } },
    { default_units => '',
      regex => qr{ \b (?<key> (?&wt_key_word))  (?&key_end) (?<value> (?&quantity))    \s* (?<units> (?&wt_units))? \b $DEFINES } },
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
    for my $pattern ( @TOTAL_LENGTH ) {
        if ( $row->{$col} =~ $pattern->{regex} ) {
            my ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
            my ($suffix) = ($key =~ m/( mm | millimeters ) $/);
            return { key => $key || '',
                     value => $value // '',
                     units => $units || $suffix || $pattern->{default_units} || '' };
        }
    }
}

sub vto_body_mass {
    my ($row, $col) = @_;
    for my $pattern ( @BODY_MASS ) {
        if ( $row->{$col} =~ $pattern->{regex} ) {
            my ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
            my ($suffix) = ($key =~ m/ ( grams ) $/);
            return { key => $key || '',
                     value => $value // '',
                     units => $units || $suffix || $pattern->{default_units} || '' };
        }
    }
}

1;

