use feature qw( switch say );
use Test::More;
use Parse qw(
    extract_sex
    extract_life_stage
    extract_total_length
    extract_body_mass
);

my ($test, $parsed, $name);

$test = { test => '"{"measurements":"308-190-45-20" }"' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '308');
is($parsed->{units}, 'mm');

$test = { test => '308-190-45-20' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '308');
is($parsed->{units}, 'mm');

$test = { test => '{"measurements":"143-63-20-17=13 g" }' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '143');
is($parsed->{units}, 'mm');
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '13');
is($parsed->{units}, 'g');

$test = { test => '143-63-20-17=13 g' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '143');
is($parsed->{units}, 'mm');
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '13');
is($parsed->{units}, 'g');

$test = { test => 'reproductive data: Testes descended -10x7 mm; sex: male; unformatted measurements: 181-75-21-18=22 g' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '22');
is($parsed->{units}, 'g');

$test = { test => '{ "massInGrams"="20.1" }' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'massInGrams');
is($parsed->{value}, '20.1');
is($parsed->{units}, 'Grams');

$test = { test => 'age class=adult ; snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '111');
is($parsed->{units}, 'mm');

$test = { test => 'sex=female ; unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18; ; total length=230 mm; tail length=115 mm; hind foot with claw=22 mm; ear from notch=18 mm' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '230');
is($parsed->{units}, 'mm');

$test = { test => '** Body length =345 cm; Blubber=1 cm  *Aged by tooth section. Died of gunshot wounds.' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'Body length');
is($parsed->{value}, '345');
is($parsed->{units}, 'cm');

$test = { test => '762-292-121-76 2435.0g' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '2435.0');
is($parsed->{units}, 'g');

$test = { test => 'TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'Weight');
is($parsed->{value}, '0.77');
is($parsed->{units}, 'g');
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '44');
is($parsed->{units}, 'mm');

$test = { test => 'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '62');
is($parsed->{units}, 'g');

#$test = { test => 'SVL 550 mm, tail 125 mm, 47.0 gm.' };
#$parsed = extract_body_mass( $test, 'test');
#is($parsed->{key},   '');
#is($parsed->{value}, '47.0');
#is($parsed->{units}, 'gm');

$test = { test => 'body mass=20 g' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   'body mass');
is($parsed->{value}, '20');
is($parsed->{units}, 'g');

$test = { test => 'weight=81.00 g; sex=female ? ; age=u ad.' };
$parsed = extract_sex( $test, 'test');
is($parsed->{key},   'sex');
is($parsed->{value}, 'female ?');
$parsed = extract_life_stage( $test, 'test');
is($parsed->{key},   'age');
is($parsed->{value}, 'u ad.');

$test = { test => 't.l.= 2 feet 3.1 - 4.5 inches ' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   't.l.');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'feet');
is($parsed->{units}->[1], 'inches');

$test = { test => '2 ft. 3.1 - 4.5 in. ' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'ft.');
is($parsed->{units}->[1], 'in.');

$test = { test => 'total length= 2 ft.' };
$parsed = extract_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}->[0], '2');
is($parsed->{units}->[0], 'ft.');

$test = { test => '2 lbs. 3.1 - 4.5 oz ' };
$parsed = extract_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}->[0], '2');
is($parsed->{value}->[1], '3.1 - 4.5');
is($parsed->{units}->[0], 'lbs.');
is($parsed->{units}->[1], 'oz');

done_testing();

