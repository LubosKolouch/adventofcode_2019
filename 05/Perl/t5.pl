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
use Data::Dumper;

# opcodes
#
# 1 - adding, noun, verb, result (3+1)
# 2 - multiply, noun, verb, result (3+1)
# 3 - input, result (1+1)
# 4 - output, result (1+1)

my %params = (
    1 => 3,
    2 => 3,
    3 => 1,
    4 => 1,
);

# positions : 0 = position mode, 1 = immediate mode
# ABCDE
# 1002
#
#DE - two-digit opcode,      02 == opcode 2
# C - mode of 1st parameter,  0 == position mode
# B - mode of 2nd parameter,  1 == immediate mode
# A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero

my $input = shift or die 'Input not provided';

open my $file, '<', '../input' or die 'file cannot be opened';

my $text = <$file>;
chomp $text;

my @data = split /,/, $text;

my $pos = 0;

while ( $data[$pos] != 99 ) {

    #say "----------------------------";
    #say "data[pos] ".$data[$pos];
    my @instr = split //, $data[$pos];
    #say "instruction";
    #warn Dumper \@instr;

    my @what;

    # load the instruction and parameters
    #say "scalar instr ".scalar(@instr);
    if ( scalar(@instr) == 1 ) {
        $what[0] = $instr[0];

        #say "processing instruction $what[0] with parameters $params{$what[0]}";

        for my $p ( 1 .. $params{ $what[0] } -1 ) {
            #say "processing param $p";

            if ($what[0] != 3) {
                #say "position mode, data ".$data[ $data[ $pos + $p] ];
                $what[$p] = $data[ $data[ $pos + $p] ];
            } else {
                #say "immediate mode";
                $what[$p] = $data[ $pos + $p ];
            }


        }
        #storing location

    }
    else {

        my $last = pop @instr // 0;
        my $prev = pop @instr // 0;

        $what[0] = 10 * $prev + $last;

        #say "prev $prev last $last => instruction $what[0]";

        die unless defined $params{$what[0]};

        for my $p ( 1 .. $params{ $what[0] } -1  ) {
            #say "parameter $p";
            my $mode = pop @instr // 0;
            if ( $mode == 1 ) {
                #say "immediate more, data ". $data[$pos + $p];
                $what[$p] = $data[$pos + $p];
            }
            else {
                #say "position mode : ";
                $what[$p] = $data[ $data[ $pos + $p ] ];
            }

        }
    }
    $what[$params{$what[0]}] = $data[$pos + $params{$what[0]}];

    #say "final what";
    #warn Dumper \@what;

    #say "data[pos] $data[$pos]";

    if ( $what[0] == 1 ) {
        #say "Writing sum of $what[1] and $what[2] to $what[3]";
        $data[ $what[3] ] = $what[1] + $what[2];
    }
    elsif ( $what[0] == 2 ) {
        $data[ $what[3] ] = $what[1] * $what[2];
    }
    elsif ( $what[0] == 3 ) {
        #say "Writing $input to position $what[1]";
        $data[ $what[1] ] = $input;
    }
    elsif ( $what[0] == 4 ) {
        say $data[ $what[1] ];
    }
    else {
        die "Unknown argument found";
    }


    my $shift = $params{ $what[0] } + 1;
    $pos += $shift;
    #say "Shifting $shift positions to $pos";

}

