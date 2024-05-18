#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <stack>
#include <string>

using namespace std;

// Define the number of registers available
const int NUM_REGISTERS = 4;
const string REGISTERS[NUM_REGISTERS] = {"R1", "R2", "R3", "R4"};

// Representation of a basic block (simplified)
struct BasicBlock {
    int id;
    vector<string> instructions;
    set<string> liveIn;
    set<string> liveOut;
};

// Representation of the interference graph
class InterferenceGraph {
public:
    map<string, set<string>> adjList;

    void addEdge(const string &u, const string &v) {
        adjList[u].insert(v);
        adjList[v].insert(u);
    }

    const set<string>& neighbors(const string &u) const {
        return adjList.at(u);
    }

    bool isNeighbor(const string &u, const string &v) const {
        return adjList.at(u).count(v) > 0;
    }
};

// Function to create an interference graph from basic blocks
InterferenceGraph createInterferenceGraph(const vector<BasicBlock> &blocks) {
    InterferenceGraph graph;

    for (const auto &block : blocks) {
        set<string> live = block.liveOut;
        for (auto it = block.instructions.rbegin(); it != block.instructions.rend(); ++it) {
            string var = *it;
            live.erase(var);
            for (const string &liveVar : live) {
                graph.addEdge(var, liveVar);
            }
            live.insert(var);
        }
    }

    return graph;
}

// Function to allocate registers using graph coloring
map<string, string> allocateRegisters(const InterferenceGraph &graph) {
    map<string, int> degree;
    stack<string> simplifyStack;
    map<string, string> allocation;

    for (const auto &node : graph.adjList) {
        degree[node.first] = node.second.size();
    }

    // Simplification phase
    while (!degree.empty()) {
        auto it = find_if(degree.begin(), degree.end(), [](const pair<string, int> &p) {
            return p.second < NUM_REGISTERS;
        });

        if (it == degree.end()) {
            cerr << "Spill detected! Simplification failed." << endl;
            return allocation;
        }

        string node = it->first;
        degree.erase(it);

        for (const string &neighbor : graph.neighbors(node)) {
            if (degree.count(neighbor)) {
                degree[neighbor]--;
            }
        }

        simplifyStack.push(node);
    }

    // Select phase
    while (!simplifyStack.empty()) {
        string node = simplifyStack.top();
        simplifyStack.pop();

        set<string> forbidden;
        for (const string &neighbor : graph.neighbors(node)) {
            if (allocation.count(neighbor)) {
                forbidden.insert(allocation[neighbor]);
            }
        }

        for (const string &reg : REGISTERS) {
            if (forbidden.count(reg) == 0) {
                allocation[node] = reg;
                break;
            }
        }
    }

    return allocation;
}

int main() {
    // Example basic blocks
    vector<BasicBlock> blocks = {
        {1, {"a", "b", "c"}, {"a", "b"}, {"c"}},
        {2, {"b", "d", "e"}, {"b"}, {"d", "e"}}
    };

    InterferenceGraph graph = createInterferenceGraph(blocks);
    map<string, string> allocation = allocateRegisters(graph);

    cout << "Register Allocation:" << endl;
    for (const auto &pair : allocation) {
        cout << pair.first << " -> " << pair.second << endl;
    }

    return 0;
}
