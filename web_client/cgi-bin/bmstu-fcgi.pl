#!/usr/bin/perl

use strict;
use warnings;

use JSON;
use FCGI;
use FCGI::ProcManager qw( pm_manage pm_pre_dispatch pm_write_pid_file pm_post_dispatch );
use File::Basename qw( basename );
use IO::Socket::INET;
use IO::Socket::SSL;

(my $basename = basename $0) =~ s/\.pl$//;
my $pidfile = "$basename.pid";
my $logfile;

my $config = {
    LISTEN_ADDR         => "/var/run/fcgi/$basename.socket",
    PIDFILE             => "/var/run/fcgi/$pidfile",
    THREADS_COUNT       => 4,
    DEBUG               => 1,
    DAEMONIZE           => 0,
    USER                => 'nobody',
    GROUP               => 'nogroup',
    MANAGER_NAME        => "$basename-process-manager",
    WORKER_NAME         => "$basename-worker",
    HOST                => "127.0.0.1",
    PORT                => "5000",
    SSL_ENABLED         => 0,
    DATA_MAX_LEN        => 32 * 1024,
};

run();

############################## Entry point ############################

sub main_loop {
    my ($uri, $params, $socket) = @_;
    my $msg = _log("$uri?$params");
    print "Content-Type: application/json\r\n\r\n";
    print $msg;
}

############################ Actions ################################

sub prepare_callback {

}

sub act_register_person {

}

sub act_recister_account {

}

sub act_login {

}

sub act_get_user_info {

}

############################## General subs ############################

sub _err { _log("Error: " . (shift)); }
sub _log {
    my $msg = shift;
    if ($config->{DEBUG}) {
        unless (defined $logfile) {
            open $logfile, ">>/var/log/$basename.log" or die "$!\n";
            autoflush $logfile;
        }
        print $logfile ($msg = (scalar localtime) . " [$$]: $msg\n");
        print $msg unless $config->{ DAEMONZE };
    }
    $msg;
}

sub daemonize {
    chdir '/'                 or die "Can't chdir to /: '$!'\n";
    for my $handle (*STDIN, *STDOUT, *STDERR){
        open ($handle, '+<', '/dev/null' ) || 
            die "Can't reopen $handle to /dev/null: '$!'\n";
    }
    defined(my $pid = fork)   or die "Can't fork: '$!'\n";
    exit if $pid;
    POSIX::setsid()           or die "Can't start a new session: '$!'\n";
}

sub change_user {
    my $uid = getpwnam($config->{ USER }) || 
        die _err("Cannot get uid for $config->{ USER }\n");
    my $gid = getgrnam($config->{ USER }) || 
        die _err("Cannot get gid for $config->{ USER }\n");
    POSIX::setuid($uid) or die _err("Can't set uid($uid): '$!'\n");
    POSIX::setuid($gid) or die _err("Can't set gid($gid): '$!'\n");
    check_if_pid_file_can_be_created();
    return 1;
}

sub check_for_another_running_processes {
    if (-f $config->{ PIDFILE }) {
        if(open my $fhr,'<',$config->{ PIDFILE }) {
            chomp (my $pid = <$fhr>);
            if (kill 0,$pid) {
                die "already running with pid $pid\n";
            }
        }
    }
}

sub check_if_pid_file_can_be_created {
    open my $fh, '>', $config->{ PIDFILE } 
        or die "Can't create pid file at '$config->{PIDFILE}' " .
            "from user '$config->{USER}'\n";
    unlink $config->{PIDFILE};
}

sub establish_connection {
    my $socket;
	my $err = "Error while establishing connection to server " .
			  "$config->{ HOST }:$config->{ PORT }: %s";
    _log "$$: establishing connection to $config->{ HOST }:$config->{ PORT }";
    if ($config->{ SSL_ENABLED }) {
        $socket = IO::Socket::SSL->new(
                PeerHost    => $config->{ HOST },
                PeerPort    => $config->{ PORT },
                SSL_verify_mode => IO::Socket::SSL::SSL_VERIFY_PEER,
            ) or return _log(sprintf $err, $!);
    } else {
        $socket = IO::Socket::INET->new(
                PeerHost    => $config->{ HOST },
                PeerPort    => $config->{ PORT },
                Proto       => 'tcp',
            ) or return _log(sprintf $err, $!);
    }
    $socket;
}

sub send_json {
    my ($socket, $data) = @_;
    _log("Sending data:  $data");
    $socket->send($data);
}

sub send_data {
    my ($socket, $data) = @_;
    $data = { data => $data } if ref($data) ne "HASH";
    send_json($socket, to_json($data) . "\r\n");
}

sub recv_json {
    my $socket = shift;
    my $data;
    $socket->recv($data, $config->{ DATA_MAX_LEN });
    _log("Data recieved: $data");
    $data;
}

sub recv_data {
    my $data = recv_json(shift);
    $data = decode_json $data if defined $data;
    $data;
}

sub run {
    die "Run program as root!\n" if (getpwuid $>) ne 'root';

    umask 0;
    my $socket = FCGI::OpenSocket($config->{ LISTEN_ADDR }, 10) 
        or die "Can't open port $config->{ LISTEN_ADDR } for listening $!";
    my $request = FCGI::Request(\*STDIN, \*STDOUT, \*STDERR, \%ENV, $socket,  
                                FCGI::FAIL_ACCEPT_ON_INTR());

    check_for_another_running_processes();
    daemonize if $config->{ DAEMONIZE };
    pm_write_pid_file $config->{ PIDFILE };

    _log("Manager started: $$");

    change_user;
    pm_manage( n_processes => $config->{THREADS_COUNT}, 
               pm_title => $config->{ MANAGER_NAME } );
    $0 = $config->{ WORKER_NAME };
    _log("Worker started: $$");

    my $server_socket = establish_connection;

    while ($request->Accept() >= 0) {
        pm_pre_dispatch();
        main_loop $ENV{DOCUMENT_URI}, $ENV{QUERY_STRING}, $socket;
        pm_post_dispatch();
    }
    FCGI::CloseSocket($socket);
    _log("Finished: $$");
}
