#!/usr/bin/perl

# test.pl  07/20/18 11:31:03  leiyang@novogene.com

use strict;
use warnings;
use Getopt::Long;
use Pod::Usage;

my ($help, $break, $bam);
GetOptions(
	'help'=>\$help,
	'break:s'=>\$break,
	'bam:s'=>\$bam,
);

pod2usage 1 if($help);

my %hash;
open FL,"$break";
while(<FL>){
	chomp;
	my @tem = split /\t/;
	$hash{$tem[0]} = $tem[1];
}
close FL;

open PID,"samtools view $bam |";
while(<PID>){
	chomp;
	my @tem = split /\t/;
	
	if($tem[6] eq '='){
		$tem[6] = $tem[2];
	}

	if($hash{$tem[2]}){
		if($tem[3] <= $hash{$tem[2]}){
			$tem[2] = "$tem[2]_1";
		}else{
			$tem[3] -= $hash{$tem[2]};
			$tem[2] = "$tem[2]_2";
		}
	}
	
	if($hash{$tem[6]}){
		if($tem[7] <= $hash{$tem[6]}){
			$tem[6] = "$tem[6]_1";
		}else{
			$tem[7] -= $hash{$tem[6]};
			$tem[6] = "$tem[6]_2";
		}
	}
	if($tem[6] eq  $tem[2]){
		$tem[6] = '=';
	}
	print +(join "\t",@tem[0 .. 10]),"\n";
}
close PID;

=head1 SYNOPSIS

test.pl --help

=head1 OPTIONS

 --help        help
=cut

