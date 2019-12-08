#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t1.pl
#
#        USAGE: ./t1.pl  
#
#  DESCRIPTION: https://adventofcode.com/2019/day/8
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Lubos Kolouch
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 12/08/2019 12:03:24 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use 5.020;
use Data::Dumper;

open my $file, '<', 'input' or die 'File cannot be opened';

my $text = (<$file>);
chomp $text;

my @arr = split //, $text;

my $count;
my $seg_size = 25*6;
my $min = 9999999;
my $min_count;

my %layer;

my $i =0;
for (@arr) {
    $i++;

    my $which_layer = int(($i-1) / $seg_size);

    $layer{ $which_layer }{$_}++;

}

for (keys %layer) {
    if ($layer{$_}{0} < $min) {
        $min = $layer{$_}{0};
        $min_count =  $layer{$_}{1} *  $layer{$_}{2};
    }
}

say $min_count;
