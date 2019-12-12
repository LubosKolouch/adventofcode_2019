#!env perl

use warnings;
use strict;
use Math::Utils;
use Data::Dumper;
use 5.020;

my %moons;
my %all_moons;
my %cachex;
my %cachey;
my %cachez;

my $seenx;
my $seeny;
my $seenz;

my $moon = 0;
my $step = 0;

open my $file, '<', 'input';

for my $line (<$file>) {
    chomp $line;

    $moons{$step}{'energy'} = 0;

    $all_moons{$moon}          = 1;
    $moons{$step}{$moon}{'vx'} = 0;
    $moons{$step}{$moon}{'vy'} = 0;
    $moons{$step}{$moon}{'vz'} = 0;

    $line =~ s/\<//g;
    $line =~ s/\>//g;

    my @pairs = split /, /, $line;

    for my $pair (@pairs) {
        my ( $coord, $value ) = split( /=/, $pair );
        $moons{$step}{$moon}{$coord} = $value;
    }

    $moons{$step}{$moon}{'energy'} = (
        abs( $moons{$step}{$moon}{'x'} ) +
          abs( $moons{$step}{$moon}{'y'} ) +
          abs( $moons{$step}{$moon}{'z'} ) ) *
      (
        abs( $moons{$step}{$moon}{'vx'} ) +
          abs( $moons{$step}{$moon}{'vy'} ) +
          abs( $moons{$step}{$moon}{'vz'} ) );

    $moons{$step}{'energy'} += $moons{$step}{$moon}{'energy'};

    $moon += 1;
}

while (1) {
    $step++;
    $moons{$step}{'energy'} = 0;
    my $hashx = '';
    my $hashy = '';
    my $hashz = '';
    #warn Dumper \%cachex;
    #warn Dumper \%cachey;
    #warn Dumper \%cachez;

    #warn Dumper \%moons;

    for my $m1 ( keys %all_moons ) {
        $moons{$step}{$m1}{'vx'} = $moons{ $step - 1 }{$m1}{'vx'};
        $moons{$step}{$m1}{'vy'} = $moons{ $step - 1 }{$m1}{'vy'};
        $moons{$step}{$m1}{'vz'} = $moons{ $step - 1 }{$m1}{'vz'};
    }
    for my $m1 ( keys %all_moons ) {

        for my $m2 ( keys %all_moons ) {
            $moons{$step}{$m1}{'vx'} += 1 if $moons{ $step - 1 }{$m1}{'x'} < $moons{ $step - 1 }{$m2}{'x'};
            $moons{$step}{$m1}{'vx'} -= 1 if $moons{ $step - 1 }{$m1}{'x'} > $moons{ $step - 1 }{$m2}{'x'};

            $moons{$step}{$m1}{'vy'} += 1 if $moons{ $step - 1 }{$m1}{'y'} < $moons{ $step - 1 }{$m2}{'y'};
            $moons{$step}{$m1}{'vy'} -= 1 if $moons{ $step - 1 }{$m1}{'y'} > $moons{ $step - 1 }{$m2}{'y'};

            $moons{$step}{$m1}{'vz'} += 1 if $moons{ $step - 1 }{$m1}{'z'} < $moons{ $step - 1 }{$m2}{'z'};
            $moons{$step}{$m1}{'vz'} -= 1 if $moons{ $step - 1 }{$m1}{'z'} > $moons{ $step - 1 }{$m2}{'z'};
        }

        #pprint("Before applying moon "+str($m1))
        #pprint(moons)
        $moons{$step}{$m1}{'x'} = $moons{ $step - 1 }{$m1}{'x'} + $moons{$step}{$m1}{'vx'};
        $moons{$step}{$m1}{'y'} = $moons{ $step - 1 }{$m1}{'y'} + $moons{$step}{$m1}{'vy'};
        $moons{$step}{$m1}{'z'} = $moons{ $step - 1 }{$m1}{'z'} + $moons{$step}{$m1}{'vz'};

        $hashx .= $moons{$step}{$m1}{'x'} . ' ' . $moons{$step}{$m1}{'vx'};
        $hashy .= $moons{$step}{$m1}{'y'} . ' ' . $moons{$step}{$m1}{'vy'};
        $hashz .= $moons{$step}{$m1}{'z'} . ' ' . $moons{$step}{$m1}{'vz'};

        $moons{$step}{$m1}{'energy'} =
          ( abs( $moons{$step}{$m1}{'x'} ) + abs( $moons{$step}{$m1}{'y'} ) + abs( $moons{$step}{$m1}{'z'} ) )
          * (
            abs( $moons{$step}{$m1}{'vx'} ) +
              abs( $moons{$step}{$m1}{'vy'} ) +
              abs( $moons{$step}{$m1}{'vz'} ) );

        $moons{$step}{'energy'} += $moons{$step}{$m1}{'energy'};
    }

    if ( ( defined $cachex{$hashx} ) and ( not $seenx ) ) {
        say "x: ";
        say $step - 1;
        $seenx = $step - 1;
    }
    else {
        $cachex{$hashx} = 1;
    }

    if ( ( defined $cachey{$hashy} ) and ( not $seeny ) ) {
        say "y: ";
        say $step - 1;
        $seeny = $step - 1;
    }
    else {
        $cachey{$hashy} = 1;
    }

    if ( ( defined $cachez{$hashz} ) and ( not $seenz ) ) {
        say "z: ";
        say $step - 1;
        $seenz = $step - 1;
    }
    else {
        $cachez{$hashz} = 1;
    }

    if ( $step == 1000 ) { say "solution 1 : " . $moons{$step}{'energy'} };

    say $step if ( $step % 1e4 == 0 );

    if ( $seenx and $seeny and $seenz ) {
        say( Math::Utils::lcm( Math::Utils::lcm( $seenx, $seeny ), $seenz ) );
        die;
    }

}
