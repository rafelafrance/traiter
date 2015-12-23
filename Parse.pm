package Parse;

use strict;
use warnings FATAL => 'utf8';
use feature qw( switch say );
use open    qw( :std :utf8 );
use re      '/xims';

use JSON;
use Text::CSV_XS;
use Data::Dumper;

use parent 'Exporter';

our @EXPORT = qw(
    extract_sex
    extract_life_stage
    extract_total_length
    extract_body_mass
);

our @EXPORT_OK = qw(
    @SEX
    %SEX_BY_NAME
    @LIFE_STAGE
    %LIFE_STAGE_BY_NAME
    @TOTAL_LENGTH
    %TOTAL_LENGTH_BY_NAME
    @BODY_MASS
    %BODY_MASS_BY_NAME
);

#############################################################################
# Parse sex

our @SEX = (
    { name => 'sex_with_delimiter', as_array => 0,
      regex => qr/ \b (?<key> sex)
                      \W+
                      (?<value> [\w?.]+ (?: \s+ [\w?.]+ ){0,2} )
                      \s* (?: [:;,"] | $ )
                 /},
    { name => 'sex_without_delimiter', as_array => 0,
      regex => qr{ \b (?<key> sex) \W+ (?<value> \w+ ) }},
    { name => 'sex_unkeyed', as_array => 1,
      regex => qr{ \b (?<value> (?: males? | females? ) (?: \s* \? ) ) \b }},
);

our %SEX_BY_NAME = ();
$SEX_BY_NAME{$_->{name}} = $_ for @SEX;

#############################################################################
# Parse life stage

our @LIFE_STAGE = (
    { name => 'lifestage_with_delimiter',
      regex => qr/ \b (?<key> (?: life \s* stage | age (?: \s* class )? ) )
                      \W+
                      (?<value> [\w?.\/]+ (?: \s+ [\w?.\/]+){0,4} )
                      \s* (?: [:;,"] | $ )
                 /},
    { name => 'lifestage_without_delimiter',
      regex => qr/ \b (?<key> life \s* stage
                            | age \s* class
                            | age \s* in \s* (?: hour | day ) s?
                            | age
                      )
                      \W+
                      (?<value> \w+ (?: \s+ (?: year | recorded ) )? )
                 /},
    { name => 'lifestage_unkeyed',
      regex => qr{ (?<value> (?: after \s+ )?
                             (?: first | second | third | fourth | hatching )
                             \s+ year )
                 }},
);

our %LIFE_STAGE_BY_NAME = ();
$LIFE_STAGE_BY_NAME{$_->{name}} = $_ for @LIFE_STAGE;

#############################################################################
# Common regular subexpressions for parsing both total length and body mass

my $DEFINES = qr/
    (?(DEFINE)
        (?<number>   [\[\(]? \d+ (?: \. \d* )? [\]\)]? [\*]? )
        (?<quantity> (?&number) (?: \s* (?: - | to ) \s* (?&number) )? )

        (?<sep>      [:,\/\-\s] )
        (?<wt_sep>   [=\s]+ )
        (?<no_word>  (?: ^ | [;,:\{\[\(]+ ) \s* ["']? )
        (?<shorthand_typos>  mesurements | Measurementsnt )
        (?<all_len_keys> (?&total_len_key) | (?&svl_len_key) | (?&other_len_key) | (?&len_key_ambiguous)
                       | (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<all_wt_keys>  (?&total_wt_key)  | (?&other_wt_key) | (?&wt_key_word)
                      |  (?&key_units_req) | (?&shorthand_words) | (?&shorthand_typos))
        (?<len_shorthand>    (?: (?&sep) (?&number) ){3,} )
        (?<wt_shorthand>     (?: (?&number) (?&sep) ){3,} (?&number) (?&wt_sep) )
        (?<wt_shorthand_req> (?: (?&number) (?&sep) ){4,} )
        (?<shorthand_words> on \s* tag
                          | specimens?
                          | catalog
                          | measurements (?: \s+ \w+)*
                          | tag \s+ \d+ \s* =? (?: male | female)? \s* ,
                          | meas [.,]? (?: \s+ \w+ \. \w+ \. )?
        )
        (?<len_shorthand_euro> hb (?: (?&sep) (?&number) [a-z]* ){4,} )
        (?<wt_shorthand_euro>  (?&number) hb (?: (?&sep) (?&number) [a-z]* ){4,} = )

        (?<key_units_req> measurements? | body | total )
        (?<key_end>       \s* [^\w.\[\(]* \s* )
        (?<dash>          [\s\-]? )
        (?<dot>           \.? )
        (?<open>          [\(\[\{]? )
        (?<close>         [\)\]\}]? )

        (?<total_len_key> total  (?&dash) length (?&dash) in (?&dash) mm
                        | length (?&dash) in     (?&dash) millimeters
                        | (?: total | max | standard ) (?&dash) lengths?
        )
        (?<svl_len_key> snout  (?&dash) vent   (?&dash) lengths? (?: (?&dash) in (?&dash) mm )?
                      | s (?&dot) v (?&dot) l (?&dot)
                      | snout \s+ vent \s+ lengths?
        )
        (?<other_len_key> head  (?&dash) body (?&dash) length (?&dash) in (?&dash) millimeters
                        | (?: fork | mean | body ) (?&dash) lengths?
                        | t [o.]? l (?&dot) _?
        )
        (?<len_key_ambiguous> lengths? | tag )
        (?<len_key_abbrev>    t (?&dot) o? l (?&dot) )
        (?<len_key_suffix>    (?: in \s* )? (?&len_key_abbrev) )
        (?<len_in_phrase>     (?: total \s+ length | snout \s+ vent \s+ length ) s? )

        (?<len_units>        (?&len_units_word) | (?&len_units_abbrev) )
        (?<len_units_word>   (?: meter | millimeter | centimeter | foot | feet | inch e? ) s? )
        (?<len_units_abbrev> (?: [cm] (?&dot) m | in | ft ) (?&dot) s? )
        (?<len_foot>         (?: foot | feet | ft ) s? (?&dot) )
        (?<len_inch>         (?: inch e? | in )     s? (?&dot) )

        (?<total_wt_key> weightingrams | massingrams
                       | (?: body | full | observed | total ) (?&dot) \s* (?&wt_key_word)
        )
        (?<other_wt_key>    (?: dead | live ) (?&dot) \s* (?&wt_key_word) )
        (?<wt_key_word>     weights? | mass | w (?&dot) t s? (?&dot) )
        (?<wt_in_phrase>    total \s+ (?&wt_key_word) )
        (?<wt_units>        (?&wt_units_word) | (?&wt_units_abbrev) )
        (?<wt_units_word>   (?: gram | milligram | kilogram | pound | ounce ) s? )
        (?<wt_units_abbrev> (?: m (?&dot) g | k (?&dot) g | g[mr]? | lb | oz ) s? (?&dot) )
        (?<wt_pound>        (?: pound | lb ) s? (?&dot) )
        (?<wt_ounce>        (?: ounce | oz ) s? (?&dot))
    )
/;

#############################################################################
# Parse total length

our @TOTAL_LENGTH = (
    { name => 'en_len', default_units => '', default_key => '_english_', compound => 2,
      regex => qr{ \b (?<key> (?&all_len_keys))? (?&key_end)?
                      (?<value1> (?&quantity))    \s*
                      (?<units1> (?&len_foot))    \s*
                      (?<value2> (?&quantity))    \s*
                      (?<units2> (?&len_inch)) 
                      $DEFINES } },
    { name => 'total_len_key', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&total_len_key)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))?
                      $DEFINES } },
    { name => 'other_len_key', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&other_len_key)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))?
                      $DEFINES } },
    { name => 'key_units_req', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&key_units_req)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))
                      $DEFINES } },
    { name => 'len_in_phrase', default_units => '', default_key => '', compound => 0,
      regex => qr/ \b (?<key> (?&len_in_phrase)) \D{1,32}
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))?
                      $DEFINES / },
    { name => 'len_key_ambiguous_units', default_units => '', default_key => '', compound => 0,
      regex => qr{ (?&no_word)
                   (?<key> (?&len_key_ambiguous)) (?&key_end)
                   (?<value> (?&quantity)) \s*
                   (?<units> (?&len_units))
                   $DEFINES } },
    { name => 'len_key_abbrev', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&len_key_abbrev)) \s*
                      (?&open) \s* (?<units> (?&len_units)) \s* (?&close) \s*
                      (?<value> (?&quantity))
                      $DEFINES } },
    { name => 'len_key_suffix', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))? \s*
                      (?<key> (?&len_key_suffix))
                      $DEFINES } },
    { name => 'len_shorthand', default_units => '_mm_', default_key => '_shorthand_', compound => 0,
      regex => qr{ \b (?: (?<key> (?&all_len_keys)) (?&key_end) )?
                      (?<value> (?&number))
                      (?&len_shorthand)
                      $DEFINES } },
    { name => 'len_shorthand_euro', default_units => '_mm_', default_key => '_shorthand_', compound => 0,
      regex => qr{ \b (?: (?<key> (?&all_len_keys)) (?&key_end) )?
                      (?<value> (?&number))
                      (?&len_shorthand_euro)
                      $DEFINES } },
    { name => 'len_key_ambiguous', default_units => '', default_key => '', compound => 0,
      regex => qr{ (?&no_word)
                   (?<key> (?&len_key_ambiguous)) (?&key_end)
                   (?<value> (?&quantity))
                   $DEFINES } },
    { name => 'svl_len_key', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&svl_len_key)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&len_units))?
                      $DEFINES } },
);

