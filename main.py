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

    # Loop through times in stimuli data
    for time, signal_datas in stimuli_parsed_data.items():
        # Update inputs based on the stimuli at the current time
        for signal, value in signal_datas.items():
            verilog_parsed_data["inputs"][signal] = value

        # Process each gate to update wires and outputs
        for gate_id, gate in verilog_parsed_data["gates"].items():
            output_wire = gate["connections"][0]
            input_wires = [wire for wire in gate["connections"][1:]]
            inputslist = []

            # Populate inputslist with values from inputs or wires
            for signal in input_wires:
                if signal in verilog_parsed_data["inputs"]:
                    inputslist.append(verilog_parsed_data["inputs"][signal])
                elif signal in verilog_parsed_data["wires"]:
                    inputslist.append(verilog_parsed_data["wires"][signal])

            # Handle each gate type
            if gate["type"] == 'not':
                result = not inputslist[0]

            elif gate["type"] == 'and':
                result = all(inputslist)

            elif gate["type"] == 'or':
                result = any(inputslist)

            elif gate["type"] == 'xor':
                result = bool(sum(inputslist) % 2)  # XOR: True if odd number of True values

            elif gate["type"] == 'nand':
                result = not all(inputslist)  # NAND: True if not all inputs are True

            elif gate["type"] == 'nor':
                result = not any(inputslist)  # NOR: True if all inputs are False

            elif gate["type"] == 'xnor':
                result = not bool(sum(inputslist) % 2)  # XNOR: True if even number of True values

            elif gate["type"] == 'buf':
                result = inputslist[0]  # BUF: Pass the input directly to the output

            # Set the result in the appropriate wire or output
            if output_wire in verilog_parsed_data["wires"]:
                verilog_parsed_data["wires"][output_wire] = result
            elif output_wire in verilog_parsed_data["outputs"]:
                verilog_parsed_data["outputs"][output_wire] = result

        # Store the simulation results at the current time
        simulation_results[time] = {
            "inputs": verilog_parsed_data["inputs"].copy(),
            "wires": verilog_parsed_data["wires"].copy(),
            "outputs": verilog_parsed_data["outputs"].copy()
        }

    return simulation_results

def write_to_sim(simulation_results, output_file="output.sim"):
    with open(output_file, "w") as file:
        for time, data in simulation_results.items():
            # Writing each element's state at each time step
            for element_type, elements in data.items():
                for element, value in elements.items():
                    file.write(f"{time} {element} {int(value)}\n")
            file.write("\n")  # Adding an extra newline after each timestamp




# Usage example
circuit_num = input("Select circuit number to simulate: ")
verilog_parsed_data = parse_verilog_file(circuit_num)
# if verilog_parsed_data:
    # print(verilog_parsed_data)

stimuli_parsed_data = parse_stimuli_file(circuit_num)
# print(stimuli_parsed_data)
simulation_results = simulator(verilog_parsed_data, stimuli_parsed_data)
print(simulation_results)
write_to_sim(simulation_results)