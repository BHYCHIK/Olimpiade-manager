#!/usr/bin/perl

use strict;
use warnings;

use IO::Socket::INET;
use IO::Socket::SSL;

use config;
our $config;

use debugger;

package network;
use base qw( Exporter );

use JSON;

our @EXPORT = qw( new send_data send_json 
				  recv_data recv_json );
my $socket;
my $connections_count = 0;

sub establish_connection {
	my $self = shift;
	
	return $socket if defined $socket;

	my $s;
	my $err = "Error while establishing connection to server " .
			  "$config->{ host }:$config->{ port }\n";
	$self->{ debugger }->log("Establishing connection...") 
		if $self->{ debugger };
	if ($config->{ ssl_enabled }) {
# TODO: SSL sockets works incorrectly =(
		$s = IO::Socket::SSL->new(
				PeerHost	=> $config->{ host },
				PeerPort	=> $config->{ port },
				SSL_verify_mode => IO::Socket::SSL::SSL_VERIFY_PEER, 
			) or die $err . $! . "\n";
	} else {
		$s = IO::Socket::INET->new(
				PeerAddr	=> $config->{ host },
				PeerPort	=> $config->{ port },
				Proto		=> 'tcp',
			) or die $err . $! . "\n";
	}
	$self->{ debugger }->log("Connection established.");
	$socket = $s;
}

sub send_json {
	my $self = shift;
	my $data = shift;
	$self->{ debugger }->log("Sending data: ", $data)
		if $self->{ debugger };
	$self->{ socket }->send($data);
}

sub send_data {
	my $self = shift;
	my $data = shift;
	$data = { data => $data } if ref($data) ne "HASH";
	my $json = to_json $data;
	$self->send_json($json . "\r\n");
}

=item recv_json
	Arguments: timeout
	Returns: string 

Function wait data from server timeout seconds
and returns it. If data wasn't recieved, returns undef.
If timeout wasn't passed, socket wait data forever.
=cut
sub recv_json {
	my $self = shift;
	my $timeout = shift;
	$timeout = 0 if !$timeout;
	my $data;
	eval {
		$SIG{ ALRM } = sub { die "Timeout!\n"; };
		alarm $timeout;
		my $remote = $self->{ socket };
		$self->{ socket }->recv($data, $config->{ data_max_len });
		$self->{ debugger }->log("Data recieved: ", $data) 
			if $self->{ debugger };
		alarm 0;
	};
	$data;
}

=item recv_data
	Arguments: timeout
	Returns: hash ref 

Function wait data from server timeout seconds
and returns it. If data wasn't recieved, returns undef.
If timeout wasn't passed, socket wait data forever.
=cut
sub recv_data {
	my $self = shift;
	my $data = $self->recv_json(shift);
	$data = decode_json $data if $data;
	$data;
}

sub new {
	my $class = shift;
	my $is_debug = shift;
	$connections_count++;
	my $self = {};

	bless $self, $class;
	$self->{ debugger } = debugger->new() if $is_debug;
	$self->{ socket } = $self->establish_connection;
	$self;
}

sub DESTROY {
	my $self = shift;
	$self->{ socket }->close 
		if $connections_count == 1;
	$connections_count--;
	$self->{ debugger }->log("Connection closed") 
		if $self->{ debugger };
}

1;
