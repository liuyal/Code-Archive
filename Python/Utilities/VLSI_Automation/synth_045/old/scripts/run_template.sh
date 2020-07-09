#!/bin/bash


source /etc/profile.d/ensc-cmc.csh
source /CMC/setups/CDS_setup.csh
source /CMC/setups/FE_setup.csh

dc_shell-xg-t -f scripts/synth.tcl

echo "done"