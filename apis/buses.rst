ierr, cmpval = gendat(ibus)
ierr, ival = macind(ibus, id)
ierr, ival = lodint(ibus, id, string)

flag, string = 2,'NUMBER'
ierr, iarray = abusint(sid, flag, string)

ierr, ival = brnint(ibus,jbus,ickt,string)
ierr, carray = abrnchar(sid, owner, ties, flag, entry, string)


flag, string = 4,'NUMBER'
ierr, iarray = amachint(sid, flag, string)

flag, string = 4,'NUMBER'
ierr, iarray = alodbusint(sid, flag, string)


flag, string = 4, 'NUMBER'
ierr, iarray = aswshint(sid, flag, string)

flag, string = 4, 'NUMBER'
ierr, iarray = afxshuntint(sid, flag, string)

owner, ties, flag, string = 1,1,2,'FROMNUMBER'
ierr, iarray = aflowint(sid, owner, ties, flag, string)
owner, ties, flag, string = 1,1,2,'TONUMBER'
ierr, iarray = aflowint(sid, owner, ties, flag, string)

flag, string = 2,'NUMBER'
ierr, iarray = aindmacbusint(sid, flag, string)