our %TOTAL_LENGTH_BY_NAME = ();
$TOTAL_LENGTH_BY_NAME{$_->{name}} = $_ for @TOTAL_LENGTH;

#############################################################################
# Parse body mass

our @BODY_MASS = (
    { name => 'en_wt', default_units => '', default_key => '_english_', compound => 2,
      regex => qr{ \b (?<key> (?&all_wt_keys))? (?&key_end)?
                      (?<value1> (?&quantity))  \s*
                      (?<units1> (?&wt_pound))  \s*
                      (?<value2> (?&quantity))  \s*
                      (?<units2> (?&wt_ounce)) 
                      $DEFINES } },
    { name => 'total_wt_key', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&total_wt_key)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&wt_units))?
                      $DEFINES } },
    { name => 'other_wt_key', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&other_wt_key)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&wt_units))?
                      $DEFINES } },
    { name => 'key_units_req', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&key_units_req)) (?&key_end)
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&wt_units))
                      $DEFINES } },
    { name => 'wt_in_phrase', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&wt_in_phrase)) \D{1,32}
                      (?<value> (?&quantity)) \s*
                      (?<units> (?&wt_units))?
                      $DEFINES } },
    { name => 'wt_key_word', default_units => '', default_key => '', compound => 0,
      regex => qr{ \b (?<key> (?&wt_key_word)) \s*
                      (?&open) \s* (?<units> (?&wt_units)) \s* (?&close) \s*
                      (?<value> (?&quantity))
                      $DEFINES } },
    { name => 'wt_key_word_req', default_units => '', default_key => '', compound => 0,
      regex => qr{ (?<key> (?&wt_key_word)) (?&key_end)
                   (?<value> (?&quantity)) \s*
                   (?<units> (?&wt_units))
                   $DEFINES } },
    { name => 'wt_shorthand', default_units => '', default_key => '_shorthand_', compound => 0,
      regex => qr{ \b (?: (?<key> (?&all_wt_keys)) (?&key_end) )?
                      (?&wt_shorthand) \s*
                      (?<value> (?&number)) \s*
                      (?<units> (?&wt_units))?
                      $DEFINES } },
    { name => 'wt_shorthand_req', default_units => '', default_key => '_shorthand_', compound => 0,
      regex => qr{ \b (?: (?<key> (?&all_wt_keys)) (?&key_end) )?
                      (?&wt_shorthand_req) \s*
                      (?<value> (?&number)) \s*
                      (?<units> (?&wt_units))
                      $DEFINES } },
    { name => 'wt_shorthand_euro', default_units => '', default_key => '_shorthand_', compound => 0,
      regex => qr{ \b (?: (?<key> (?&all_wt_keys)) (?&key_end) )?
                      (?&wt_shorthand_euro) \s*
                      (?<value> (?&number)) \s*
                      (?<units> (?&wt_units))?
                      $DEFINES } },
    { name => 'wt_fa', default_units => '', default_key => '_shorthand_', compound => 0,
      regex => qr{ fa \d* - 
                   (?<value> (?&number)) \s*
                   (?<units> (?&wt_units))?
                   $DEFINES } },
    { name => 'wt_key_ambiguous', default_units => '', default_key => '', compound => 0,
      regex => qr{ (?<key> (?&wt_key_word)) (?&key_end)
                   (?<value> (?&quantity)) \s*
                   (?<units> (?&wt_units))?
                   $DEFINES } },
);

