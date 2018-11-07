#!/usr/bin/env perl 

use strict;
use warnings;
use Getopt::Long;
my ($file,$out)=@ARGV;
  if ($file =~ /\.gz$/){
    open (IN,"zcat $file |") or die "Couldn't read $file : $!";  
  }
  elsif ($file =~ /\.bam$/) {
      #open (IN,"samtools view $file |") or die "Couldn't read $file: $!";
      open (IN,"cat $file |") or die "Couldn't read $file: $!";
  }
  else{
    open (IN, $file) or die "Could not open $file\n";
  }
  
  open (OUT, '>', "$out") or die "Could not write to $out!";
  
  while(<IN>){
    if(/^@/){    #Remove SAM header lines
      next;
    }
    
    my $readF = $_;
    my $readR = scalar <IN>;
    
    my $chromosomeF = (split(/\t/, $readF))[2];
    my $chromosomeR = (split(/\t/, $readR))[2];
    my $positionF = (split(/\t/, $readF))[3];
    my $positionR = (split(/\t/, $readR))[3];
    my $seqF = (split(/\t/, $readF))[9];
    my $seqR = (split(/\t/, $readR))[9];
	my $readid=(split(/\t/, $readF))[0];

    my $strandF;
    my $strandR;

    if(((split(/\t/,$readF))[1]) & 0x10){    #Analyse the SAM bitwise flag to determine strand
      $strandF = '-';    #Negative strand   
      $positionF = $positionF + length($seqF) - 1;
    }else{
      $strandF = '+';    #Positive strand
    }

    if(((split(/\t/,$readR))[1]) & 0x10){    #Analyse the SAM bitwise flag to determine strand
      $strandR = '-';    #Negative strand
      $positionR = $positionR + length($seqR) - 1;
    }else{
      $strandR = '+';    #Positive strand
    }

    print OUT "$readid\t$chromosomeF\t$positionF\t$strandF\t$chromosomeR\t$positionR\t$strandR\n";
}
  close IN;
  close OUT;


