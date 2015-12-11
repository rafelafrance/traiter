use feature qw( switch say );
use Test::More;
use Parse qw( dwc_sex dwc_life_stage vto_total_length vto_body_mass );

my ($test, $parsed);

$test = { test => 'reproductive data: Testes descended -10x7 mm; sex: male; unformatted measurements: 181-75-21-18=22 g' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   'measurements');
is($parsed->{value}, '22');
is($parsed->{units}, 'g');

$test = { test => '{ "massInGrams"="20.1" }' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   'massInGrams');
is($parsed->{value}, '20.1');
is($parsed->{units}, 'Grams');

$test = { test => 'age class=adult ; snout-vent length=54 mm; total length=111 mm; tail length=57 mm; weight=5 g' };
$parsed = vto_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '111');
is($parsed->{units}, 'mm');

$test = { test => 'sex=female ; unformatted measurements=Verbatim weight=X;ToL=230;TaL=115;HF=22;E=18; ; total length=230 mm; tail length=115 mm; hind foot with claw=22 mm; ear from notch=18 mm' };
$parsed = vto_total_length( $test, 'test');
is($parsed->{key},   'total length');
is($parsed->{value}, '230');
is($parsed->{units}, 'mm');

$test = { test => '** Body length =345 cm; Blubber=1 cm  *Aged by tooth section. Died of gunshot wounds.' };
$parsed = vto_total_length( $test, 'test');
is($parsed->{key},   'Body length');
is($parsed->{value}, '345');
is($parsed->{units}, 'cm');

$test = { test => '762-292-121-76 2435.0g' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '2435.0');
is($parsed->{units}, 'g');

$test = { test => 'TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   'Weight');
is($parsed->{value}, '0.77');
is($parsed->{units}, 'g');
$parsed = vto_total_length( $test, 'test');
is($parsed->{key},   'TL');
is($parsed->{value}, '44');
is($parsed->{units}, 'mm');

$test = { test => 'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   '');
is($parsed->{value}, '62');
is($parsed->{units}, 'g');

#$test = { test => 'SVL 550 mm, tail 125 mm, 47.0 gm.' };
#$parsed = vto_body_mass( $test, 'test');
#is($parsed->{key},   '');
#is($parsed->{value}, '47.0');
#is($parsed->{units}, 'gm');

$test = { test => 'body mass=20 g' };
$parsed = vto_body_mass( $test, 'test');
is($parsed->{key},   'body mass');
is($parsed->{value}, '20');
is($parsed->{units}, 'g');

done_testing();

