import sys
import json
sys.path.append(r"C:\DigSILENT15p1p7\python") # set the path to python folder inside your digsilent instalatio folder

# import  PowerFactory  module
import powerfactory


# start PowerFactory  in engine  mode
app = powerfactory.GetApplication('jmmauricio','') # change 'jmmauricio' by your user name and '' by your password

# activate project
project = app.ActivateProject("20150209 SING DB Febrero original")  # change "Nine Bus System" by the name of your project
prj = app.GetActiveProject()    # active project instance

print('prj: {:s}'.format(prj)) # to check if the project is opened properly

ldf = app.GetFromStudyCase("ComLdf")    # Load flow
ini = app.GetFromStudyCase('ComInc')    # Dynamic initialization
sim = app.GetFromStudyCase('ComSim')    # Transient simulations

buses = app.GetCalcRelevantObjects("*.StaBar,*.ElmTerm")
syms = app.GetCalcRelevantObjects("*.ElmSym")
loads = app.GetCalcRelevantObjects("*.ElmLod")
substats = app.GetCalcRelevantObjects("*.ElmSubstat")
##buses = []
##for substat in substats:
##    substat_buses = app.GetCalcRelevantObjects(substat.loc_name + "\*.ElmTerm")
##    print(substat_buses)
##    buses += app.GetCalcRelevantObjects(substat.loc_name + "\*.ElmTerm")
##
elmres = app.GetFromStudyCase('Results.ElmRes')

json_path = r'E:\Documents\public\workspace\pypstools\dev\simple_sing.json'
geo = json.load(open(json_path,'r'))
  
    

buses_names = list(geo['bus'].keys())
syms_names = list(geo['sym'].keys())
# channels for buses
for bus in buses:

        if bus.loc_name.find('220')>0 or bus.loc_name.find('345')>0:
            print(bus.loc_name)
            elmres.AddVars(bus,'m:u'
                           ##    ,'m:phiu'
                           ##    ,'m:fehz'
                           )  # creating channels for:
                              # voltage ('m:u'),  angle ('m:phi') and frequency ('m:fehz')  
        # channels for synchronous machines
##for sym_name in syms_names:
##    
##    obj = app.GetCalcRelevantObjects("{:s}.ElmSym".format(sym_name) )
##    if len(obj)>0:
##        sym=obj[0]
##
##        print(sym_name)
##        elmres.AddVars(sym, 
##    ##                   's:ve',    # p.u  Excitation Voltage
##    ##                   's:pt',    # p.u.   IN    Turbine Power
##                       's:ut',    # p.u.   OUT   Terminal Voltage
##    ##                   's:ie',    # p.u.   OUT   Excitation Current
##                       's:xspeed',# p.u.   OUT   Speed
##    ##                   's:xme',   # p.u.   OUT   Electrical Torque
##    ##                   's:xmt',   # p.u.   OUT   Mechanical Torque
##    ##                   's:cur1',  # p.u.   OUT   Positive-Sequence Current, Magnitude
##                       's:P1',    # MW     OUT   Positive-Sequence, Active Power
##                       's:Q1',    # Mvar   OUT   Positive-Sequence, Reactive Power
##    ##                   'c:firel', # deg    Rotor angle with reference to reference machine angle 
##               )

### channels for loads
##for load in loads:                        # creating channels for:
##    elmres.AddVars(load, 'n:u1:bus1',     # voltage ('m:u')
##                         'm:I1:bus1',     # current ('s:P1')
##                         'm:Psum:bus1',   # active power ('s:P1')
##                         'm:Qsum:bus1')   # reactive power ('s:Q1')

ldf.iopt_net = 0
ldf.Execute()

ini.iopt_dtgrd = 0.001  # step size
ini.dtout = 1.0
ini.Execute()


sim.tstop = 1.0
sim.Execute()

comres = app.GetFromStudyCase('ComRes'); 
comres.iopt_csel = 0
comres.iopt_tsel = 0
comres.iopt_locn = 2
comres.ciopt_head = 1
comres.pResult=elmres
comres.f_name = r'E:\Documents\public\workspace\pypstools\dev\sing_results.txt'  # change 'C:\Users\jmmauricio\hola.txt' with your path
comres.iopt_exp=4
comres.Execute()

app.ResetCalculation()
