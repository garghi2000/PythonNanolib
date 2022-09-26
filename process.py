def procces_data(data, exp_type):
    if exp_type == 'CLAMPoints-dat':
        processed_data = data
    elif exp_type == 'bias spectroscopy':
        processed_data = data
    elif exp_type == 'History Data':
        processed_data = data
    elif exp_type == 'Sweep':
        processed_data = data   
    elif exp_type == 'Oscilloscope':
        processed_data = data
    elif exp_type == 'Z spectroscopy':
        processed_data = data
    elif exp_type == 'Longterm':
        processed_data = data
    elif exp_type == 'Spectrum':
        processed_data = data
    elif exp_type == 'STM':
        processed_data = data
    elif exp_type == 'SFEM':
        processed_data = data
    else:
        raise Exception('The experiment type could not be found in the header.')
    return processed_data
#if clam
Xlabel = "Energy (eV)"
Ylabel = "Counter 2 (cps)"
Ylabelnorm = "Counts/Current (cps/A)"
Xdata = myfile.data[Xlabel]
Ydata = myfile.data[Ylabel]
Ydatanorm = Ydata/np.abs(myfile.data['Tip Current (A)'])

fig, ax = plt.subplots()
ax.plot(Xdata, Ydata, '.-b', label='row')
ax.set_xlabel(Xlabel)
ax.set_ylabel(Ylabel)

ax2 = ax.twinx()
ax2.plot(Xdata, Ydatanorm, '.-r', label='norm by current')
ax2.set_ylabel(Ylabelnorm)

plt.title(myfile.metadata["File name"])

ax.legend(loc=0)
ax2.legend(loc=1)

plt.show()

   #if bbx
Xlabel = "BB Back Bias (V)"
Ylabel = "BBX (Hz)"
Ylabelnorm = "Counts/Current (cps/A)"
Xdata = myfile.data[Xlabel]
Ydata = myfile.data[Ylabel]
Ydatanorm = Ydata/np.abs(myfile.data['Tip Current (A)'])

fig, ax = plt.subplots()
ax.plot(Xdata, Ydatanorm, '.-b', label='Si(111) 7x7')
ax.set_xlabel(Xlabel)
ax.set_ylabel(Ylabelnorm)
    
plt.title(["Si(111) 7x7 , Ep = 133 eV"])

ax.legend(loc=0)
plt.show()

