clear
import delimited "C:\Users\Darrick\Documents\maya\projects\_UE4-Chars\scripts\ai_data\curve_list.csv", encoding(ISO-8859-2) 

rename v1 crv
reshape long v@, i(crv)

gen x = (_j - 14)  / 12
gen x2 = x^2

levelsof crv, local(crvs)
local numcrvs: word count `crvs'

mat LT0 = J(`numcrvs', 3, .)
mat GE0 = J(`numcrvs', 3, .)
mat rownames LT0 = `crvs'
mat rownames GE0 = `crvs'

foreach cname of local crvs {
	qui sum v if crv == "`cname'" & x == 0
	local cval = round(`r(mean)', .001)
	qui sum v if crv == "`cname'" & x == -1
	local lval = round(`r(mean)', .001)
	qui sum v if crv == "`cname'" & x == 1
	local uval = round(`r(mean)', .001)
	
	constraint 1 _cons = `cval'
	constraint 2 `cval'- x + x2 = `lval'
	constraint 3 `cval' + x + x2 = `uval'
	
	qui cnsreg v x x2 if x <= 0 & crv == "`cname'", c(1 2)
	local r2 = round(e(r2), .01)
	if `r2' < .98 {
		di "`cname': `r2'"
	}
	mat LT0[rownumb(LT0, "`cname'"), 1] = e(b)
	// qui reg v c.x##c.x if x >= 0 & crv == "`cname'"
	qui cnsreg v x x2 if x >= 0 & crv == "`cname'", c(1 3)
	local r2 = round(e(r2), .01)
	if `r2' < .98 {
		di "`cname': `r2'"
	}
	mat GE0[rownumb(GE0, "`cname'"), 1] = e(b)
}

mat OUT = LT0[1..., 3], LT0[1..., 1..2], GE0[1..., 3], GE0[1..., 1..2]
mat colnames OUT = "lt0" "lt1" "lt2" "ge0" "ge1" "ge2"
mat li OUT
putexcel set "C:\Users\Darrick\Documents\maya\projects\_UE4-Chars\scripts\ai_data\crv_coefs", replace
putexcel A1 = matrix(OUT), rownames