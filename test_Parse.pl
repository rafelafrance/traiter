use feature qw( switch say );
use Test::More;
use Parse qw(
    extract_sex
    extract_life_stage
    extract_total_length
    extract_body_mass
);

my ($test, $parsed);

sub setup {
    my $tc = shift;
    $name = substr $tc, 0, 20;
    return { test => $tc };
}

$test = setup('"{"measurements":"308-190-45-20" }"');
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '308');
is($parsed->{units}, '_mm_');

$test = setup( '308-190-45-20' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '308');
is($parsed->{units}, '_mm_');

$test = setup( '{"measurements":"143-63-20-17=13 g" }' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '143');
is($parsed->{units}, '_mm_');
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '13');
is($parsed->{units}, 'g');

$test = setup( '143-63-20-17=13' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '143');
is($parsed->{units}, '_mm_');
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '13');
is($parsed->{units}, '');

$test = setup( 'reproductive data: Testes descended -10x7 mm; sex: male; unformatted measurements: 181-75-21-18=22 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '22');
is($parsed->{units}, 'g');

$test = setup( '{ "massInGrams"="20.1" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'massInGrams');
is($parsed->{value}, '20.1');
is($parsed->{units}, 'Grams');

$test = setup( 'snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '111');
is($parsed->{units}, 'mm');

$test = setup( 'unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18; ; total length=230 mm; tail length=115 mm;' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '230');
is($parsed->{units}, 'mm');

$test = setup( '** Body length =345 cm; Blubber=1 cm ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Body length');
is($parsed->{value}, '345');
is($parsed->{units}, 'cm');

$test = setup( '762-292-121-76 2435.0g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '2435.0');
is($parsed->{units}, 'g');

$test = setup( 'TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'Weight');
is($parsed->{value}, '0.77');
is($parsed->{units}, 'g');
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '44');
is($parsed->{units}, 'mm');

$test = setup( 'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '62');
is($parsed->{units}, 'g');

#$test = setup( 'SVL 550 mm, tail 125 mm, 47.0 gm.' );
#$parsed = extract_body_mass( $test, 'test');
#is($parsed->{key},   '');
#is($parsed->{value}, '47.0');
#is($parsed->{units}, 'gm');

$test = setup( 'body mass=20 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'body mass');
is($parsed->{value}, '20');
is($parsed->{units}, 'g');

$test = setup( 'weight=81.00 g; sex=female ? ; age=u ad.' );
$parsed = extract_sex( $test, 'test');
is($parsed->{key},   'sex');
is($parsed->{value}, 'female ?');
$parsed = extract_life_stage( $test, 'test');
is($parsed->{key},   'age');
is($parsed->{value}, 'u ad.');

$test = setup( 't.l.= 2 feet 3.1 - 4.5 inches ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   't.l.');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'feet');
is($parsed->{units}->[1], 'inches');

$test = setup( '2 ft. 3.1 - 4.5 in. ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '_english_');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'ft.');
is($parsed->{units}->[1], 'in.');

$test = setup( 'total length= 2 ft.' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '2');
is($parsed->{units}, 'ft.');

$test = setup( '2 lbs. 3.1 - 4.5 oz ' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_english_');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'lbs.');
is($parsed->{units}->[1], 'oz');

$test = setup( '{"totalLengthInMM":"x", "earLengthInMM":"20", "weight":"[139.5] g" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight');
is($parsed->{value}, '[139.5]');
is($parsed->{units}, 'g');

$test = setup( '{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", "molt":"No molt", "stomach contents":"Not recorded", "weight":"94 gr."' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight');
is($parsed->{value}, '94');
is($parsed->{units}, 'gr.');

$test = setup( 'AJR-32   186-102-23-15  15.0g' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '186');
is($parsed->{units}, '_mm_');

$test = setup( 'sex=unknown ; crown-rump length=8 mm' );
$parsed = extract_sex( $test, 'test');
is($parsed->{key},   'sex');
is($parsed->{value}, 'unknown');

$test = setup( 'sex=unknown ; crown-rump length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed, '');

$test = setup( 'length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length');
is($parsed->{value}, '8');
is($parsed->{units}, 'mm');

$test = setup( 'another; length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length');
is($parsed->{value}, '8');
is($parsed->{units}, 'mm');

$test = setup( 'another; TL_120, noise' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL_');
is($parsed->{value}, '120');
is($parsed->{units}, '');

$test = setup( 'another; TL - 101.3mm, noise' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '101.3');
is($parsed->{units}, 'mm');

$test = setup( 'before; TL153, after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '153');
is($parsed->{units}, '');

$test = setup( 'before; Total length in catalog and specimen tag as 117, after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Total length');
is($parsed->{value}, '117');
is($parsed->{units}, '');

$test = setup( 'before Snout vent lengths range from 16 to 23 mm. after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Snout vent lengths');
is($parsed->{value}, '16 to 23');
is($parsed->{units}, 'mm.');

$test = setup( 'Size=13 cm TL' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '13');
is($parsed->{units}, 'cm');

$test = setup( 'det_comments:31.5-58.3inTL' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '31.5-58.3');
is($parsed->{units}, 'in');

$test = setup( 'SVL52mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'SVL');
is($parsed->{value}, '52');
is($parsed->{units}, 'mm');

$test = setup( 'snout-vent length=221 mm; total length=257 mm; tail length=36 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '257');
is($parsed->{units}, 'mm');

$test = setup( 'SVL 209 mm, total 272 mm, 4.4 g.' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total');
is($parsed->{value}, '272');
is($parsed->{units}, 'mm');

$test = setup( 'Note in catalog: 83-0-17-23-fa64-35g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '35');
is($parsed->{units}, 'g');

$test = setup( '{"measurements":"20.2g, SVL 89.13mm" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '20.2');
is($parsed->{units}, 'g');

$test = setup( 'Body: 15 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'Body');
is($parsed->{value}, '15');
is($parsed->{units}, 'g');

$test = setup( '82-00-15-21-tr7-fa63-41g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '_shorthand_');
is($parsed->{value}, '41');
is($parsed->{units}, 'g');

$test = setup( 'left gonad length=10 mm; right gonad length=10 mm;' );
$parsed = extract_total_length( $test, 'test');
is($parsed, '');

$test = setup( 'Respective sex and msmt. in mm' );
$parsed = extract_sex( $test, 'test');
is($parsed, '');

$test = setup( 'sex=unknown ; age class=adult/juvenile' );
$parsed = extract_life_stage( $test, 'test');
is($parsed->{key},   'age class');
is($parsed->{value}, 'adult/juvenile');

$test = setup( 'weight=5.4 g; unformatted measurements=77-30-7-12=5.4' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight');
is($parsed->{value}, '5.4');
is($parsed->{units}, 'g');

$test = setup( 'unformatted measurements=77-30-7-12=5.4; weight=5.4;' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '5.4');
is($parsed->{units}, '');

$test = setup( '{"time collected":"0712-0900", "length":"12.0" }' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length');
is($parsed->{value}, '12.0');
is($parsed->{units}, '');

$test = setup( '{"length":"20-29" }' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length');
is($parsed->{value}, '20-29');
is($parsed->{units}, '');

$test = setup( '{"time collected":"1030", "water depth":"1-8", "bottom":"abrupt lava cliff dropping off to sand at 45 ft.", "length":"119-137" }' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length');
is($parsed->{value}, '119-137');
is($parsed->{units}, '');

$test = setup( '{"totalLengthInMM":"270-165-18-22-31", ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'totalLengthInMM');
is($parsed->{value}, '270');
is($parsed->{units}, 'MM');
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'totalLengthInMM');
is($parsed->{value}, '31');
is($parsed->{units}, '');


done_testing();

