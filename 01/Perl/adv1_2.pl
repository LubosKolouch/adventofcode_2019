#!/usr/bin/perl 
#===============================================================================
#
#         FILE: adv1_2.pl
#
#        USAGE: ./adv1_2.pl  
#
#  DESCRIPTION: https://adventofcode.com/2019/day/1#part2
#
#  Day 1: The Tyranny of the Rocket Equation
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 12/01/2019 11:51:24 AM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use feature qw/say/;

sub get_fuel_req {
    my $input = shift;

    my $total;

    while ($input > 0) {
         $input = int($input / 3) - 2;       
         $total += $input if $input > 0;
    }

    return $total;
}


open my $file, '<', '../1.txt' or die 'File cannot be opened';

my $total;

while (<$file>) {
    chomp;

    $total += get_fuel_req($_);

}

say $total;


