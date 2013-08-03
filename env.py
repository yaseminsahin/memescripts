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



