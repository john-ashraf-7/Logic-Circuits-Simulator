def parse_verilog_file(circuit_num):
    # Define dictionaries to store inputs, outputs, wires, and gates
    inputs = {}
    outputs = {}
    wires = {}
    gates = {}

    # Open and read the Verilog file
    try:
        with open(f"InputFiles/circ_{circuit_num}.v", "r") as verilogfile:
            content = verilogfile.readlines()

        # Parse each line to extract inputs, outputs, wires, and gates
        for line in content:
            # Remove comments by ignoring text after //
            line = line.split("//")[0].strip()
            if not line:  # Skip empty lines
                continue

            # Check for inputs
            if line.startswith("input"):
                input_signals = line.split()[1:]  # Capture everything after "input"
                for signal in input_signals:
                    inputs[signal.replace(";", "").strip()] = 0  # Initialize each input with 0

            # Check for outputs
            elif line.startswith("output"):
                output_signals = line.split()[1:]  # Capture everything after "output"
                for signal in output_signals:
                    outputs[signal.replace(";", "").strip()] = 0  # Initialize each output with 0

            # Check for wires
            elif line.startswith("wire"):
                wire_signals = line.split()[1:]  # Capture everything after "wire"
                for signal in wire_signals:
                    wires[signal.replace(";", "").strip()] = 0  # Initialize each wire with 0

            # Check for gates (like `and`, `or`, `not`, etc.)
            elif any(gate in line for gate in ["and", "or", "not", "nand", "nor", "xor", "xnor", "buf"]):
                gate_parts = line.split(None, 2)  # Split into 3 parts: type, name, and connections
                gate_type = gate_parts[0]  # The gate type (e.g., and, or)
                gate_name = gate_parts[1]  # The gate instance name (e.g., g0, g1)

                # Extract connections by removing the parentheses and semicolon
                connections = gate_parts[2].replace("(", "").replace(");", "").split(",")
                connections = [conn.strip() for conn in connections]  # Clean up whitespace around each connection

                gates[gate_name] = {
                    "type": gate_type,
                    "connections": connections
                }

        # Return the results as a dictionary
        return {
            "inputs": inputs,
            "outputs": outputs,
            "wires": wires,
            "gates": gates
        }

    except FileNotFoundError:
        print(f"Error: File 'InputFiles/circ_{circuit_num}.v' not found.")
        return None


def parse_stimuli_file(circuit_num):
    # Dictionary to store each time as a key with changes as a nested dictionary
    stimuli_data = {}

    # Open and read the stimuli file
    try:
        with open(f"InputFiles/circ_{circuit_num}.stim", "r") as stimuli_file:
            content = stimuli_file.readlines()

        for line in content:
            if line.startswith("#"): #skips empty lines.
                # Remove the "#" from the time and split the line
                line_parts = line.strip().split()
                time = int(line_parts[0].replace("#", ""))  # Convert time to integer

                signal, value = line_parts[1].split("=")[0], int(line_parts[1].split("=")[1].replace(";",""))     # Split signal and value

                # Store the signal and value under the corresponding time
                if time not in stimuli_data:
                    stimuli_data[time] = {}
                stimuli_data[time][signal] = int(value)  # Convert value to integer

        return stimuli_data

    except FileNotFoundError:
        print(f"Error: Stimuli file 'InputFiles/circ_{circuit_num}.stim' not found.")
        return None


def simulator(verilog_parsed_data, stimuli_parsed_data):
    # Initialize a data structure to store the output for each time
    simulation_results = {}

    #loop through times in stim data
    for time, wire in stimuli_parsed_data.items():
        for signal, value in wire.items():
            verilog_parsed_data["inputs"][signal]

# for each time, update all given then update wires and output them.




# Usage example
circuit_num = 1
verilog_parsed_data = parse_verilog_file(circuit_num)
if verilog_parsed_data:
    print("Inputs:", verilog_parsed_data["inputs"])
    print("Outputs:", verilog_parsed_data["outputs"])
    print("Wires:", verilog_parsed_data["wires"])
    print("Gates:", verilog_parsed_data["gates"])

stimuli_parsed_data = parse_stimuli_file(circuit_num)
print("\nStimuli Parsed Data:")
print(stimuli_parsed_data)

# Run the simulator
simulation_results = simulator(verilog_parsed_data, stimuli_parsed_data)
print("\nSimulation Results:")
for time, output in sorted(simulation_results.items()):
    print(f"Time: {time} ms, Outputs: {output}")




# Usage example
circuit_num = 1
verilog_parsed_data = parse_verilog_file(circuit_num)
if verilog_parsed_data:
    print("Inputs:", verilog_parsed_data["inputs"])
    print("Outputs:", verilog_parsed_data["outputs"])
    print("Wires:", verilog_parsed_data["wires"])
    print("Gates:", verilog_parsed_data["gates"])

stimuli_parsed_data = parse_stimuli_file(circuit_num)

simulation_results = simulator(verilog_parsed_data, stimuli_parsed_data)
print(simulation_results)