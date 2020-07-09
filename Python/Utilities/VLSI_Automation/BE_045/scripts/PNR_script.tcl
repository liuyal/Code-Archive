# Get period
set fp [open "./inputs/square_root.sdc" r]
set file_data [read $fp]
close $fp
set start_index [string first "-period" $file_data]
set end_index [string first "-waveform " $file_data]
set period [string range $file_data $start_index+8 $end_index-1]
puts $period

# Get floorplan density
set fp [open "./scripts/01-powerPlan.tcl" r]
set lines [split [read $fp] "\n"]
close $fp
foreach line $lines {
	set index [string first "floorPlan" $line]
	set index2 [string first "#" $line]
	if {$index > -1 && $index2 < 0} {
		set found_line $line 
	}
}
set density [lindex [split $found_line " "] 3]


# Start PNR
set TIME_start [clock clicks -milliseconds]
source scripts/00-import_design.tcl
source scripts/01-powerPlan.tcl
source scripts/02-powerPlan.tcl
source scripts/04-placement.tcl
source scripts/05-postPlaceOpt.tcl
source scripts/06-cts.tcl
source scripts/07-postCTSOpt.tcl
source scripts/08-route.tcl
source scripts/09-finishing.tcl
set TIME_taken [expr [clock clicks -milliseconds] - $TIME_start]


# Create output file
set output [string cat "Total Run time: " $TIME_taken "ms"]
set output2 [string cat "Period: " $period "ns"]
set output3 [string cat "Density: " $density "%"]
puts "*********************************************************"
puts " $output"
puts " $output2"
puts " $output3"
puts "*********************************************************"

set outfile [open "./results/CPU_run_time.txt" w]
puts $outfile "$output"
puts $outfile "$output2"
puts $outfile "$output3"
close $outfile

file mkdir ./results/images

dumpPictures -dir ./results/images -fullScreen -prefix pnr.gif 

exit
