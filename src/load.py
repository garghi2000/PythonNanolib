import os, time, warnings
import numpy as np

class Nanonisfile:
    """ This is the file Class to structure Nanonis files.

    CONSTANTS
    ---------------------------------------------------------------------------
    nanonis_flags : {'file extension': 'flag'} -> dictionary containing the 
    flags separating header from data for different file types recorded by 
    nanonis

    INPUT
    ---------------------------------------------------------------------------
    fpfname : (str) ->  full path file name

    ATTRIBUTES
    ---------------------------------------------------------------------------
    _ffname : (str) ->  full path file name

    _dataflag : (int) -> index of the bit separeting header from data

    metadata : {'str': 'str/int/float'} -> dictionary of metadata 
        such as file size, file name, file directory, file type.

    header : {'str': 'str/int/float'} -> dictionary of data information
        as written by nanonis. It depends on the nanonis module used to create
        the file.

    data {'str': 'numpy 1D-array'} -> dictionary of data recorded by nanonis
        easily covertible in pandas data frame.

    """

    global nanonis_flags
    nanonis_flags = {'.sxm': 'SCANIT_END', '.dat': '[DATA]'}

    def __init__(self, fpfname):
        self._ffname = fpfname
        self.metadata = self._get_metadata()
        self._dataflag = None
        self.header = self._get_header()
        self.data = self._get_data()

    def _get_metadata(self):
        directory_fname, base_fname = os.path.split(self._ffname)
        size_f = os.path.getsize(self._ffname)
        _, type_f = os.path.splitext(self._ffname)
        lastmdate_f = time.ctime(os.path.getmtime(self._ffname))
        try:
            # for windows
            cdate_f = time.ctime(os.path.getctime(self._ffname))
        except:
            try:
                # for IOS
                stat = os.stat(self._ffname)
                cdate_f = time.ctime(stat.st_birthtime)
            except AttributeError:
                # We're probably on Linux. No easy way to get creation date,
                # so we'll settle for when its content was last modified.
                cdate_f = lastmdate_f
        metadata = {'File name': base_fname,
                    'File directory': directory_fname,
                    'File size': size_f,
                    'File extension': type_f,
                    'Date creation': cdate_f,
                    'Date last modification': lastmdate_f}
        return metadata

    def _get_header(self):
        fname_ext = self.metadata['File extension']

        if fname_ext not in ['.sxm', '.dat']:
            raise UnhandledFileError(
                f"{fname_ext} is not a supported filetype or does not exist")

        tag = nanonis_flags[fname_ext]

        with open(self._ffname, 'rb') as f:

            # Set to a default value to know if end_tag wasn't found
            self._dataflag = -1

            for line in f:
                # Convert from bytes to str
                try:
                    entry = line.strip().decode()
                except UnicodeDecodeError:
                    warnings.warn(
                        '{} has non-uft-8 characters, replacing them.'.format(f.name))
                    entry = line.strip().decode('utf-8', errors='replace')
                if tag in entry:
                    self._dataflag = f.tell()
                    break
        with open(self._ffname, 'rb') as f:
            header = f.read(self._dataflag).decode('utf-8', errors='replace')
        if self._dataflag == -1:
            raise FileHeaderNotFoundError(
                    'Could not find the {} end tag in {}'.format(tag, self._ffname)
                    )

        if fname_ext == '.dat':
            header = _parse_dat_header(header)
           
        elif fname_ext == '.sxm':
            header = _parse_sxm_header(header)            

        return header

    def _get_data(self):
        fname_ext = self.metadata['File extension']
        
        if fname_ext not in ['.sxm','.dat']:
            raise UnhandledFileError(f'{fname_ext} is not a supported filetype or does not exist')

        data = _load_data(self._ffname, self.metadata['File extension'], self._dataflag, self.header)
        return data

class UnhandledFileError(Exception):

    """
    To be raised when unknown file extension is passed.
    """
    pass


class FileHeaderNotFoundError(Exception):
    """
    To be raised when no header information could be determined.
    """
    pass

def _parse_scan_header_table(table_list):
    """
    Parse scan file header entries whose values are tab-separated
    tables.
    """
    table_processed = []
    for row in table_list:
        # strip leading \t, split by \t
        table_processed.append(row.strip('\t').split('\t'))

    # column names are first row
    keys = table_processed[0]
    values = table_processed[1:]

    zip_vals = zip(*values)

    return dict(zip(keys, zip_vals))

