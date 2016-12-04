use strict;
use warnings;
use Cwd qw(cwd);
use File::Copy qw(copy);

sub execute($) {
	my $cmd = shift;
	system($cmd);
	use Carp qw(croak);
	croak "\n\nError executing \n\t'$cmd'\n\n" if ( ( $? >> 8 ) != 0 || $? == -1 || ( $? & 127 ) != 0 );
}

my $header = qq(
OPT	+=  -DUNEQUALSOFTENINGS
OPT	+=  -DMULTIPLEDOMAINS=64
OPT	+=  -DTOPNODEFACTOR=3.0
OPT	+=  -DPEANOHILBERT
OPT	+=  -DWALLCLOCK
OPT	+=  -DMYSORT
OPT	+=  -DDOUBLEPRECISION
OPT	+=  -DNO_ISEND_IRECV_IN_DOMAIN
OPT	+=  -DFIX_PATHSCALE_MPI_STATUS_IGNORE_BUG
OPT	+=  -DOUTPUTPOTENTIAL
OPT	+=  -DOUTPUTACCELERATION
OPT	+=  -DHAVE_HDF5
);

sub build() {
	execute("cd src; make clean; make -j12");
}

open my $fdOut, '>', 'src/gadget.make' or die;
print $fdOut $header;
close $fdOut;
build();
copy('src/Gadget3', 'nogas/') or die;
copy('src/Gadget3', 'gas/') or die;

open $fdOut, '>', 'src/gadget.make' or die;
print $fdOut qq(
$header
OPT	+=  -DSFR
OPT	+=  -DCOOLING
OPT	+=  -DGENERATIONS=1
OPT	+=  -DMOREPARAMS
OPT	+=  -DSTELLARAGE
);
close $fdOut;
build();
copy('src/Gadget3/Gadget3', 'gas+sfr/') or die;