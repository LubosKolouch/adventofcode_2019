#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t7_2.pl
#
#        USAGE: ./t7_2.pl
#
#  DESCRIPTION: https://adventofcode.com/2019/day/7
#
#  --- Day 7: proclification Circuit --
#
#       AUTHOR: Lubos Kolouch
#===============================================================================

use strict;
use warnings;
use feature qw/say/;
use Math::Combinatorics;
use Data::Dumper;

my %processor;
my %program_param;
my %painted;

my %grid;

sub get_input {
    my $cur_proc = shift;

    # for debugging
    my $qu      = $processor{$cur_proc}{'io'};
    my $g_value = $grid{ $processor{$cur_proc}{'x'} }{ $processor{$cur_proc}{'y'} } // 0;
    push @{ $processor{$cur_proc}{'io'} }, $g_value;

    return 1;
}

sub process_output {
    my $cur_proc = shift;

    if (scalar @{ $processor{$cur_proc}{'io'} } == 2 ) {
        my $paint = shift @{ $processor{$cur_proc}{'io'} };

        $grid{$processor{$cur_proc}{'x'}}{$processor{$cur_proc}{'y'}}    = $paint;
        $painted{($processor{$cur_proc}{'x'},$processor{$cur_proc}{'y'})} = 1;
        my $next_move = shift @{ $processor{$cur_proc}{'io'} };
        if ( $next_move == 0 ) {

            # ^ -> <
            if ( $processor{$cur_proc}{'direction'} eq '^' ) {
                $processor{$cur_proc}{'direction'} = '<';
                $processor{$cur_proc}{'x'} -= 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq '>' ) {
                $processor{$cur_proc}{'direction'} = '^';
                $processor{$cur_proc}{'y'} -= 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq 'v' ) {
                $processor{$cur_proc}{'direction'} = '>';
                $processor{$cur_proc}{'x'} += 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq '<' ) {
                $processor{$cur_proc}{'direction'} = 'v';
                $processor{$cur_proc}{'y'} += 1;
            }
        }

        if ( $next_move == 1 ) {

            # ^ -> <
            if ( $processor{$cur_proc}{'direction'} eq '^' ) {
                $processor{$cur_proc}{'direction'} = '>';
                $processor{$cur_proc}{'x'} += 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq '>' ) {
                $processor{$cur_proc}{'direction'} = 'v';
                $processor{$cur_proc}{'y'} += 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq 'v' ) {
                $processor{$cur_proc}{'direction'} = '<';
                $processor{$cur_proc}{'x'} -= 1;
            }

            elsif ( $processor{$cur_proc}{'direction'} eq '<' ) {
                $processor{$cur_proc}{'direction'} = '^';
                $processor{$cur_proc}{'y'} -= 1;
            }
        }
    }

    return 1;
}

sub run_intcode {

    # current processor
    my $cur_proc = shift;

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
# 9 - reset relative base

    my %params = (
        1  => 3,
        2  => 3,
        3  => 1,
        4  => 1,
        5  => 2,
        6  => 2,
        7  => 3,
        8  => 3,
        9  => 1,
        99 => 0,
    );

    # positions : 0 = position mode, 1 = immediate mode
    # ABCDE
    # 1002
    #
    #DE - two-digit opcode,      02 == opcode 2
    # C - mode of 1st parameter,  0 == position mode
    # B - mode of 2nd parameter,  1 == immediate mode
    # A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero

    #warn Dumper \$processor{$cur_proc};

    my $pos = $processor{$cur_proc}{'position'};

    while (1) {

        my $instr = $processor{$cur_proc}{'program'}{$pos};

        my $op    = $instr % 100;
        my $mode1 = int( $instr / 100 ) % 10;
        my $mode2 = int( $instr / 1000 ) % 10;
        my $mode3 = int( $instr / 10000 ) % 10;

        my $reg1 = $processor{$cur_proc}{'program'}{ $pos + 1 } // 0;
        my $reg2 = $processor{$cur_proc}{'program'}{ $pos + 2 } // 0;
        my $reg3 = $processor{$cur_proc}{'program'}{ $pos + 3 } // 0;

        my $v1 = $reg1;

        if ( $op != 3 ) {
            $v1 = $processor{$cur_proc}{'program'}{$reg1} if $mode1 == 0;
            $v1 = $processor{$cur_proc}{'program'}{ $reg1 + $processor{$cur_proc}{'relative_base'} }
              if $mode1 == 2;
        }
        else {
            $v1 += $processor{$cur_proc}{'relative_base'} if $mode1 == 2;
        }

        my $v2 = $reg2;
        $v2 = $processor{$cur_proc}{'program'}{$reg2} if $mode2 == 0;
        $v2 = $processor{$cur_proc}{'program'}{ $reg2 + $processor{$cur_proc}{'relative_base'} }
          if $mode2 == 2;

        my $v3 = $reg3;
        $v3 += $processor{$cur_proc}{'relative_base'} if $mode3 == 2;

        die unless defined $params{$op};

        $v1 = 0 unless defined $v1;

        #$v2 = 0 unless defined $v2;

        #        say "pos $pos mode1 $mode1 mode2 $mode2 mode3 $mode3  op $op v1 $v1 v2 $v2 v3 $v3";

        if ( $op == 1 ) {
            $processor{$cur_proc}{'program'}{$v3} = $v1 + $v2;
        }
        elsif ( $op == 2 ) {
            $processor{$cur_proc}{'program'}{$v3} = $v1 * $v2;
        }
        elsif ( $op == 3 ) {
            get_input($cur_proc);
            $processor{$cur_proc}{'program'}{$v1} = shift @{ $processor{$cur_proc}{'io'} };
        }
        elsif ( $op == 4 ) {
            push @{ $processor{$cur_proc}{'io'} }, $v1;
            process_output($cur_proc);
        }
        elsif ( $op == 5 ) {
            if ($v1) {
                $pos = $v2;
                next;
            }
        }
        elsif ( $op == 6 ) {
            if ( $v1 == 0 ) {
                $pos = $v2;
                next;
            }
        }
        elsif ( $op == 7 ) {
            if ( $v1 < $v2 ) {
                $processor{$cur_proc}{'program'}{$v3} = 1;

            }
            else {
                $processor{$cur_proc}{'program'}{$v3} = 0;
            }
        }
        elsif ( $op == 8 ) {

            if ( $v1 == $v2 ) {
                $processor{$cur_proc}{'program'}{$v3} = 1;
            }
            else {
                $processor{$cur_proc}{'program'}{$v3} = 0;
            }
        }
        elsif ( $op == 9 ) {
            $processor{$cur_proc}{'relative_base'} += $v1;
        }

        elsif ( $op == 99 ) {
            return ${ $processor{$cur_proc}{'io'} }[-1];
        }
        else {
            die "Unknown argument found";
        }

        my $shift = $params{$op} + 1;
        $pos += $shift;

    }

    return 1;
}

