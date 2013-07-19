#!/usr/bin/perl

use strict;
use warnings;

use JSON;
use CGI;

use network;

my $q = CGI->new();
my %data = $q->Vars;

=cut
for my $param (qw( u_name u_surname u_lastname u_sex
				   u_login u_passw u_email u_about u_role)) {
	$data->{ $param } = $q->param($param);
}
=cut

my $server = network->new();
$server->send_data(%data);

print $q->header("application/json");
print to_json(\%data);
# TODO: Обработать входящие данные
