#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t2.pl
#
#        USAGE: ./t2.pl  
#
#  DESCRIPTION: https://adventofcode.com/2019/day/2
#
#  --- Day 2: 1202 Program Alarm ---
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (), 
# ORGANIZATION: 
#      VERSION: 1.0
#      CREATED: 12/02/2019 06:15:21 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use feature qw/say/;

open my $file, '<', '../input' or die 'file cannot be opened';

my $text = <$file>;
chomp $text;

my @data = split /,/, $text;

$data[1] = 12;
$data[2] = 2;

my $pos=0;

while ($data[$pos] != 99) {
    my $arg1 = $data[$data[$pos+1]];
    my $arg2 = $data[$data[$pos+2]];   

    if ($data[$pos] == 1) {
        $data[$data[$pos+3]] = $arg1+$arg2;
    } elsif ($data[$pos] == 2) {
         $data[$data[$pos+3]] = $arg1*$arg2;       
    } else {
        die "Unknown argument found";
    }
    $pos += 4;
}

say $data[0];



