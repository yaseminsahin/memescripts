import os

global _env

_env = {}

_env['MEME_PATH'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir) )
_env['DATA_PATH'] = os.path.abspath(
    os.path.join(_env['MEME_PATH'] , 'mydata') )
_env['MEME_BIN_PATH'] = os.path.abspath(
    os.path.join(_env['MEME_PATH'] , 'bin') )
_env['MEME_EXE_PATH'] = os.path.abspath(
    os.path.join(_env['MEME_BIN_PATH'] , 'meme') )
    
_env['MERCI_PATH'] = os.path.abspath(os.path.join(os.getcwd(), os.pardir) )
_env['MERCI_DATA_PATH'] = os.path.abspath(
    os.path.join(_env['MERCI_PATH'] , 'mydata') )
    
_env['MERCI_EXE_PATH'] = os.path.abspath(
    os.path.join(_env['MERCI_PATH'] , 'MERCI.pl') )
    
_env['MERCI_CLASSIFICATION_PATH'] = os.path.abspath(
    os.path.join(_env['MERCI_PATH'] , 'classification') )
    
_env['MERCI_OUTPUT_PATH'] = os.path.abspath(
    os.path.join(_env['MERCI_DATA_PATH'] , 'merciresult') )




