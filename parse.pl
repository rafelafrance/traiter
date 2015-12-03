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
                     | m (?! \.)    # Take a lone M but not an abbreviation
                     | f (?! \.)    # Take a lone F but not an abbreviation
       )) \b
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

my $TOTAL_LENGTH_KEYS = qr{
    length | t \.? \s* l \.? | measure
};

my $TOTAL_LENGTH = qr{
    \b (?:
        # Match with the label in the prefix
        (?<key> (?&keys) )
            \D*
            (?<value> (?&quanity) )
            \s*
            (?<units> (?&lengths) )?
        # Match with the label in the suffix
    ) \b

    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? ) # Simple decimals should work OK
        (?<keys> totalLengthInMM
                | measurements  # Measurements is ambiguous and needs to be last
        )
        (?<lengths> (?: mm | m | cm | meter | millimeter | centimeter |
                        in | foot | feet | inche? ) s?
        )
    )
};

my $BODY_MASS = qr{
    \b (?:
        # Match with the label in the prefix
        (?<key> (?&keys) )
            \D*
            (?<value> (?&quanity) )
            \s*
            (?<units> (?&masses) )?
        # Match with the label in the suffix
    ) \b

    (?(DEFINE)
        (?<quanity> \d+ (?: \. \d* )? ) # Simple decimals should work OK
        (?<keys>  weightInGrams
                | measurements  # Measurements is ambiguous and needs to be last
        )
        (?<masses> (?: g | gram | mg | milligram | kg | kilogram |
                       oz | ounce | pound | lb ) s? )
    )
};

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
                my $parsed = &{$new_columns{$new_col}}( $row, $scan_col );
                $new_value->{$scan_col} = $parsed if $parsed;
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
    if ( $row->{$col} =~ $TOTAL_LENGTH ) {
        return { key => $+{key}, value => $+{value}, units => $+{units} };
    }
    die $row->{$col} . "\n" if $row->{$col} =~ $TOTAL_LENGTH_KEYS;
}

sub vto_body_mass {
    # my ($row, $col) = @_;
}

1;

