#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t8_2.pl
#
#        USAGE: ./t8_2.pl  
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
use utf8;
use open ':std', ':encoding(UTF-8)';

my %chars = ( 1 => '▓', 0 => ' ',    2=>'x' );

open my $file, '<', 'input' or die 'File cannot be opened';

my $text = (<$file>);
chomp $text;

my @arr = split //, $text;

my $lay_size = 25*6;
my %layer;

my $i =0;
for (@arr) {
    $i++;

    my $which_layer = int(($i-1) / $lay_size) +1;

    # 1 => 1 0 0
    # 2 => 1 0 1
    # 3 => 1 0 2
    # 26 => 1 1 0
    # 150 => 1 0 0

    my $x = int(($i -1 )  / 25 % 6);
    my $y = int(($i-1)  % 25);

    next if defined $layer{$x}{$y} and $layer{$x}{$y} ne 'x';
    $layer{$x}{$y} = $chars{$_};


}

for my $x (0..5) {
    for my $y (0..24) {
        print $layer{$x}{$y};
    }
    say '';
}
