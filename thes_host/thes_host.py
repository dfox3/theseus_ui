# install with "sudo apt install python-serial"
# pip install pyserial
# pip install esptools
import serial
import serial.tools.list_ports
import datetime
import time
import glob, os
import sys
import parse
import argparse


#--------------------------------------------------------------
# GLOBALS
THES_MSG_TERMINATOR = '\n'
dir = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILENAME = os.path.join(dir, "thes_config.txt")
WINPORT = "ELTIMA"

#--------------------------------------------------------------
# ARGPARSE
parser = argparse.ArgumentParser(description='Theseus Host')
parser.add_argument('-i',  
    action='store', 
    dest='i',
    type=str,
    default="dev",
    help="path/to/input.txt - commands script text file. If not entered, user enters dev mode.")

options = parser.parse_args()

#--------------------------------------------------------------
# MAIN
def main():
    serial_port_name = ""
    if sys.platform == "linux" or sys.platform == "linux2":
        # find first ttyUSBx device
        tty_dir = '/dev/serial/by-id/'
        tty_dev = ''
        for file in os.listdir(tty_dir):
            if 'CP2102N_USB_to_UART' in file:
                tty_dev = file
        if tty_dev == '':
            print('couldn\'t find a ttyUSB device - is the Theseus USB plugged in?')
            sys.exit(0)

        serial_port_name = tty_dir + tty_dev
    elif sys.platform == "win32":
        #import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        print("ports:")
        print(ports)
        for p in ports:
            print(p)
            if WINPORT in p[1]:
                serial_port_name = p[0]
    else:
        print('OS not supported')
    # open all files and ports
    with serial.Serial(serial_port_name, 115200, timeout=0.3) as serial_console:
        # clear input data
        char = 'a'
        while len(char) != 0:
            char = serial_console.read().decode('ascii')
        # open config file
        with open(CONFIG_FILENAME, 'r') as config_file:
            # run config file script at beginning of session
            processScript(serial_console, None, config_file)
            if options.i == "dev": #dev mode
                while 1:
                    # prompt user for script file to run or command to send
                    user_input = input('theseus > ')        
                    tokens = user_input.split(' ')
                    cmd = tokens[0]
                    if cmd == 'run':
                        # user wants to run a script
                        if len(tokens) != 2:
                            log(None, 'run command expected 1 arg\n')
                            continue
                        script_filename = 'assays/' + tokens[1]
                        if not os.path.exists(script_filename):
                            log(None, 'script file doesn\'t exist\n')
                            continue
                        with open(script_filename, 'r') as script_file:
                            log_filename = 'thes_log_{}_{}.txt'.format(tokens[1], datetime.datetime.now().strftime('%Y_%m_%d_%H:%M:%S'))
                            with open('logs/' + log_filename, 'w+') as log_file:
                                log(log_file, 'running script {}{}'.format(script_file, THES_MSG_TERMINATOR))
                                processScript(serial_console, log_file, script_file)
                    elif cmd == 'print' or cmd == '':
                        pass
                    elif cmd == 'tec_tune':
                        if len(tokens) != 3:
                            log(None, 'run command expected 2 args (setpoint, runtime)\n')
                            continue
                        serial_console.write(('1:tec_run:' + tokens[1] + ',' + tokens[2] + THES_MSG_TERMINATOR).encode('ascii'))
                        serial_console.flush()

                        time = 0
                        resp = ''
                        while (resp != '1:-2:end,0' + THES_MSG_TERMINATOR):
                            resp = ''
                            while not resp.endswith(THES_MSG_TERMINATOR):
                                resp += serial_console.read().decode('ascii')
                            log(None, '<--- {}'.format(resp))
                            temp_parse = parse.search('temp = [{}] err', resp)
                            dt_parse = parse.search('dt(ms) = [{}] output', resp)
                            if temp_parse != None:
                                time += float(dt_parse.fixed[0])
                                temp = float(temp_parse.fixed[0])
                                plt.scatter(time, temp)
                                plt.pause(0.01)
                    else:
                        # user entered a command to send to theseus
                        serial_console.write((user_input + THES_MSG_TERMINATOR).encode('ascii'))
                        serial_console.flush()
                    # print out console output
                    resp = ' '
                    while resp != '':
                        byte = serial_console.read().decode('ascii')
                        log(None, byte)
                        resp = byte
            else:
                print("automatic command excepted")
                with open(str(options.i), 'r') as input_script:
                    processScript(serial_console, None, input_script)


#--------------------------------------------------------------
# DEFS
def log(log_file, msg):
	if log_file != None:
		log_file.write(msg)
	sys.stdout.write(msg)

def reportErr(log_file, line, file, msg):
	log(log_file, 'error on line {} of {}: {}{}'.format(line, file.name, msg, THES_MSG_TERMINATOR))

def processScript(serial_console, log_file, script_file):
	content = script_file.readlines()
	for i in range(len(content)):
		line_num = i+1
		line = content[i].strip()
		tokens = line.split(':')
		cmd = tokens[0]
		cmd_msg = str(line_num) + ':' + cmd
		# delay command
		if cmd == 'delay':
			if len(tokens) == 2:
				time.sleep(float(tokens[1]))
				log(log_file, line + THES_MSG_TERMINATOR)
			else:
				reportErr(log_file, line_num, script_file, 'delay command expected 1 arg')
		# print command
		elif cmd == 'print':
			if len(tokens) >= 2:
				log(log_file, line + THES_MSG_TERMINATOR)
			else:
				reportErr(log_file, line_num, script_file, 'print command expected 1 arg')
		# command is a comment or empty line
		elif cmd == '' or cmd.startswith('#'):
			continue
		# any other command
		else:
			thes_cmd = '{}:{}'.format(line_num, line)
			log(log_file, '---> {}{}'.format(thes_cmd, THES_MSG_TERMINATOR))
			serial_console.write((thes_cmd + THES_MSG_TERMINATOR).encode('ascii'))
			serial_console.flush()
			resp = ''
			while (resp != str(line_num) + ':-2:end,0' + THES_MSG_TERMINATOR) and (resp != '-2:ready' + THES_MSG_TERMINATOR):
				resp = ''
				while not resp.endswith(THES_MSG_TERMINATOR):
					resp += serial_console.read().decode('ascii')
				log(log_file, '<--- {}'.format(resp))

	log(log_file, '\n' + script_file.name + ' complete\n\n')

if __name__ == '__main__':
    main()