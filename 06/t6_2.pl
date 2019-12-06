#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t6.pl
#
#        USAGE: ./t6.pl  
#
#  DESCRIPTION: Advent of code 2019 Day 6 task 1
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 12/06/2019 12:37:53 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use Graph;
use 5.020;

my $g = Graph->new( directed => 0);
my %vertex_from;
my %vertex_to;

open my $file, '<', '../input';

while (<$file>) {
    chomp;

    my ($first, $second) = $_ =~ /(.*?)\)(.*)/msx;
    $vertex_from{$first} = 1;
    $vertex_to{$second} = 1;

    $g->add_edge($first, $second);
}

my @path = $g->SP_Dijkstra("YOU", "SAN");
        if (@path) {
            say scalar @path - 3;
        }
