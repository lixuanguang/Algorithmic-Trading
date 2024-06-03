'''
v1.0 - Generic File Reader
'''

# Import libraries
import pandas as pd
import glob
import os

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')


def singledirimport(dir, **kwargs):

    '''
    Function that reads from single directory all the files fulfiling a condition, then returns a dataframe

    :param dir: (str) specifies the directory to read files from
    :param dtype: [optional, default = str] (type) reads all columns as string by default unless specified
    :param skipper: [optional, default = [0,0]] (array[x(int), y(int)]) specifies how many [x=rows, y=footer] to skip
    :param nrows: [optional, default = None] (int) specifies the number of rows to read
    :param filename: [optional, default = ''] (str) specifies the common name of all files to read
    :param horizontal: [optional, default = False] (array[str, str, ...]) specifies the list of columns to horizontal merge the datafrmes on
    :param dropcol: [optional, default = False] (array[str, str, ...]) specifies the list of columns to drop when reading the files
    :param ignorelist: [optional, default = False] (array[str, str, ...]) specifies the list of files to ignore when reading
    :param ignore_index: [optional, default = False] (boolean) if True, do not use the index values along the concatenation axis
    :param sheet_name: [optional, default = 0] (str, int, [str/int, str/int, ...]) specifies the name or index of an excel sheet, or list of excel sheet to read from
    :param keepfilename: [optional, default = False] (boolean) specifies whether to keep the name of the file in a separate column after reading it
    :param delimiter: [optional, default = None] (str) specifies whether to read the file with specific delimiter
    :returns: a merged pandas dataframe containing all the data from the specified files in a single directory
    
    '''


    ################ Optional Argument Specifications ############################

    # Datatype specification - reads all columns as string by default unless specified
    if 'dtype' in kwargs:
        dtype = kwargs['dtype']
    else:
        dtype = str

    # Skipping specification - on how many [rows, footer] to skip. Does not skip any rows by default
    if 'skipper' in kwargs:
        skipper = kwargs['skipper']
    else:
        skipper = [0,0]

    # Number of rows to read specification - specifies the number of rows to read
    if 'nrows' in kwargs:
        nrowsval = kwargs['nrows']
    else:
        nrowsval = None

    # Filename specification - get all files with the common name specified
    if 'filename' in kwargs:
        filename = kwargs['filename']
    else:
        filename = ''
    
    # Horizontal merge specification - whether to merge horizontal on the column names specified in the list
    if 'horizontal' in kwargs:
        horiz = kwargs['horizontal']
    else:
        horiz = False

    # Column drop specification - whether to drop any columns when reading
    if 'dropcol' in kwargs:
        dropcol = kwargs['dropcol']
    else:
        dropcol = False
    
    # Ignore list specification - whether to drop any files with the names in the list specified
    if 'ignorelist' in kwargs:
        ignorelist = kwargs['ignorelist']
    else:
        ignorelist = False

    # Ignore Index specification - If True, do not use the index values along the concatenation axis. 
    # The resulting axis will be labeled 0, …, n - 1. 
    # This is useful if you are concatenating objects where the concatenation axis does not have meaningful indexing information. 
    if 'ignore_index' in kwargs:
        ignore_index = kwargs['ignore_index']
    else:
        ignore_index = False

    # Sheet name specification - specifies the name or index of an excel sheet, or list of excel sheet to read from
    if 'sheet_name' in kwargs:
        sheet_name = kwargs['sheet_name']
    else:
        sheet_name = 0

    # Keep file name specification - whether to keep the name of the source file where the information was retrieved from
    if 'keepfilename' in kwargs:
        keepfilename = kwargs['keepfilename']
    else:
        keepfilename = False

    # Delimiter specification - whether to read the file with specific delimiter
    if 'delimiter' in kwargs:
        delimiter = kwargs['delimiter']
    else:
        delimiter = None

    ################ End of Optional Argument Specifications ############################


    ##################### List of Files in Directory Fulfilling Condition ############################

    # Get list of file names
    filedir = dir + '\\' + filename + '*'
    listfiles = glob.glob(filedir)

    # Filter for files in ignore list
    if ignorelist != False:
        for filenameignore in ignorelist:
            listfiles = list(filter(lambda x: filenameignore not in x, listfiles))
    
    listfiles = list(filter(lambda x: '~$' not in x, listfiles)) # Ignore temp files created

    # Segment files into file types of csv, txt, xlsx
    csvtxtfiles = list(filter(lambda x: x.endswith(('.csv', 'txt')), listfiles))
    xlsxfiles = list(filter(lambda x: x.endswith(('.xls', 'xlsx')), listfiles))

    ##################### End of List of Files in Directory Fulfilling Condition ############################

    ##################### File Parser that Returns a Pandas DataFrame ############################

    # Dataframe to store results
    df = pd.DataFrame()

    # Read csv and txt files
    if csvtxtfiles != []:
        for file in csvtxtfiles:
            rawfilename = file.split('\\')[-1]

            if delimiter != None:
                filedf = pd.read_csv(file, dtype=dtype, skiprows=skipper[0], skipfooter=skipper[1], nrows=nrowsval)
            else:
                filedf = pd.read_csv(file, delimiter=delimiter[0], dtype=dtype, skiprows=skipper[0], skipfooter=skipper[1], nrows=nrowsval)
            
            if keepfilename != False:
                filedf['Source_Filename'] = rawfilename

            if dropcol != False:
                filedf = filedf.drop(dropcol, axis=1)
            
            if horiz == False:
                df = pd.concat([df, filedf], ignore_index=ignore_index)
            else:
                if not df.empty:
                    df = df.merge(filedf, how='outer', on=horiz)
                else:
                    df = filedf
    
    # Read excel files
    if xlsxfiles != []:
        for file in xlsxfiles:
            rawfilename = file.split('\\')[-1]

            filedf = pd.read_excel(file, sheet_name=sheet_name, dtype=dtype, skiprows=skipper[0], skipfooter=skipper[1], nrows=nrowsval)

            if keepfilename != False:
                filedf['Source_Filename'] = rawfilename

            if dropcol != False:
                filedf = filedf.drop(dropcol, axis=1)
            
            if horiz == False:
                df = pd.concat([df, filedf], ignore_index=ignore_index)
            else:
                if not df.empty:
                    df = df.merge(filedf, how='outer', on=horiz)
                else:
                    df = filedf
            
    ##################### End of File Parser that Returns a Pandas DataFrame ############################

    return df


