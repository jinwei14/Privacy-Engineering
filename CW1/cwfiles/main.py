
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import json	# load
import sys	# argv

import ot	# alice, bob
import util	# ClientSocket, log, ServerSocket
import yao	# Circuit

# Alice is the circuit generator (client) __________________________________

def alice(filename):
    socket = util.ClientSocket()

    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    # << Your code >>
    for json_circuit in json_circuits['circuits']:
        print(json_circuit)




# Bob is the circuit evaluator (server) ____________________________________

def bob():
    socket = util.ServerSocket()
    util.log(f'Bob: Listening ...')

    # << removed >>
    while True:
        print("?")
        break




# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    # << removed >>
    for json_circuit in json_circuits['circuits']:
        print(json_circuit)


# main _____________________________________________________________________
# json/f.add.json json file
def main():
    behaviour = sys.argv[1]
    if  behaviour == 'alice':
        alice(filename=sys.argv[2])

    elif behaviour == 'bob':
        bob()

    elif behaviour == 'local':
        local_test(filename=sys.argv[2])

if __name__ == '__main__':
  main()

# __________________________________________________________________________


