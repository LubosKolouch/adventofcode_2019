#!/usr/bin/perl 
#===============================================================================
#
#         FILE: adv1.pl
#
#        USAGE: ./adv1.pl  
#
#  DESCRIPTION: https://adventofcode.com/2019/day/1
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

open my $file, '<', '../1.txt' or die 'File cannot be opened';

my $total;

while (<$file>) {
    chomp;

    $total += int($_ / 3) - 2;
}

say $total;


