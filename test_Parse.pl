use feature qw( switch say );
use Test::More;
use Parse qw(
    extract_sex
    extract_life_stage
    extract_total_length
    extract_body_mass
);

my ($test, $parsed, $name);

sub setup {
    my $tc = shift;
    $name = substr $tc, 0, 20;
    return $name, { test => $tc };
}

($name, $test) = setup('"{"measurements":"308-190-45-20" }"');
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '308', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( '308-190-45-20' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '308', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( '{"measurements":"143-63-20-17=13 g" }' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '143', $name);
is($parsed->{units}, 'mm', $name);
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '13', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( '143-63-20-17=13' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '143', $name);
is($parsed->{units}, 'mm', $name);
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '13', $name);
is($parsed->{units}, '', $name);

($name, $test) = setup( 'reproductive data: Testes descended -10x7 mm; sex: male; unformatted measurements: 181-75-21-18=22 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '22', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( '{ "massInGrams"="20.1" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'massInGrams', $name);
is($parsed->{value}, '20.1', $name);
is($parsed->{units}, 'Grams', $name);

($name, $test) = setup( 'snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length', $name);
is($parsed->{value}, '111', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18; ; total length=230 mm; tail length=115 mm;' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length', $name);
is($parsed->{value}, '230', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( '** Body length =345 cm; Blubber=1 cm ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Body length', $name);
is($parsed->{value}, '345', $name);
is($parsed->{units}, 'cm', $name);

($name, $test) = setup( '762-292-121-76 2435.0g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '2435.0', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( 'TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'Weight', $name);
is($parsed->{value}, '0.77', $name);
is($parsed->{units}, 'g', $name);
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL', $name);
is($parsed->{value}, '44', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '62', $name);
is($parsed->{units}, 'g', $name);

#$test = setup( 'SVL 550 mm, tail 125 mm, 47.0 gm.' );
#$parsed = extract_body_mass( $test, 'test');
#is($parsed->{key},   '');
#is($parsed->{value}, '47.0');
#is($parsed->{units}, 'gm');

($name, $test) = setup( 'body mass=20 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'body mass', $name);
is($parsed->{value}, '20', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( 'weight=81.00 g; sex=female ? ; age=u ad.' );
$parsed = extract_sex( $test, 'test');
is($parsed->{key},   'sex', $name);
is($parsed->{value}, 'female ?', $name);
$parsed = extract_life_stage( $test, 'test');
is($parsed->{key},   'age', $name);
is($parsed->{value}, 'u ad.', $name);

($name, $test) = setup( 't.l.= 2 feet 3.1 - 4.5 inches ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   't.l.', $name);
is($parsed->{value}->[0], '2', $name);
is($parsed->{value}->[1], '3.1 - 4.5', $name);
is($parsed->{units}->[0], 'feet', $name);
is($parsed->{units}->[1], 'inches', $name);

($name, $test) = setup( '2 ft. 3.1 - 4.5 in. ' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}->[0], '2', $name);
is($parsed->{value}->[1], '3.1 - 4.5', $name);
is($parsed->{units}->[0], 'ft.', $name);
is($parsed->{units}->[1], 'in.', $name);

($name, $test) = setup( 'total length= 2 ft.' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length', $name);
is($parsed->{value}->[0], '2', $name);
is($parsed->{units}->[0], 'ft.', $name);

($name, $test) = setup( '2 lbs. 3.1 - 4.5 oz ' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}->[0], '2', $name);
is($parsed->{value}->[1], '3.1 - 4.5', $name);
is($parsed->{units}->[0], 'lbs.', $name);
is($parsed->{units}->[1], 'oz', $name);

($name, $test) = setup( '{"totalLengthInMM":"x", "earLengthInMM":"20", "weight":"[139.5] g" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight', $name);
is($parsed->{value}, '[139.5]', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( '{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", "molt":"No molt", "stomach contents":"Not recorded", "weight":"94 gr."' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight', $name);
is($parsed->{value}, '94', $name);
is($parsed->{units}, 'gr.', $name);

($name, $test) = setup( 'AJR-32   186-102-23-15  15.0g' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '186', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'sex=unknown ; crown-rump length=8 mm' );
$parsed = extract_sex( $test, 'test');
is($parsed->{key},   'sex', $name);
is($parsed->{value}, 'unknown', $name);

($name, $test) = setup( 'sex=unknown ; crown-rump length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed, '', $name);

($name, $test) = setup( 'length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length', $name);
is($parsed->{value}, '8', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'another; length=8 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'length', $name);
is($parsed->{value}, '8', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'another; TL_120, noise' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL_', $name);
is($parsed->{value}, '120', $name);
is($parsed->{units}, '', $name);

($name, $test) = setup( 'another; TL - 101.3mm, noise' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL', $name);
is($parsed->{value}, '101.3', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'before; TL153, after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL', $name);
is($parsed->{value}, '153', $name);
is($parsed->{units}, '', $name);

($name, $test) = setup( 'before; Total length in catalog and specimen tag as 117, after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Total length', $name);
is($parsed->{value}, '117', $name);
is($parsed->{units}, '', $name);

($name, $test) = setup( 'before Snout vent lengths range from 16 to 23 mm. after' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Snout vent lengths', $name);
is($parsed->{value}, '16 to 23', $name);
is($parsed->{units}, 'mm.', $name);

($name, $test) = setup( 'Size=13 cm TL' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL', $name);
is($parsed->{value}, '13', $name);
is($parsed->{units}, 'cm', $name);

($name, $test) = setup( 'det_comments:31.5-58.3inTL' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL', $name);
is($parsed->{value}, '31.5-58.3', $name);
is($parsed->{units}, 'in', $name);

($name, $test) = setup( 'SVL52mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'SVL', $name);
is($parsed->{value}, '52', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'snout-vent length=221 mm; total length=257 mm; tail length=36 mm' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length', $name);
is($parsed->{value}, '257', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'SVL 209 mm, total 272 mm, 4.4 g.' );
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total', $name);
is($parsed->{value}, '272', $name);
is($parsed->{units}, 'mm', $name);

($name, $test) = setup( 'Note in catalog: 83-0-17-23-fa64-35g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '35', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( '{"measurements":"20.2g, SVL 89.13mm" }' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '20.2', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( 'Body: 15 g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'Body', $name);
is($parsed->{value}, '15', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( '82-00-15-21-tr7-fa63-41g' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '', $name);
is($parsed->{value}, '41', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( 'left gonad length=10 mm; right gonad length=10 mm;' );
$parsed = extract_total_length( $test, 'test');
is($parsed, '', $name);

($name, $test) = setup( 'Respective sex and msmt. in mm' );
$parsed = extract_sex( $test, 'test');
is($parsed, '', $name);

($name, $test) = setup( 'sex=unknown ; age class=adult/juvenile' );
$parsed = extract_life_stage( $test, 'test');
is($parsed->{key},   'age class', $name);
is($parsed->{value}, 'adult/juvenile', $name);

($name, $test) = setup( 'weight=5.4 g; unformatted measurements=77-30-7-12=5.4' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'weight', $name);
is($parsed->{value}, '5.4', $name);
is($parsed->{units}, 'g', $name);

($name, $test) = setup( 'unformatted measurements=77-30-7-12=5.4; weight=5.4;' );
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements', $name);
is($parsed->{value}, '5.4', $name);
is($parsed->{units}, '', $name);


done_testing();

