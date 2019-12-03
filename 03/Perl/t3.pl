#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t3.pl
#
#        USAGE: ./t3.pl  
#
#  DESCRIPTION: 
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 12/03/2019 09:48:28 AM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use Data::Dumper;
use 5.020;

my %grid;
my $posx=0;
my $posy=0;
my %seen;

sub process_step {
                $grid{$posx}{$posy}++ unless $seen{$posx}{$posy};
                $seen{$posx}{$posy}=1;

                if ($grid{$posx}{$posy} > 1) {
                    my $distance = abs($posx) + abs($posy);
                    say "intersection $posx $posy distance $distance";
                }
}

open my $file, '<', '../input' or die 'cannot open input';



while (<$file>) {
    $posx=0;
    $posy=0;
    %seen = ();

    chomp;

    my @arr = split /,/, $_;

    for (@arr) {
        my ($direction, $count) = $_ =~ /(.)(.*)/msx;

        if ($direction eq 'R') {
            for (1..$count) {
                $posx++;
                &process_step;
            }
        }

        if ($direction eq 'L') {
            for (1..$count) {
                $posx--;
                &process_step;
            }
        }

        if ($direction eq 'U') {
            for (1..$count) {
                $posy++;
                &process_step;
            }
        }

        if ($direction eq 'D') {
            for (1..$count) {
                $posy--;
                &process_step;
            }
        }

    }

}


