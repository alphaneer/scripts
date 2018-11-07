use strict;
#use warnings;

my $in=shift;
open IN,"$in" or die "$!";
print $in,"\t";
while(my $line=<IN>){
	chomp $line;
	my @info=split(/\t+/,$line);
	if($info[0]=~/^Number/ && $info[0]=~/clusters/){
		my $contig_n=$info[1];
		$info[2]=~/\((\d+\.?\d+)%/;
		my $contig_p=$1;
		print $contig_n,"\t",$contig_p,"\t";
	}elsif($info[0]=~/^Length/ && $info[0]=~/clusters/){
		my $chr_l=$info[1];
		$info[2]=~/\((\d+\.?\d+)%/;
		my $chr_p=$1;
		print $chr_l,"\t",$chr_p,"\t";
	}elsif($line=~/\|\s+0\s+\|\s+\d+\s+\|\s+(\d+)\s+\|/){
		my $len_max=$1;
		print $len_max,"\t";
	}elsif($line=~/\|\s+7\s+\|\s+\d+\s+\|\s+(\d+)\s+\|/){
		my $len_min=$1;
		print $len_min,"\t";
	}elsif($info[0]=~/^Number/ && $info[0]=~/trunks/){
		my $trunk_n=$info[1];
		$info[2]=~/\((\d+\.?\d+)%/;
		my $trunk_p=$1;
		print $trunk_n,"\t",$trunk_p,"\t";
	}elsif($line=~/^Length/ && $info[0]=~/trunks/){
		my $trunks_len=$info[1];
		$info[2]=~/\((\d+\.?\d+)%/;
		my $trunks_per=$1;
		print $trunks_len,"\t",$trunks_per,"\n";
	}
}
close IN;
