#!/usr/bin/perl

use strict;
use warnings;

use JSON;
use FCGI;
use FCGI::ProcManager qw( pm_manage pm_pre_dispatch pm_write_pid_file pm_post_dispatch );
use File::Basename qw( basename );
use IO::Socket::INET;
use IO::Socket::SSL;
use Cache::Memcached;

(my $basename = basename $0) =~ s/\.pl$//;
my $pidfile = "$basename.pid";
my $logfile;
my $cache;

my $config = {
    WORK_DIR            => "/var/run/fcgi/",
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
    MEMCACHED_SERV_LIST             => ['127.0.0.1:11211'],
    MEMCACHED_DEBUG                 => 0,
    MEMCACHED_COMPRESS_THRESHOLD    => 10_000,
};

run();

############################## Entry point ############################

sub main_loop {
    my ($uri, $params, $actions, $socket) = @_;
    _log("$uri?$params");
    print "Content-Type: application/json\r\n\r\n";

    my %p = $params =~ /(\w+)=([\w\d.@]+)&?/g;

    return _err("Action is required") unless $p{ action };
    return _err("Action not found") unless $actions->{ $p{ action } };

    my $r = $actions->{ $p{ action } }->{ handler }->( $socket, \%p );
    print to_json $r if ref $r eq 'HASH'
}

############################ Actions ################################

sub prepare_callbacks {
    my $actions = {};
    
    $actions->{ login }->{ handler } = \&act_login;
    $actions->{ register_person }->{ handler } = \&act_register_person;
    $actions->{ register_account }->{ handler } = \&act_register_account;
    $actions->{ get_user_info }->{ handler } = \&act_get_user_info;

    $actions;
}

sub act_register_person {

}

sub act_register_account {

}

sub act_login {
    my ($socket, $params) = @_;

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

sub hash_to_str {
    my $data = shift;
    my $r = "";
    for (keys %$data) {
        $r .= "$_: $data->{ $_ }, ";
    }
    $r =~ s/, $//;
    $r;
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
            my $pid = <$fhr>;
            if ($pid) {
                chomp $pid;
                die "already running with pid $pid\n" if kill 0, $pid;
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
    _log("$$: establishing connection to $config->{ HOST }:$config->{ PORT }");
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
    if (ref $data eq 'HASH') {
        $data->{ id } = rand 1000 unless $data->{ id };
    }
    _log("Sending data:  $data");
    $socket->send($data);
}

sub send_data {
    my ($socket, $data) = @_;
    $data = { data => $data } if ref($data) ne "HASH";
    $data = to_json($data);
    $data =~ s/[\r\n]*$/\r\n/;
    send_json($socket, $data);
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
    $data =~ s/[\r\n]*$//;
    $data = from_json $data if defined $data;
    $data;
}

sub listen_socket {
    my $socket = shift;
    while (my $data = recv_data $socket) {
        my $id = $data->{ id };
        unless (defined $id) {
            _err("Id is required: " . hash_to_str($data));
            next;
        }
        $cache->set($basename . "_$data->{ id }", $data);
    }
}

sub has_key {
    my $key = shift;
    return 1 if $cache->get($basename . "_$key");
    return 0;
}

sub run {
    die "Run program as root!\n" if (getpwuid $>) ne 'root';

    my $memcached = sub {
        my $cache = new Cache::Memcached {
                'servers'     => $config->{ MEMCACHED_SERV_LIST },
                'debug'       => $config->{ MEMCACHED_DEBUG },
                'compress_threshold' => $config->{ MEMCACHED_COMPRESS_THRESHOLD },
        };
        die _err "Unable to connect to Memcached" unless
            $cache->set("test_" . rand $$ * 1000, 1);
        $cache;
    };

    mkdir $config->{ WORK_DIR };
    umask 0;
    my $socket = FCGI::OpenSocket($config->{ LISTEN_ADDR }, 10) 
        or die "Can't open port $config->{ LISTEN_ADDR } for listening $!";
    my $request = FCGI::Request(\*STDIN, \*STDOUT, \*STDERR, \%ENV, $socket,  
                                FCGI::FAIL_ACCEPT_ON_INTR());

    check_for_another_running_processes();
    daemonize if $config->{ DAEMONIZE };
    pm_write_pid_file $config->{ PIDFILE };

    my $server_socket = establish_connection;
    my $actions = prepare_callbacks;

    unless (fork) {
        _log("Socket listener started: $$");
        $cache = $memcached->();
        return listen_socket $server_socket;
    }

    _log("Manager started: $$");

    pm_manage( n_processes => $config->{ THREADS_COUNT }, 
               pm_title => $config->{ MANAGER_NAME } );
    change_user;
    $0 = $config->{ WORKER_NAME };
    _log("Worker started: $$");

    $cache = $memcached->();

    while (1) {
        sleep rand($$) % 5;
        send_data($server_socket, {id => int(rand $$ * 9999), cmd => 'onp_ping'});
    }

    while ($request->Accept() >= 0) {
        pm_pre_dispatch();
        main_loop $ENV{DOCUMENT_URI}, $ENV{QUERY_STRING}, $actions, $socket;
        pm_post_dispatch();
    }
    FCGI::CloseSocket($socket);
    _log("Finished: $$");
}
