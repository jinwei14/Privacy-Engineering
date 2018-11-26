
"""
Submission by:
Thien Nguyen (tn518 / 01565994)
Jinwei Zhang (jz2618 / 01540854)
"""

# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

import json	# load
import sys	# argv

import ot	# alice, bob
import util	# ClientSocket, log, ServerSocket
import fern
import os
import json
import circuit as c # yaos garbled circuit
import evaluator as bh # bob's seperately computed evaluation


def generateTitle(string):
    bar = "======="
    title = "\n" + bar + " " + string + " " + bar
    print(title)

# Alice is the circuit generator (client) __________________________________

def alice(filename):
  def obliviousTransfer(input1, input2):
    alice = ot.Alice(input1, input2)
    # wait until bob is online
    # print("waiting for bob to send OT_REQ")
    ready = socket.receive()
    if ready:
      # send c
      ot_c = alice.send_c()
      socket.send(ot_c)
      # wait for bob to send H0 so that we can receive it.
      h0 = socket.receive()
      # compute c_1, E, length
      c_1, E, length = alice.sendMessage(h0)
      # send c_1, E, length to Bob.
      payload = (c_1, E, length)
      socket.send(payload)

  def basicTransfer(input1, input2):
    payload = socket.receive()
    if payload == 0:
      socket.send(input1)
    else:
      socket.send(input2)

  socket = util.ClientSocket()

  with open(filename) as json_file:
    json_circuits = json.load(json_file)

  for json_circuit in json_circuits['circuits']:
    # print title
    generateTitle(json_circuit['name'])

    # generate permutation of alice's inputs.
    aliceInputs = util.perms(len(json_circuit['alice']))
    for aliceInput in aliceInputs:
      # check whether this circuit involves bob.
      if not 'bob' in json_circuit:
        # set up circuit.
        circuit = c.Circuit(json_circuit)
        # bob is not involved in this circuit so theres no point computing
        # our encrypted transfer.
        circuit.printRow(aliceInput, None)
      else:
        # alice will assume that bob will compute these values:
        for bobInput in util.perms(len(json_circuit['bob'])):
          # set up circuit.
          circuit = c.Circuit(json_circuit)
          # calculate the reference output
          test = circuit.compute(aliceInput + bobInput)
          # build relevant files needed to send to bob
          toBob = circuit.sendToBob(aliceInput)
          # send to bob.
          socket.send(toBob)
          # wait for an OT request
          for i in range(len(toBob['bobIndex'])):
            bobIndex = toBob['bobIndex'][i]
            inp1, inp2 = circuit.setupBobOT(bobIndex)
            obliviousTransfer(inp1, inp2)

          # Bob will send a payload saying that he's ready.
          socket.receive()
          socket.send("OK")
          # at this stage the next received msg is the output.
          output = socket.receive()
          # create checksum to determine whether
          # our output is the same as the input.
          check = True if test == output else False
          if check:
            # the computation is equivalent;
            # Alice will compute the truth table.
            circuit.printRow(aliceInput, bobInput)
            socket.send(True)
          else:
            print("ERROR: The circuit does not compute.", test, output)
            socket.send(False)
          # blank message saying that he's ready to go again.
          msg = socket.receive()
          if msg == "AGAIN":
            # bob has not finished iterating through his binary
            # values.
            pass
          elif msg == "DONE":
            print("bob has finished iterating through his parts.")
  # socket.send("DONE")
  pass

# Bob is the circuit evaluator (server) ____________________________________

def bob():
  def obliviousTransferB(inputIndex):
    # set up ot class for Bob
    bob = ot.Bob(inputIndex)
    # set up ready.
    socket.send("OT_REQUEST")
    # wait to receive c value
    ot_c = socket.receive()
    # generate H0
    H0 = bob.send_h0(ot_c)
    # send H0 to alice
    socket.send(H0)
    # wait for Alice to send h0, E, length as a payload
    (c_1, E, length) = socket.receive()
    # compute response
    message = bob.getMessage(c_1, E, length).decode()
    return message

  def basicTransfer(inputIndex):
    socket.send(inputIndex)
    return socket.receive()

  socket = util.ServerSocket()
  util.log(f'Bob: Listening ...')
  print("Listening for Alice..")
  print("waiting to receive primary payload from alice..")
  payload = socket.receive()
  while True:
    if isinstance(payload,dict):
      print("Received primary payload from alice.")
    else:
      if payload == "DONE":
        print("I've finished computing the things I needed to do")
        print("\tfor this garbled circuit.")
        print("Please run me again if you wish to evaluate a")
        print("\tdifferent circuit.")
        break
      else:
        print("Received unexpected value:", payload)

    for bobInput in util.perms(len(payload['bobIndex'])):
      # set up input variables needed to compute the garbled circ.
      bobPInput = []
      for i in range(len(bobInput)):
        bobValue = bobInput[i]
        value = obliviousTransferB(bobValue)
        # value = basicTransfer(bobValue)
        bobPInput.append(int(value))
      # tell Alice i'm ready to evaluate the output.
      socket.send("READY")
      msg = socket.receive()
      # evaluate the output.
      output = bh.evaluate(payload, pinputs=bobPInput)
      # send the output to alice for verification
      socket.send(output)
      # receive response checking whether it was right or not.
      check = socket.receive()
      if check is False:
        print("Incorrect.")
      else:
        print("Correct.")
      # either way, tell alice you're ready to receive again.
      socket.send("AGAIN")
      payload = socket.receive()

# local test of circuit generation and evaluation, no transfers_____________

def local_test(filename):
  with open(filename) as json_file:
    json_circuits = json.load(json_file)

  for json_circuit in json_circuits['circuits']:
    circuit = c.Circuit(json_circuit)
    # generate title
    generateTitle(json_circuit['name'])

    for aliceInput in circuit.perms(len(json_circuit['alice'])):
      # check whether this circuit involves bob.
      if circuit.bob:
        # build relevant files needed to send to bob
        toBob = circuit.sendToBob(aliceInput)
        # iterate through bob's potential inputs.
        for bobInput in circuit.perms(len(json_circuit['bob'])):
          # get the reference output to verify the results.
          test = circuit.compute(aliceInput + bobInput)
          # do oblivious transfer on this.
          bobPInput = []
          for i in range(len(bobInput)):
            bobValue = bobInput[i]
            bobIndex = toBob['bobIndex'][i]
            otB = ot.Bob(bobValue)
            inp1, inp2 = circuit.setupBobOT(bobIndex)
            otA = ot.Alice(inp1, inp2)
            # garbled circuit stuff.
            ot_c = otA.send_c()
            h0 = otB.send_h0(ot_c)
            c_1, E, length = otA.sendMessage(h0)
            payload = int(otB.getMessage(c_1, E, length))
            bobPInput.append(payload)
          # bob evaluates the output.
          output = bh.evaluate(toBob,pinputs=bobPInput)
          # create checksum to determine whether
          # our output is the same as the input.
          check = True if test == output else False
          if check:
            # the computation is equivalent;
            # Alice will compute the truth table.
            circuit.printRow(aliceInput,bobInput)
          else:
            print("ERROR: The garbled circuit does not compute.")
      else:
        # bob is not involved in this circuit so theres no point 
        # computing our encrypted transfer.
        circuit.printRow(aliceInput, None)

# main _____________________________________________________________________

def main():
  behaviour = sys.argv[1]
  if   behaviour == 'alice': alice(filename=sys.argv[2])
  elif behaviour == 'bob':   bob()
  elif behaviour == 'local': local_test(filename=sys.argv[2])

if __name__ == '__main__':
  main()

# __________________________________________________________________________


