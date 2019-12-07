#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t7.pl
#
#        USAGE: ./t7.pl
#
#  DESCRIPTION: https://adventofcode.com/2019/day/7
#
#  --- Day 7: Amplification Circuit --
#
#       AUTHOR: Lubos Kolouch
#===============================================================================

use strict;
use warnings;
use feature qw/say/;
use Math::Combinatorics;
use Data::Dumper;

sub run_intcode {
    my $input = shift;

    my @input_arr = @{$input};

# opcodes
#
# 1 - adding, noun, verb, result (3+1)
# 2 - multiply, noun, verb, result (3+1)
# 3 - input, result (1+1)
# 4 - output, result (1+1)
# 5 - jump, zero/nonzero, where (or ignored if zero)
# 6 - jump, zero/nonzero, where if zero (or ignored)
# 7 - less than, if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# 8 - equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

    my %params = (
        1 => 3,
        2 => 3,
        3 => 1,
        4 => 1,
        5 => 2,
        6 => 2,
        7 => 3,
        8 => 3,
    );

    my %writing_instr = (
        1 => 1,
        2 => 1,
        7 => 1,
        8 => 1,
    );

    # positions : 0 = position mode, 1 = immediate mode
    # ABCDE
    # 1002
    #
    #DE - two-digit opcode,      02 == opcode 2
    # C - mode of 1st parameter,  0 == position mode
    # B - mode of 2nd parameter,  1 == immediate mode
    # A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero

    open my $file, '<', 'input' or die 'file cannot be opened';

    #open my $file, '<', 'test_input' or die 'file cannot be opened';

    my $text = <$file>;
    chomp $text;

    my @data = split /,/, $text;

    my $pos = 0;

    while ( $data[$pos] != 99 ) {

        #say "----------------------------";
        #say "pos $pos";
        #warn "pos $pos";
        #say "instruction " . $data[$pos];
        #warn "instruction " . $data[$pos];
        my @instr = split //, $data[$pos];

        #say Dumper \@instr;

        my @what;

        my $mode;

        # load the instruction and parameters
        if ( scalar(@instr) == 1 ) {
            unshift @instr, 0;
        }

        my $last = pop @instr // 0;
        my $prev = pop @instr // 0;

        $what[0] = 10 * $prev + $last;

        #say "prev $prev last $last => instruction $what[0]";

        die unless defined $params{ $what[0] };

        for my $p ( 1 .. $params{ $what[0] } ) {

            #say "parameter $p in data $data[$pos+$p] or $data[$data[$pos+$p]]";
            $mode = pop @instr // 0;

            if ( ( $mode == 1 ) or ( $data[$pos] == 3 ) ) {

                #say "immediate mode, data " . $data[ $pos + $p ]." to what ".$p ;
                $what[$p] = $data[ $pos + $p ];
                next;
            }

            if ( ( $p == $params{ $what[0] } ) and ( $writing_instr{ $what[0] } ) ) {

                #say "immediate mode, data " . $data[ $pos + $p ]." to what ".$p ;
                $what[$p] = $data[ $pos + $p ];
            }
            else {
                #say "position mode, data : ".$data[ $data[$pos+$p]]." to what $p";
                $what[$p] = $data[ $data[ $pos + $p ] ];
            }

        }

        # Parameters that an instruction writes to will never be in immediate mode.
        #    $what[$params{$what[0]}] = $data[$pos + $params{$what[0]}];

        #say "final what";
        #say Dumper \@what;

        ##say "data[pos] $data[$pos]";

        if ( $what[0] == 1 ) {

            #say "Writing sum of $what[1] and $what[2] to $what[3]";
            $data[ $what[3] ] = $what[1] + $what[2];
        }
        elsif ( $what[0] == 2 ) {
            $data[ $what[3] ] = $what[1] * $what[2];
        }
        elsif ( $what[0] == 3 ) {

            #say "Writing $input to position $what[1]";
            $data[ $what[1] ] = shift @input_arr;

            #say "data[9]: ".$data[9];
        }
        elsif ( $what[0] == 4 ) {
            return $what[1];
        }
        elsif ( $what[0] == 5 ) {

            #say "Processing instruction 5";
            if ( $what[1] ) {
                $pos = $what[2];

                #say "Jumping to $pos";
                next;
            }
        }
        elsif ( $what[0] == 6 ) {
            if ( $what[1] == 0 ) {
                $pos = $what[2];

                #say "Jumping to $pos";
                next;
            }
        }
        elsif ( $what[0] == 7 ) {
            if ( $what[1] < $what[2] ) {

                #say "Storing 1 to $what[3]";
                $data[ $what[3] ] = 1;

            }
            else {
                #say "Storing 0 to $what[3]";
                $data[ $what[3] ] = 0;
            }
        }
        elsif ( $what[0] == 8 ) {

            #say "Instruction 8";
            if ( $what[1] == $what[2] ) {

                #say "Values are equal";
                $data[ $what[3] ] = 1;
            }
            else {
                #say "Values are not equal";
                $data[ $what[3] ] = 0;
            }
        }
        else {
            die "Unknown argument found";
        }

        my $shift = $params{ $what[0] } + 1;
        $pos += $shift;

        #say "Shifting $shift positions to $pos";

    }
}

# -------- MAIN ------------

my @list = qw/0 1 2 3 4/;

my $combinat = Math::Combinatorics->new(
        count => 5,
        data  => [@list],
    );


my $max = 0;
while ( my @combo = $combinat->next_permutation ) {
    my $input = 0;
    for my $code (@combo) {
        #say "passing code $code input $input";

        $input = run_intcode([$code,$input]);

        $max = $input if ($input > $max);
        #say "result $input max $max";
    }

}
say $max;
