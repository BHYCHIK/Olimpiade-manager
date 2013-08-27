#!/usr/bin/perl

use strict;
use warnings;

use JSON;
use CGI;

my $q = CGI->new();
my %data = $q->Vars;
my %result;

local $/ = undef;
for (keys %data) {
    if (open my $f, $data{$_}) {
        $result{ $_ } = <$f>;
    } else {
        $result{ $_ } = "Error openning $_ file: $!";
    }
}

print to_json(\%result);
