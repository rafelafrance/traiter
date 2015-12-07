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

my $DEFINES = qr/
    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? )
        (?<range>   (?&quanity) (?: \s* (?: - | to ) \s* (?&quanity) )? (?! \s* - ))

        (?<shorthand_typos> mesurements | Measurementsnt | et )
        (?<len_shorthand_keys> (?&len_key) | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<wt_shorthand_keys>  (?&wt_key)  | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<shorthand_sep>   [: = , \/ \- ]+ )
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

        (?<len_key> total \s* length \s* in \s* mm
                  | snout \s* vent \s* lengths? (?: \s* in \s* mm )?
                  | length \s* in \s* millimeters
                  | head \s* body \s* length \s* in \s* millimeters
                  | (?: total | max | fork | mean )? \s* lengths?
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

#############################################################################################################
# Go thru the regular expressions in array order

my @TOTAL_LENGTH = (
    qr{ \b (?<key>   (?&len_key))        (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))?        \b $DEFINES },
    qr{ \b (?<key>   (?&key_units_req))  (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&len_units))         \b $DEFINES },
    qr{ \b (?<key>   (?&len_in_phrase))  \D+         (?<value> (?&range))      \s* (?<units> (?&len_units))?        \b $DEFINES },
    qr{ \b (?<value> (?&range))          \s*         (?<units> (?&len_units))? \s* (?<key>   (?&len_key_as_suffix)) \b $DEFINES },
    qr{ \b (?<key>   (?&len_shorthand_keys)) (?&key_sep) \s* (?<value> (?&quanity)) (?&len_shorthand) \b (?<next_word> [^\d\s]* ) $DEFINES },
    qr{ \b (?<prev_word> [^\d\s]* )                      \s* (?<value> (?&quanity)) (?&len_shorthand) \b (?<next_word> [^\d\s]* ) $DEFINES },
);

# This is for debugging/development only
my $SKIP_PREV_WORD = qr/
      date= | \?- | had | on | exhibit\( | cew | wing | nuttalli | nov
    | uam | incisors, | primaries | americana | carolinensis | mark
/;

my @BODY_MASS = (
    qr{ \b (?<key> (?&wt_key))         (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&wt_units))?        \b $DEFINES },
    qr{ \b (?<key> (?&key_units_req))  (?&key_sep) (?<value> (?&range))      \s* (?<units> (?&wt_units))         \b $DEFINES },
    qr{ \b (?<key> (?&wt_in_phrase))   \D+         (?<value> (?&range))      \s* (?<units> (?&wt_units))?        \b $DEFINES },
    qr{ \b (?<value> (?&range))        \s*         (?<units> (?&wt_units))?  \s* (?<key>   (?&wt_key_as_suffix)) \b $DEFINES },
    qr{ \b (?<key> (?&wt_shorthand_keys)) (?&key_sep) (?&wt_shorthand) (?<value> (?&quanity)) \b $DEFINES },
    qr{ \b (?<prev_word> [^\d\s]* )       \s*         (?&wt_shorthand) (?<value> (?&quanity)) \b $DEFINES },
);

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
    for my $regex ( @TOTAL_LENGTH ) {
        if ( $row->{$col} =~ $regex ) {
            my ($key, $value, $units, $prev_word) = ($+{key}, $+{value}, $+{units}, $+{prev_word});
            #say "$key, $value, $units";
            #return if ($key eq '' || $value eq '') && ($prev_word eq '' || $prev_word =~ $SKIP_PREV_WORD);
            my ($suffix) = ($key =~ m/( mm | millimeters ) $/);
            $units ||= $suffix;
            #say "$key, $value, $units";
            #say "$prev_word";
            #die if $key =~ m/in \s+ mm/;
            #die $prev_word . "\n" if (! $key || ! $value ) && $prev_word !~ /[;,.:]$/;
            return { key => $key, value => $value, units => $units };
        }
    }
    #die "$col: $row->{$col}\n" if $row->{$col} =~ m/\b(length|t\.?l\.?)\b/;
}

sub vto_body_mass {
    my ($row, $col) = @_;
    print "$col: $row->{$col}\n";
    my $i = 0;
    for my $regex ( @BODY_MASS ) {
        if ( $row->{$col} =~ $regex ) {
            say "matched: $i";
            my ($key, $value, $units, $prev_word) = ($+{key}, $+{value}, $+{units}, $+{prev_word});
            say "$key, $value, $units";
            #return if ($key eq '' || $value eq '') && ($prev_word eq '' || $prev_word =~ $SKIP_PREV_WORD);
            my ($suffix) = ($key =~ m/ ( grams ) $/);
            $units ||= $suffix;
            say "$key, $value, $units";
            say "$prev_word";
            die if $key =~ m/in \s+ mm/;
            die $prev_word . "\n" if (! $key || ! $value ) && $prev_word !~ /[;,.:]$/;
            return { key => $key, value => $value, units => $units };
        }
        $i++;
    }
    die "$col: $row->{$col}\n" if $row->{$col} =~ m/\b(weight|grams|w\.?t\.?)\b/ && $row->{$col} !~ /body/;
}

1;

