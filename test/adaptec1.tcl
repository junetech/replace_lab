set design adaptec1_lefdef
set bench_dir ./ispd2005/adaptec1/

replace_external rep

# Import LEF/DEF files
rep import_lef ${bench_dir}/${design}.lef
rep import_def ${bench_dir}/${design}.def
rep set_output ./output/

# Initialize RePlAce
rep init_replace

# place_cell with Nesterov method
rep place_cell_nesterov_place

# Export DEF file
rep export_def ./${design}_placed.def

puts "nesterovPlace HPWL: [rep get_hpwl]"
puts "final WNS: [rep get_wns]"
puts "final TNS: [rep get_tns]"

exit
