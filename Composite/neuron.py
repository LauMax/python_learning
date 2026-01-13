class Neuron:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

    def add_input(self, neuron):
        self.inputs.append(neuron)

    def add_output(self, neuron):
        self.outputs.append(neuron)

    def __repr__(self):
        return f"Neuron({self.name})"
    
    def __str__(self):
        input_names = [neuron.name for neuron in self.inputs]
        output_names = [neuron.name for neuron in self.outputs]
        return (f"Neuron: {self.name}\n"
                f"  Inputs: {', '.join(input_names) if input_names else 'None'}\n"
                f"  Outputs: {', '.join(output_names) if output_names else 'None'}")