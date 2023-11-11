#!/usr/bin/perl -w
# Fortinet EMEA Support
# This script convert a fgt verbose 3 sniffer output file to
# a file that can be opened by Ethereal. It uses text2pcap binary.

  my $version 		      = "2.0 (06/19/06)";
  
# Enter you prefered system (avoid setting -system option when calling script)
  my $prefered_system 	= 'linux' ;  # can be either 'linux' or 'windows'

# Path to the linux text2pcap
  my $text2pcapdirlinux	= "/usr/bin";
  
# Path to the windows text2pcap.exe
# You need to double character '\'
  my $text2pcapdirwin   = "c:\\Progra~1\\wireshark";
 
# ------------------ don't edit after this line -------------------------------
  use strict;
  use Getopt::Long;
  use FileHandle;
  use vars qw ($debug $help $vers $in $out $lines $system);

# Global variables

  my $line_count		        = 0;
  my ($fh_in, $fh_out)  	      	= new FileHandle;
  my @fields 			        = {};
  my @subhexa 			        = {};
  my ($offset,$hexa,$garbage) 		= "";
  my @list 				= {};
  my $numArgs;
  my $OSversion				= "";
  my $tmp				= "";
  
# Control command line options

#   GetOptions(
#	"debug"	  	=> \$debug,	# use -debug to turn on debug
# 	"version"   	=> \$vers,    	# use -version to display version
#	"help" 	  	=> \$help,	# use -help to display help page
#	"in=s"    	=> \$in,	# use -in  <filename> to specify an input file
#	"out=s"   	=> \$out,	# use -out <filename> to specify an output file
#	"lines=i"  	=> \$lines,	# use -lines <number> to stop after <number> lines written
#	"system=s" 	=> \$system	# use - system to specify 'linux' or 'windows' system
#	);
	
  $numArgs = $#ARGV + 1;
  $OSversion =  $^O;
  $in = $ARGV[0];
  $out = $ARGV[1];

  # print "in is ---> $in <-----\n";
  # print "out is ---> $out <-----\n";
  # print "os is ---> $^O <----\n";  
  # if ($in = ~/help/)
  #{
  #   Print_help();
  #   exit;
  #}

  #if ($in = ~/version/)
  #{
#	  Print_verion();
#	  exit;
  # }
    print "system is ---> $system 1<==\n";
  $tmp = $OSversion;
  
  if ($tmp =~ m/MSWin32/)
  {
	  $system = "windows";
  }
    print "system is ---> $system 2<==\n";
  $tmp = $OSversion;

  if ($tmp =~ m/linux/)
    {
	    $system = "linux";
    }

    print "system is ---> $system 3<==\n";
#  if ($help) {
#    Print_help();
#    exit;
#    }
    
#  if ($vers) {
#    Print_version();
#    exit;
#    }
    
# Sanity checks

  if (not(defined($in))) {
    Print_usage();
    exit;
    }

#  if (defined($system)) {
#    die "non authorized system specified"
#      if (not($system =~ /linux|windows/));
#    }
    
# Open input file for reading, open output file for writing

  printf "Called with input filename ".$in."\n" if $debug;
  $out = "output.eth" if (not(defined($out)));
  printf "Output file is ".$out."\n" if $debug ;
  
  open(fh_in,  '<', $in)  or die "Cannot open file ".$in." for reading\n";
  open(fh_out, '>', "output.tmp") or die "Cannot open file output.tmp for writing\n";

# Convert

  printf "Conversion of file ".$in." phase 1 (FGT verbose 3 conversion)\n";

  LINE: while (<fh_in>) {
    #Initialisation
    $offset = "";
    $hexa = "";
    $garbage = "";
    @list = {};

    chomp;
    # Keep timestamps.
    if ($_ =~ /^([0-9]+)\.([0-9]+) /)
    {
        my $packet = 1;
        my $time = $1;
        my $sec = $time % 60;
        $time -= $sec;
        my $minute = ($time / 60) % 60;
        $time -= $minute * 60;
        my $hour = ($time % (60 * 60));
        print fh_out $hour . ":" . $minute . ":" . $sec . ".$2\n";
    }
    next if not(/^0x/);         		# skip all lines not started with '0x'
    s/^0x//;                    		# delete Ox in the beginning of each lines

    if ($debug) {
      printf "------------------------------------------------------------\n" if ($offset eq "0000");
      printf "-->".$_."\n";
      }
    

    # extract each hexa code from hexacode part

    @fields = {};
    @fields  = $_ =~ /
      ^(\w{4})                    # offset of 4 digits
        \s+(\w{0,2})(\w{0,2})     # 1st group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 2st group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 3rd group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 4th group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 5th group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 6th group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 7th group of 4 chars if any
        \s+(\w{0,2})(\w{0,2})     # 8th group of 4 chars if any
        \s                        # space
        */x;                      # Crap

    printf fh_out "00".$fields[0]." ";    			# Write Offset to output file
    printf $line_count." : 00".$fields[0]." " if $debug;

    for (my $i=1;$i<17;$i++) {
      if (defined($fields[$i])){
        if ($fields[$i] ne '') {
            printf fh_out $fields[$i]." ";
            printf $fields[$i]." " if $debug;
            }
        }
      else {print "** " if $debug};
      }
    print fh_out "\n";          				# Write end of the line
    print "\n\n" if $debug;

    $line_count++;
    if (defined($lines)) {
      if ($line_count >= $lines) {
        print "Reached max number of lines to write in output file\n";
        last LINE;
        }
      }
    }

