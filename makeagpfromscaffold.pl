#!/usr/bin/perl

if(@ARGV<2)
  {
    print "$0 scaffold pre\n";
    exit;
  }
 open(IN, "$ARGV[0]") or die;
 open(OUT1,">$ARGV[1].agp") or die;
 open(OUT2,">$ARGV[1].ctg.fasta") or die;
 $/=">";
 <IN>;
 while($line=<IN>)
   { $m=0;
     $line=~s/>$//;
     @array=split /\n/, $line,2;
     $scaname=(split /\s+/, $array[0],2)[0];
     $array[1]=~s/\s+//g;
     $seq1=$array[1];
     $seq2=$array[1];
     undef @gaps;
     while($seq1=~/([nN]+)/g)
        {
          push(@gaps,$1);
        }
      @contigs=split /[nN]+/, $seq2;
      $numgaps=@gaps;
      $numcontigs=@contigs;
      $basecoor=0;
      for($i=0;$i<@contigs;$i++)
        {
        	 if($i != @contigs-1)
        	   {
        	   	 $len=length($contigs[$i]);
        	   	 $start1=$basecoor+1;
        	   	 $end1=$basecoor+$len; 
        	   	 $contigm++;
        	   	 $m++;
        	   	 $basecoor=$end1;
        	   	 print OUT1 "$scaname\t$start1\t$end1\t$m\tW\t${scaname}_$contigm\t1\t$len\t+\n";
        	   	 print OUT2 ">${scaname}_$contigm\n$contigs[$i]\n";
        	   	 $len=length($gaps[$i]);
        	   	 $start1=$basecoor+1;
        	   	 $end1=$basecoor+$len;
        	   	 $m++;
        	   	 $basecoor=$end1;
        	   	 print OUT1 "$scaname\t$start1\t$end1\t$m\tN\t$len\tfragment\tyes\n";
        	   }else
        	   {
        	   	 $len=length($contigs[$i]);
        	   	 $start1=$basecoor+1;
        	   	 $end1=$basecoor+$len; 
        	   	 $contigm++;
        	   	 $m++; 
               print OUT1 "$scaname\t$start1\t$end1\t$m\tW\t${scaname}_$contigm\t1\t$len\t+\n";
               print OUT2 ">${scaname}_$contigm\n$contigs[$i]\n";
             } 
        }
        $contigm=0;
    }      
    