our %BODY_MASS_BY_NAME = ();
$BODY_MASS_BY_NAME{$_->{name}} = $_ for @BODY_MASS;

#############################################################################

sub extract_sex {
    my ($row, $col) = @_;
    for my $pattern ( @SEX ) {
        if ( $pattern->{as_array} ) {
            if ( my @matches = ($row->{$col} =~ /$pattern->{regex}/g) ) {
                #say $pattern->{name};
                return { key => '', value => \@matches };
            }
        } elsif ( $row->{$col} =~ $pattern->{regex} ) {
            #say $pattern->{name};
            my ($key, $value) = ($+{key}, $+{value});
            $value = '' if $value =~ /^ (?: and | was | is ) $/;
            return { key => $key, value => $value } if $value;
        }
    }
}

sub extract_life_stage {
    my ($row, $col) = @_;
    for my $pattern ( @LIFE_STAGE ) {
        if ( $row->{$col} =~ $pattern->{regex} ) {
            #say $pattern->{name};
            my ($key, $value) = ($+{key}, $+{value});
            $value = '' if $value =~ /^ (?: determination ) /;
            return { key => $key, value => $value } if $value;
        }
    }
}

sub extract_total_length {
    my ($row, $col) = @_;
    my ($key, $value, $units, $suffix);
    for my $pattern ( @TOTAL_LENGTH ) {
        if ( $row->{$col} =~ $pattern->{regex} ) {
            say '************************* ', $pattern->{name};
            if ($pattern->{compound} ) {
                ($key, $value, $units) = ($+{key}, [$+{value1}, $+{value2}], [$+{units1}, $+{units2}]);
            } else {
                ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
                ($suffix) = ($key =~ m/( mm | millimeters ) $/);
                $value //= '';
                $value =~ s/\s*$//;
            }
            return { key   => $key || $pattern->{default_key},
                     value => $value,
                     units => $units || $suffix || $pattern->{default_units} };
        }
    }
}

sub extract_body_mass {
    my ($row, $col) = @_;
    my ($key, $value, $units, $suffix);
    for my $pattern ( @BODY_MASS ) {
        if ( $row->{$col} =~ $pattern->{regex} ) {
            # say '************************* ', $pattern->{name};
            if ($pattern->{compound} ) {
                ($key, $value, $units) = ($+{key}, [$+{value1}, $+{value2}], [$+{units1}, $+{units2}]);
            } else {
                ($key, $value, $units) = ($+{key}, $+{value}, $+{units});
                ($suffix) = ($key =~ m/ ( grams ) $/);
                $value //= '';
                $value =~ s/\s*$//;
            }
            return { key   => $key || $pattern->{default_key},
                     value => $value,
                     units => $units || $suffix || $pattern->{default_units} };
        }
    }
}

1;

