#!/usr/bin/env perl
#
#print $#ARGV;
if ($#ARGV < 1){
    print("Usage: make_syn.pl project_dir model/evdp[/k|f]\n");
    exit(1);
}

$ddir = $ARGV[0];
$mod = $ARGV[1];
open(WEI, "<$ddir/weight.dat") or die("cannot find the project: $ddir\n");
$cmd = "fk.pl -M$mod -N2048/0.2 ";
foreach $sta (<WEI>){
    chomp $sta;
    @junk = split(" ", $sta);
    $cmd = $cmd.$junk[1]." ";
}
print("$cmd\n");
system("$cmd");