def _parse_sxm_header(header_raw):
    """
    Parse raw header string.

    Empirically done based on Nanonis header structure. See Scan
    docstring or Nanonis help documentation for more details.

    Inputs
    ----------
    header_raw : str
        Raw header string to be formatted.

    Returns
    -------
    dict : {'Channel name';'[data array]'}
        Channel name keyed dictionary of each channel array.
    """
    header_entries = header_raw.split('\n')
    header_entries = header_entries[:-3]

    header_dict = dict()
    entries_to_be_split = ['scan_offset',
                           'scan_pixels',
                           'scan_range',
                           'scan_time']

    entries_to_be_floated = ['scan_offset',
                             'scan_range',
                             'scan_time',
                             'bias',
                             'acq_time']

    entries_to_be_inted = ['scan_pixels']

    entries_to_be_dict = [':DATA_INFO:',
                          ':Z-CONTROLLER:',
                          ':Multipass-Config:']

    entries_possibly_multilines = [':COMMENT:']

    for i, entry in enumerate(header_entries):
        if entry in entries_to_be_dict:
            count = 1
            for j in range(i+1, len(header_entries)):
                if header_entries[j].startswith(':'):
                    break
                if header_entries[j][0] == '\t':
                    count += 1
            header_dict[entry.strip(':').lower()] = _parse_scan_header_table(header_entries[i+1:i+count])
            continue
        if entry in entries_possibly_multilines:
            multilines_entry = []
            for j in range(i+1, len(header_entries)):
                if header_entries[j].startswith(':'):
                    break
                multilines_entry.append(header_entries[j])
            header_dict[entry.strip(':').lower()] = '\n'.join(multilines_entry)
            continue
        if entry.startswith(':'):
            header_dict[entry.strip(':').lower()] = header_entries[i+1].strip()

    for key in entries_to_be_split:
        header_dict[key] = header_dict[key].split()

    for key in entries_to_be_floated:
        if isinstance(header_dict[key], list):
            header_dict[key] = np.asarray(header_dict[key], dtype=np.float)
        else:
            header_dict[key] = np.float(header_dict[key])
    for key in entries_to_be_inted:
        header_dict[key] = np.asarray(header_dict[key], dtype=np.int)

    return header_dict

def _parse_dat_header(header_raw):
    """
    Parse point spectroscopy header.

    Each key-value pair is separated by '\t' characters. Values may be
    further delimited by more '\t' characters.

    Inputs
    ----------
    header_raw : str
        Raw header string to be formatted.

    Returns
    -------
    dict :
        Parsed point spectroscopy header.
    """

    header_entries = header_raw.split('\r\n')
    header_entries = header_entries[:-3]
    header_dict = dict()
    for entry in header_entries:
        # homogenize output of .dat files with \t delimit at end of every key
        if entry[-1] == '\t':
            entry = entry[:-1]
        if '\t' not in entry:
            entry += '\t'

        key, val = entry.split('\t')
        header_dict[key] = val

    return header_dict

def _load_data(filename, file_ext, dataflag, header):
    """
    Loads ascii formatted .dat file or bynary formatted .sxm file.
    
    Inputs
    -------
        file --> entire full file path
        file_ext --> file extension needed to differenciate the
                    way data are loaded.
        dataflag --> flag that delimitates header from data.
        header --> header usefull for retrive data structure in sxm files.

    Returns
    -------
    dict
        Keys correspond to each channel recorded, including
        saved/filtered versions of other channels.
    """

    # load .dat files
    if file_ext == '.dat':

        # done differently since data is ascii, not binary
        with open(filename, 'r') as f:
            f.seek(dataflag)
            data_dict = dict()
            column_names = f.readline().strip('\n').split('\t')

        num_lines = _num_header_lines(filename)
        specdata = np.genfromtxt(filename, delimiter='\t',
                                 skip_header=num_lines)

        for i, name in enumerate(column_names):
            data_dict[name] = specdata[:, i]

    # load .sxm files
    elif file_ext == '.sxm':
        channs = list(header['data_info']['Name'])
        nchanns = len(channs)
        nx, ny = header['scan_pixels']

        # assume both directions for now
        ndir = 2
        data_dict = dict()

        # open and seek to start of data
        scandata = np.fromfile(filename, dtype='>f4', offset=dataflag + 4)

        # reshape
        scandata_shaped = scandata.reshape(nchanns, ndir, ny, nx)

        # extract data for each channel
        for i, chann in enumerate(channs):
            chann_dict = dict(forward=scandata_shaped[i, 0, :, :],
                              backward=scandata_shaped[i, 1, :, :])
            data_dict[chann] = chann_dict

    return data_dict

def _num_header_lines(fname):
    """Number of lines the header is composed of."""
    with open(fname, 'r') as f:
        data = f.readlines()
        for i, line in enumerate(data):
            if nanonis_flags['.dat'] in line:
                return i + 2  # add 2 to skip the tag itself and column names
    return 0
