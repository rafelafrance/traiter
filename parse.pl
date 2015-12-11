use strict;
use feature qw( switch say );

use JSON;
use Text::CSV_XS;
use Data::Dumper;

use Parse;

my $input_file = $ARGV[0];
my $output_file = $input_file . '.csv'; # TODO Get from argv[1]

#############################################################################
# So we can loop thru the parsing functions

my %new_columns = (
    dwc_sex          => \&Parse::dwc_sex,
    dwc_life_stage   => \&Parse::dwc_life_stage,
    vto_total_length => \&Parse::vto_total_length,
    vto_body_mass    => \&Parse::vto_body_mass,
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

