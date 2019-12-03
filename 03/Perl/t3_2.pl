#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t3_2.pl
#
#        USAGE: ./t3_2.pl  
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
my %steps;
my $steps_count;
my $i;
my $min_count;
my %seen;

sub process_step {

                $grid{$posx}{$posy}++ unless $seen{$posx}{$posy};
                $seen{$posx}{$posy}=1;
                $steps_count++;
                unless ($steps{$i}{$posx}{$posy}) {
                    $steps{$i}{$posx}{$posy} = $steps_count;
                }

                if ($grid{$posx}{$posy} > 1) {
                    my $distance = abs($posx) + abs($posy);
                    my $total_steps = $steps{1}{$posx}{$posy} + $steps{2}{$posx}{$posy};
                    say "intersection $posx $posy distance $distance steps $total_steps";
                    $min_count = $total_steps unless $min_count;
                    $min_count = $total_steps if $min_count > $total_steps;
                    say "min count $min_count";
                }
}

open my $file, '<', '../input' or die 'cannot open input';


$i=0;
while (<$file>) {
    $i++;
    $posx=0;
    $posy=0;
    $steps_count = 0;
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


