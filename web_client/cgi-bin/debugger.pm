#!/usr/bin/perl

use strict;
use warnings;

package debugger;
use base qw( Exporter );

use Data::Dumper;

sub new {
    my $class = shift;
    my $f_name = shift;
    $f_name = "/tmp/debug.log" if !$f_name;

    open my $h, ">", $f_name 
        or die "Error while openning log file: $!";

    my $self = { file => $h };
    bless $self, $class;
}

sub log {
    my $self = shift;
    print { $self->{ file } } Dumper(@_) . "\n"
}

sub DESTROY {
    my $self = shift;
    close $self->{ file };
}

1;
