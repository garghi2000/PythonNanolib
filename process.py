admitted_types = ["CLAMPoints-dat",
                "bias spectroscopy",
                "History Data",
                "Sweep",
                "Oscilloscope",
                "Z spectroscopy",
                "Longterm",
                "Spectrum",
                "STM",
                "SFEM"
                ]

def _normalization(data):
    return data
def _scaling(data):
    return data
def _multiplying(data):
    return data
def _differentiation(data):
    return data
def _sum(data):
    return data

def _process_data(data, processType):
    process_data = data
    return process_data

def process(NanonisFile, processType = 'Normalization', chnsToProc = 'all', ref = None):
    processAllowed = ['Normalization','Scaling','Differentiation','Multiplycation','Sum']
    df = NanonisFile.data
    
    
    
    #check the input processType
    if not(processType in processAllowed):
        raise Exception('The processType must be one of the following: '
                        'Normalization, Scaling, Moltiplying, Sum.')
    
    if chnsToProc == 'all' :
        chnsToProc = df.columns
    elif set(chnsToProc).issubset(df.columns):
        chnsToProc = chnsToProc
    elif set(chnsToProc).issubset(range(len(df.columns))):
        chnsToProc = df.columns[chnsToProc]
    else :
        raise Exception('The parameter yChns must be a list of column names,'
                        'a list of integers, or a string == all')
        
    #retrive data to process to numpy array
    ################################ work from here ##########################
    for chn in chnsToProc:    
        dataToProcess = df[chn].to_numpy()
        newData = _process_data(dataToProcess, processType)
        newDataName = chn + ' ' + processType
        df.insert(len(df)+1, newData, newDataName)
    
    if ref in df.columns or  ref in range(len(df.columns)):
        ref = df[ref]
    else :
        raise Exception('The parameter ref must be None or string present in '
                    'the list of the recorded channels names')
    
    pass