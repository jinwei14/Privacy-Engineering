def load(filename="json/f.smart.json"):
    with open(filename) as json_file:
        json_circuits = json.load(json_file)

    for json_circuit in json_circuits['circuits']:
        circuit = Circuit(json_circuit)
        circuit.printall()


class Circuit:
    def __init__(self, circuitDict):
        self.name = None
        self.alice = None
        self.bob = None
        self.gates = None
        self.out = None
        # processes json.
        self.processCircuit(circuitDict)

    def processCircuit(self, circuit):
        """
        Loads the json and adds the relevant contents into the
        object.
        """
        for key in circuit.keys():
            setattr(self, key, circuit[key])
        self.raw = circuit

    def compute(self, inputs):
        """
        Computes the gate operations and then returns the output.
        """
        # initiate gates
        gates = Gates()
        # creates stores.
        limit = max([max(self.out), max([i['id'] for i in self.gates])])
        # create array to reference values at.
        store = [0 for i in range(limit + 1)]

        # store inputs
        input_ids = self.alice + self.bob if self.bob else self.alice
        for i in input_ids:
            store[i] = inputs.pop(0)

        # iterate through the gate operations
        for gate in self.gates:
            # load logic gate
            logic = getattr(gates, gate['type'])
            # load inputs
            parameters = tuple([store[i] for i in gate['in']])
            # get output
            result = logic(parameters)
            # store result
            store[gate['id']] = result

        return [store[i] for i in self.out]

    def printall(self):
        """
        Helper function to handle printing as is specified in the
        coursework notes.
        """
        print(self.name)
        for alice in self.perms(len(self.alice)):
            if self.bob:
                for bob in self.perms(len(self.bob)):
                    inputs = alice + bob
                    pr = "Alice" + str(self.alice) + " = "
                    for i in alice:
                        pr += str(i) + " "
                    pr += "  Bob" + str(self.bob) + " = "
                    for i in bob:
                        pr += str(i) + " "
                    pr += "  Outputs" + str(self.out) + " = "
                    for i in self.compute(inputs):
                        pr += str(i) + " "
                    print(pr)
            else:
                inputs = alice
                pr = "Alice" + str(self.alice) + " = "
                for i in alice:
                    pr += str(i) + " "
                pr += "  Outputs" + str(self.out) + " = "
                for i in self.compute(inputs):
                    pr += str(i) + " "
                print(pr)
        print()

    @staticmethod
    def perms(n):
        """
        Helper function to generate permutations for binary integers
        based on the length n.
        """
        if not n:
            return
        entries = []
        for i in range(2 ** n):
            s = bin(i)[2:]
            s = "0" * (n - len(s)) + s
            ent = [int(i) for i in s]
            entries.append(ent)
        return entries


# load()


def loadall():
    import os
    folderpath = "json"
    for file in os.listdir(folderpath):
        filename = os.path.join(folderpath, file)
        with open(filename) as json_file:
            json_circuits = json.load(json_file)

        for json_circuit in json_circuits['circuits']:
            circuit = Circuit(json_circuit)
            circuit.printall()


loadall()