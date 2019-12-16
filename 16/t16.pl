#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t16.pl
#
#        USAGE: ./t16.pl
#
#  DESCRIPTION: https://adventofcode.com/2019/day/16
#
#  --- Day 16: Flawed Frequency Transmission ---
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Lubos Kolouch
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 12/16/2019 08:52:49 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use 5.020;
use Data::Dumper;
use File::Slurp;

sub get_sol1 {
    my ( $input, $times ) = @_;

    my @input_arr = split //, $input;
    my @phases = ( 0, 1, 0, -1 );
    my @input2;

    for ( 1 .. 100 ) {
        undef @input2;
        for my $i ( 0 .. scalar(@input_arr) - 1 ) {
            my $repeat = scalar @input_arr - $i;

            my $value;
            for my $j ( 0 .. $i ) {
                my $pos_phases = ( int( ( $i - $j ) / $repeat ) + 1 ) % scalar @phases;
                $value += ( $input_arr[ -$j - 1 ] * $phases[$pos_phases] );
            }
            unshift @input2, abs($value) % 10;
        }
        @input_arr = @input2;
    }
    return join '',@input_arr[0..7];
}

sub get_sol2 {
    my ($input, $times,$offset) = @_;

    # the offset was close to the list and obviously pattern for second half of
    # the list is 1, so...

    my @data = split //, substr($input,$offset-1);

    for (1..100) {
        my $sum = 0;
        for (my $i = scalar(@data)-1; $i>0; $i--) {        
            $sum += $data[$i];
            $sum = $sum % 10;
            $data[$i] = $sum;
        }
    }

    return join '', @data[1..8];
}

my $input;
open my $file, '<', shift or die 'Nothing supplied';

$input = read_file($file);
chomp $input;

say "Part 1: ".get_sol1($input,100);
my $offset = substr($input,0,7);
$input = $input x 10_000;

say "Part 2: ".get_sol2($input,100,$offset);