def multidirimport(dir, **kwargs):

    '''
    Function that reads from directory and all subdirectory all the files fulfiling a condition, then returns a dataframe

    :param dir: (str) specifies the directory to read files from
    :param dtype: [optional, default = str] (type) reads all columns as string by default unless specified
    :param skipper: [optional, default = [0,0]] (array[x(int), y(int)]) specifies how many [x=rows, y=footer] to skip
    :param nrows: [optional, default = None] (int) specifies the number of rows to read
    :param filename: [optional, default = ''] (str) specifies the common name of all files to read
    :param horizontal: [optional, default = False] (array[str, str, ...]) specifies the list of columns to horizontal merge the datafrmes on
    :param dropcol: [optional, default = False] (array[str, str, ...]) specifies the list of columns to drop when reading the files
    :param ignorelist: [optional, default = False] (array[str, str, ...]) specifies the list of files to ignore when reading
    :param ignore_index: [optional, default = False] (boolean) if True, do not use the index values along the concatenation axis
    :param sheet_name: [optional, default = 0] (str, int, [str/int, str/int, ...]) specifies the name or index of an excel sheet, or list of excel sheet to read from
    :param keepfilename: [optional, default = False] (boolean) specifies whether to keep the name of the file in a separate column after reading it
    :param delimiter: [optional, default = None] (str) specifies whether to read the file with specific delimiter
    :returns: a merged pandas dataframe containing all the data from the specified files in a single directory
    
    '''

    ################ Optional Argument Specifications ############################

    # Ignore Index specification - If True, do not use the index values along the concatenation axis. 
    # The resulting axis will be labeled 0, …, n - 1. 
    # This is useful if you are concatenating objects where the concatenation axis does not have meaningful indexing information. 
    if 'ignore_index' in kwargs:
        ignore_index = kwargs['ignore_index']
    else:
        ignore_index = False

    ################ End of Optional Argument Specifications ############################

    # Dataframe to store results
    df = pd.DataFrame()

    # Iterate through subdirectories to read all files
    for subdir, dirs, files in os.walk(dir):

        filedf = singledirimport(subdir, **kwargs)
        df = pd.concat([df, filedf], ignore_index=ignore_index)
    
    df = df.reset_index(drop=True)

    return df