# -------- MAIN ------------

sub main {
    my $input_file = shift or die 'No input file passed';
    open my $file, '<', $input_file or die 'file cannot be opened';

    my $program = <$file>;
    chomp $program;

    $program_param{'mode'}        = 'normal';
    $program_param{'program_end'} = 0;

    #my @list = qw/5 6 7 8 9/;
    #y @list = ( 0 .. 4 ) if $program_param{'mode'} eq 'normal';
    #@list = ( 5 .. 9 ) if $program_param{'mode'} eq 'feedback';

    my @list = (1);

    my $combinat = Math::Combinatorics->new(
        count => scalar @list,
        data  => [@list],
    );

    my $max = 0;
    while ( my @combo = $combinat->next_permutation ) {
        $program_param{'program_end'} = 0;
        my @proc = qw/A/;

        # initialize the processors

        my $input = 0;

        for my $phase (@combo) {
            my $cur_proc = shift @proc;
            $processor{$cur_proc}{'phase'} = $phase;

            # do we need to set phase at the beginning?
            $processor{$cur_proc}{'phase_needed'}  = 0;
            $processor{$cur_proc}{'position'}      = 0;
			$processor{$cur_proc}{'io'}            = [];
            #$processor{$cur_proc}{'io'}            = [2];
            $processor{$cur_proc}{'phase_set'}     = 0;
            $processor{$cur_proc}{'relative_base'} = 0;
            $processor{$cur_proc}{'x'}             = 50;
            $processor{$cur_proc}{'y'}             = 50;
            $processor{$cur_proc}{'direction'}     = '^';

            my $i = 0;
            for my $num ( split /,/msx, $program ) {
                $processor{$cur_proc}{'program'}{$i} = $num;
                $i++;
            }

        }

        my $end = 0;
        while ( $end == 0 ) {

            my @proc = qw/A/;

            # loop through the processors
            for my $procs ( 0 .. scalar @proc - 1 ) {
                my $cur_proc  = $proc[$procs];
                my $next_proc = $proc[ ( $procs + 1 ) % scalar @proc ];

                $processor{$next_proc}{'input'} = run_intcode($cur_proc);

                #    if ( ( $procs == scalar @proc - 1 ) and ( $processor{$next_proc}{'input'} > $max ) ) {
                #   $max = $processor{$next_proc}{'input'};
                #}

                if ( $procs == scalar @proc - 1 ) {
                    return $processor{$next_proc}{'input'};
                }

                if ( $program_param{'program_end'} ) {
                    $end = 1;

                    last;
                }

            }

            $end = 1 if $program_param{'mode'} eq 'normal';
        }

    }
    
    return 1;
}

$grid{50}{50} = 0;

main('input');

say scalar keys %painted;

undef %grid;

$grid{50}{50} = 1;

main('input');

for my $i (0..100) {
    for my $j (0..100) {
        my $p  = ' ';
        $p = 'X' if ($grid{$i}{$j});

        print $p;
    }
    say '';
}


# TESTS
use Test::More;
undef %grid;
undef %painted;
$grid{50}{50} = 0;

main('input');

is(scalar keys %painted, 2415);


done_testing;

