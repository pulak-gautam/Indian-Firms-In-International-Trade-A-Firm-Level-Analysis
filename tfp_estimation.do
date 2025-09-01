* Load the cleaned CSV file
import delimited "C:\\classfn_4064_final.csv", clear

* Create separate observations for current and previous years
preserve
gen time_var = 1 // Current year
tempfile current
save `current'

* Restore and adjust for previous year data without redefining time_var
restore
replace current_total_annual_sales = last_year_total_annual_sales
replace current_total_employment = previous_total_employment
replace inter_in = prev_inter_in
replace capital = previouscapital
gen time_var = 0 // Set time_var for previous year only

* Append current year data to previous year data
append using `current'

* Generate log transformations
gen lnoutput = ln(current_total_annual_sales)
gen lnlabor = ln(current_total_employment)
gen lncapital = ln(capital)
gen lnintermediate = ln(inter_in)

* Set the panel structure using idstd and time_var
xtset idstd time_var

* Estimate TFP using the Levinsohn-Petrin method in prodest
prodest lnoutput, method(lp) free(lnlabor) proxy(lnintermediate) state(lncapital) poly(3) valueadded reps(250)
