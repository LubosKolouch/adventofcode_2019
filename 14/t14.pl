#!/usr/bin/perl 
#===============================================================================
#
#         FILE: t14.pl
#
#        USAGE: ./t14.pl
#
#  DESCRIPTION: https://adventofcode.com/2019/day/14
#
#  --- Day 14: Space Stoichiometry ---
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: YOUR NAME (),
# ORGANIZATION:
#      VERSION: 1.0
#      CREATED: 12/14/2019 12:08:09 PM
#     REVISION: ---
#===============================================================================

use strict;
use warnings;
use 5.020;
use Data::Dumper;
use Text::Trim;

my %bom;



open my $file, '<', 'input';

sub produce {
    my ( $what, $qty ) = @_;

    my %inventory;
    my %production_q;
    for (<$file>) {
        chomp;
        $_ =~ s/\h+$//msx;

        my @arr1 = split /\=\>/, $_;
        my (@out_arr) = split /\h+/, ltrim( rtrim( $arr1[1] ) );

        $bom{ $out_arr[1] }{'prod_qty'} = $out_arr[0];

        $inventory{ $out_arr[1] } = 0;
        $production_q{ $out_arr[1] } = 0;

        my @ing_list = split /, /, $arr1[0];
        for my $ing (@ing_list) {
            my @arr2 = split /\h+/, $ing;
            $bom{ $out_arr[1] }{'need_qty'}{ $arr2[1] } = $arr2[0];
            $production_q{$ing} = 0;
            $inventory{$ing} = 0;

        }

    }
    $inventory{'ORE'} = 0;

    $production_q{$what} = $qty;

    while (%production_q) {

        my $elem = ( sort keys %production_q )[0];

        #say "to produce $elem qty ".$production_q{$elem};

        $inventory{$elem} //= 0;
        if ( $inventory{$elem} >= $production_q{$elem} ) {

            #say "have enough elements";
            $inventory{$elem} -= $production_q{$elem};
            delete $production_q{$elem};
            next;
        }

        #warn Dumper \%inventory;

        my $still_needed = $production_q{$elem} - $inventory{$elem};
        $inventory{$elem} = 0;

        #say "not enough inventory, need to produce $still_needed";

        my $prod_rounds = int( $still_needed / $bom{$elem}{'prod_qty'} );

        if ( int( $still_needed / $bom{$elem}{'prod_qty'} ) * $bom{$elem}{'prod_qty'} == $still_needed ) {
            $prod_rounds = int( $still_needed / $bom{$elem}{'prod_qty'} );
        }
        else {
            $prod_rounds = int( $still_needed / $bom{$elem}{'prod_qty'} ) + 1;
        }

        #say "need $prod_rounds prod rounds, producing...";
        $inventory{$elem} += ( $prod_rounds * $bom{$elem}{'prod_qty'} ) - $still_needed;

        #warn Dumper \%inventory;
        delete $production_q{$elem};

        for my $elem2 ( keys %{ $bom{$elem}{'need_qty'} } ) {

            #say "need to produce elem $elem2";
            if ( $elem2 eq 'ORE' ) {
                $inventory{'ORE'} += $bom{$elem}{'need_qty'}{'ORE'} * $prod_rounds;
            }
            else {
                $production_q{$elem2} += $bom{$elem}{'need_qty'}{$elem2} * $prod_rounds;
            }
        }

    }

    return $inventory{'ORE'};
}

say "Part 1 : ".produce( 'FUEL', 1 );

# got this by manually testing different numbers
say "Part 2 : 4436981 =>".produce( 'FUEL', 4436981 );
say "Part 2 : 4436982 =>".produce( 'FUEL', 4436982 );
