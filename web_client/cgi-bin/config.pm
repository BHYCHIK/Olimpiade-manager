#!/usr/bin/perl

use strict;
use warnings;

package config;
use base qw( Exporter );

our @EXPORT = qw ( $config );

our $config = {
	host		=> "127.0.0.1",
	port		=> "5000",
	ssl_enabled	=> 0,
	data_max_len=> 32 * 1024,
};