# Close files
  close (fh_in)  or die "Cannot close file ".$in."\n";
  close (fh_out) or die "Cannot close file output.tmp\n";

# Calling textpcap (see www.ethereal.com)
  $system = $prefered_system if (not(defined($system)));

  # System is windows :-(
  if ($system eq "windows") {
    my @args = ($text2pcapdirwin."\\text2pcap.exe", "-t", '"%H:%M:%S."', "-q", "output.tmp", $out);
    print "Conversion of file ".$in." phase 2 (windows text2pcap)\n";
    system(@args) == 0 or die "call to text2pcap failed @args failed: $?\n
    The '-system linux' option may be needed ?\n\n"
    }

  # System is linux :-)
  elsif ($system eq "linux") {
   print "Conversion of file ".$in." phase 2 (linux text2pcap)\n";
     system ($text2pcapdirlinux."/text2pcap -q -t \"%H:%M:%S.\" output.tmp ".$out)  == 0 or die "call to text2pcap failed : $?\n
	The '-system windows' option may be needed ?\n\n"
    }
  print "Ouput file to load in Ethereal is \'".$out."\'\n";
	print "End of script\n" if $debug;

#------------------------------------------------------------------------------
 sub Print_usage {
	 return;
  print "Version : $version\n\n";
  print "Usage : fgt2eth.pl -in <input_file_name>\n\n";
  print "Mandatory argument are :\n\n";
  print "   -in  <input_file>     Specify the file to convert (FGT verbose 3 text file)\n\n";
  print "Optional arguments are :\n\n";
  print "   -help                 Display help only\n";
  print "   -version              Display script version and date\n";
  print "   -out <output_file>    Specify the output file (Ethereal readable)\n";
  print "                         By default 'output.eth' is used\n";
  print "   -lines <lines>        Only convert the first <lines> lines\n";
  print "   -system <system>      Can be either linux or windows\n";
  print "   -debug                Turns on debug mode\n";
  }
#------------------------------------------------------------------------------
 sub Print_help {
	 return;
  print "Help:\n\n";
  print "* What is this script for ?\n\n";
  print "   It permits to sniff packets on the fortigate with built-in sniffer\n\n";
  print "      diag sniff interface <interface> verbose 3 filters \'....\'\n\n";
  print "   and to be able to open the captured packets with Ethereal free sniffer.\n\n\n";
  print "* What do I need to know about this script ?\n\n";
  print "   - It can be sent to customers, but it is given as is.\n";
  print "   - No support is available for it as it is not an 'offical' fortinet product.\n";
  print "   - It should run on windows and linux as soon as perl is installed.\n";
  print "     To install perl on windows system,\n";
  print "         go to http://www.activestate.com/Products/ActivePerl/\n";
  print "   - All lines from the source file that do not begin with \'0x\' will be ignored.\n";
  print "   - Be carefull not to add \'garbage\' characters to the file during the sniff.\n";
  print "     If possible do not hit the keyboard during capture.\n\n\n";
  print "* Installation :\n\n";
  print "    You need to edit the script first lines and to specify:\n\n";
  print "       - for linux:    the path to text2pcap in \$text2pcapdirlinux\n";
  print "                       Current settings : $text2pcapdirlinux\n\n";
  print "       - for windows:  the path to text2pcap.exe in \$text2pcapdirwin\n";
  print "                       Current settings : $text2pcapdirwin\n\n";
  print "    You can also specify the \$prefered_system variable (linux or windows)\n";
  print "    For now \'$prefered_system\' is set.\n\n\n";
  print "Remarks concerning this script can be sent to eu_support\@fortinet.com\n";
  print "Thanks to Claudio for this great idea,\nThanks to Ellery from Vancouver Team for the timestamps\n\nCedric\n\n";
  print "____________________________________________________________________________\n\n";
  Print_usage();
 }
#------------------------------------------------------------------------------

sub Print_version {
  print "\nVersion : ".$version."\n\n";
  }
