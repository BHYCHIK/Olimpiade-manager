#!/usr/bin/perl

use strict;
use warnings;

use JSON;
use CGI;

use network;

my $q = CGI->new();
my %data = $q->Vars;

my $server = network->new();
$server->send_data(\%data);

print $q->header("application/json");
print $server->recv_json . "\n";
# TODO: Обработать входящие данные
