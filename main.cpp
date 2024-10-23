#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>
using namespace std;

map<string, int> wires; // Map to store wire names and their values

// This function reads the stimuli file and returns the data as a vector of string vectors.
vector<vector<string>> read_stimuli_file(const string& filename) {
    vector<vector<string>> stimuli_data;
    ifstream file(filename); // Open the stimuli file

    // If the file can't be opened, display an error message and return an empty vector.
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return stimuli_data;
    }

    string line;
    while (getline(file, line)) {
        vector<string> tokens; // Vector to store the tokens from each line
        string token;
        size_t pos;

        // Split line by commas and extract tokens
        while ((pos = line.find(',')) != string::npos) {
            token = line.substr(0, pos);
            tokens.push_back(token);
            line.erase(0, pos + 1);
        }
        tokens.push_back(line); // Add the last token
        stimuli_data.push_back(tokens); // Add tokens to the stimuli data
    }

    file.close();
    return stimuli_data; // Return the collected stimuli data
}

// This function reads the library file and returns its content as a vector of vectors of strings.
vector<vector<string>> readLibFile(const string& filename) {
    vector<vector<string>> result;
    ifstream file("lib.lib"); // Open the library file
    string line;

    // Read each line from the file and split it by commas
    while (getline(file, line)) {
        stringstream ss(line); // Treat the line as a stream
        vector<string> vec;
        string temp_string;

        // Extract each token from the line
        while (getline(ss, temp_string, ',')) {
            vec.push_back(temp_string);
        }

        result.push_back(vec); // Store the tokens from this line
    }

    return result; // Return the library data
}

// Helper function that converts a string to an integer, extracting only the digits from the string.
int convert_to_int(const string& x) {
    string clean = ""; // Store only the digits
    for (auto i : x)
        if (isdigit(i)) clean.push_back(i);

    return stoi(clean); // Convert to integer
}

// This function reads the circuit file and returns gate definitions as a vector of vectors of strings.
vector<vector<string>> extractGateDefinitions(const string& filename) {
    vector<vector<string>> gateDefinitions;
    ifstream file(filename);
    string line;
    bool gates = false; // Flag to indicate whether we are reading gate definitions

    // Read through the file line by line
    while (getline(file, line)) {
        stringstream ss(line);
        vector<string> tokens;
        string token;

        // When reaching the "Components:" section, we start reading gate definitions
        if (line == "Components:") {
            gates = true;
            continue;
        }

        // Before "Components:", we are reading wires and initializing them to zero
        if (!gates) {
            if (line != "Inputs:") wires[line] = 0;
        } else {
            int idx = 0;
            // Extract tokens from each line
            while (getline(ss, token, ',')) {
                tokens.push_back(token);
                // From the third token onward, these are wire names that are initialized to zero
                if (idx >= 2) wires[token] = 0;
                idx++;
            }
        }
        if (!tokens.empty()) gateDefinitions.push_back(tokens); // Store the gate definition
    }
    return gateDefinitions; // Return gate definitions
}

int main() {
    vector<vector<string>> GateDef = readLibFile("lib.lib");  // Read the gate library
    vector<vector<string>> Circuit = extractGateDefinitions("1.cir"); // Read the circuit file
    vector<vector<string>> events = read_stimuli_file("stimuli1.stim"); // Read the stimuli file
    map<string, pair<int, int>> update_values; // Store the time and value for gate updates
    int time = 0; // Initialize simulation time
    vector<string> updated_wires; // Track which wires are updated at each time step

    // Simulate for a fixed period of time
    while (time < 10000) {
        // Process new events from the stimuli file
        for (auto event : events) {
            int time_stamp = convert_to_int(event[0]); // Get the time stamp
            string wire_name = event[1]; // Get the wire name
            int wire_value = convert_to_int(event[2]); // Get the wire value

            // If the current time matches the event's time stamp, update the wire
            if (time == time_stamp) {
                wires[wire_name] = wire_value; // Update wire value
                updated_wires.push_back(wire_name); // Track the updated wire
                cout << time << " " << wire_name << " " << wire_value << "\n";
            }
        }

        // Apply pending updates
        for (auto i : update_values) {
            if (i.second.first == time) { // If the update is due at this time
                wires[i.first] = i.second.second; // Update the wire
                cout << i.second.first << " " << i.first << " " << i.second.second << "\n";
                updated_wires.push_back(i.first); // Track the update
            }
        }

        // Process the gates from the circuit
        for (int k = 0; k < Circuit.size(); k++) {
            if (Circuit[k][1] == "AND") {
                bool skip = true; // Assume no new event by default
                int temp = 1; // Initialize the AND result
                for (int i = 3; i < Circuit[k].size(); i++) {
                    temp = temp & wires[Circuit[k][i]]; // Perform AND operation on input wires
                    auto lookup = find(updated_wires.begin(), updated_wires.end(), Circuit[k][i]);
                    if (lookup != updated_wires.end()) skip = false; // Check if any input wire is updated
                }

                // If any input wire was updated, schedule an update for the output wire
                if (!skip) {
                    int delay = 0;
                    for (int g = 0; g < GateDef.size(); g++) {
                        if (GateDef[g][0] == "AND") delay = convert_to_int(GateDef[g][3]);
                    }
                    update_values[Circuit[k][2]] = {time + delay, temp};
                }
            }

            if (Circuit[k][1] == "OR") {
                bool skip = true;
                int temp = 0; // Initialize the OR result
                for (int i = 3; i < Circuit[k].size(); i++) {
                    temp = temp | wires[Circuit[k][i]]; // Perform OR operation on input wires
                    auto lookup = find(updated_wires.begin(), updated_wires.end(), Circuit[k][i]);
                    if (lookup != updated_wires.end()) skip = false;
                }

                // If any input wire was updated, schedule an update for the output wire
                if (!skip) {
                    int delay = 0;
                    for (int g = 0; g < GateDef.size(); g++) {
                        if (GateDef[g][0] == "OR") delay = convert_to_int(GateDef[g][3]);
                    }
                    update_values[Circuit[k][2]] = {time + delay, temp};
                }
            }

            if (Circuit[k][1] == "NOR") {
                bool skip = true;
                int temp = 0; // Initialize the NOR result
                for (int i = 3; i < Circuit[k].size(); i++) {
                    temp = temp | wires[Circuit[k][i]]; // Perform OR operation on input wires
                    auto lookup = find(updated_wires.begin(), updated_wires.end(), Circuit[k][i]);
                    if (lookup != updated_wires.end()) skip = false;
                }

                // Invert the result for NOR gate
                temp = !temp;

                // If any input wire was updated, schedule an update for the output wire
                if (!skip) {
                    int delay = 0;
                    for (int g = 0; g < GateDef.size(); g++) {
                        if (GateDef[g][0] == "NOR") delay = convert_to_int(GateDef[g][3]);
                    }
                    update_values[Circuit[k][2]] = {time + delay, temp};
                }
            }
        }

        time++; // Increment simulation time
    }

    return 0;
}
