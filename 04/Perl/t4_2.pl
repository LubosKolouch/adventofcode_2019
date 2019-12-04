#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t4.pl
#
#        USAGE: ./t4.pl
#
#  DESCRIPTION: Advent of Code 2019 Day 04 task 1
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (),
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 12/04/2019 12:36:32 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use 5.020;

my $count;

for ( 172851 .. 675869 ) {
    next unless /(\d)\1/;

    my $prev = 0;
    my $exit = 0;

    for my $x ( split // ) {
        unless ( $x >= $prev ) {
            $exit = 1;
            last;
        }
        $prev = $x;
    }

    unless ($exit) {
        my $found     = 1;
        my $prev_char = 0;
        for my $char ( split // ) {
            if ( $char != $prev_char ) {
                last if ( $found == 2 );
                $found = 1;
            }
            else {
                $found++;
            }
            $prev_char = $char;
        }
        $count++ if ( $found == 2 );
    }
}

say $count;

