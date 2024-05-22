import matplotlib.pyplot as plt
import networkx as nx
from fpdf import FPDF

# Define the number of registers available
NUM_REGISTERS = 4
REGISTERS = ["R1", "R2", "R3", "R4"]

# Example basic blocks
blocks = [
    {"id": 1, "instructions": ["a", "b", "c"], "liveIn": {"a", "b"}, "liveOut": {"c"}},
    {"id": 2, "instructions": ["b", "d", "e"}, "liveIn": {"b"}, "liveOut": {"d", "e"}}
]

# Create the interference graph
def create_interference_graph(blocks):
    graph = nx.Graph()
    
    for block in blocks:
        live = set(block["liveOut"])
        for var in reversed(block["instructions"]):
            if var in live:
                live.remove(var)
            for live_var in live:
                graph.add_edge(var, live_var)
            live.add(var)
    
    return graph

# Create and draw the interference graph
graph = create_interference_graph(blocks)

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=16)
plt.title("Interference Graph")
plt.savefig('/mnt/data/interference_graph.png')
plt.show()

# Allocate registers
def allocate_registers(graph):
    degree = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    simplify_stack = []
    allocation = {}
    removed_nodes = set()

    while degree:
        node = min(degree, key=degree.get)
        simplify_stack.append(node)
        neighbors = list(graph.neighbors(node))
        removed_nodes.add(node)
        for neighbor in neighbors:
            if neighbor in degree:
                degree[neighbor] -= 1
        degree.pop(node)

    while simplify_stack:
        node = simplify_stack.pop()
        neighbors = list(graph.neighbors(node))
        forbidden = {allocation[neighbor] for neighbor in neighbors if neighbor in allocation and neighbor not in removed_nodes}
        for reg in REGISTERS:
            if reg not in forbidden:
                allocation[node] = reg
                break

    return allocation

allocation = allocate_registers(graph)

# Create and draw the allocation result
def draw_allocation(allocation):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')
    table_data = [["Variable", "Register"]] + [[var, reg] for var, reg in allocation.items()]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1.2, 1.2)
    plt.title("Register Allocation")
    plt.savefig('/mnt/data/register_allocation.png')
    plt.show()

draw_allocation(allocation)

# Create PDF
pdf = FPDF()

# Add a page
pdf.add_page()
pdf.set_font("Arial", size = 12)

# Title
pdf.set_font("Arial", size = 16)
pdf.cell(200, 10, txt = "Register Allocation Visualization", ln = True, align = 'C')

# Add the code
pdf.set_font("Arial", size = 12)
code = """#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <stack>
#include <string>
#include <algorithm> // Include this header for find_if

using namespace std;

const int NUM_REGISTERS = 4;
const string REGISTERS[NUM_REGISTERS] = {"R1", "R2", "R3", "R4"};

struct BasicBlock {
    int id;
    vector<string> instructions;
    set<string> liveIn;
    set<string> liveOut;
};

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

map<string, string> allocateRegisters(const InterferenceGraph &graph) {
    map<string, int> degree;
    stack<string> simplifyStack;
    map<string, string> allocation;

    for (const auto &node : graph.adjList) {
        degree[node.first] = node.second.size();
    }

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
}"""
pdf.multi_cell(0, 10, code)

# Add explanation for Interference Graph
pdf.set_font("Arial", size = 14)
pdf.cell(200, 10, txt = "Interference Graph Creation", ln = True, align = 'L')
pdf.set_font("Arial", size = 12)
pdf.multi_cell(0, 10, "The interference graph is created by analyzing the live variable information at each point in the program. Variables that are live at the same time interfere with each other and are connected in the graph.")

# Add Interference Graph image
pdf.image('/mnt/data/interference_graph.png', x = 10, y = None, w = 190)

# Add explanation for Register Allocation
pdf.set_font("Arial", size = 14)
pdf.cell(200, 10, txt = "Register Allocation Process", ln = True, align = 'L')
pdf.set_font("Arial", size = 12)
pdf.multi_cell(0, 10, "The register allocation is performed using a graph coloring algorithm. Nodes are removed from the graph and added to a stack if their degree is less than the number of available registers. Registers are then assigned to nodes from the stack ensuring no two adjacent nodes have the same register.")

# Add Register Allocation image
pdf.image('/mnt/data/register_allocation.png', x = 10, y = None, w = 190)

# Save the PDF
pdf_output_path = "/mnt/data/Register_Allocation_Visualization.pdf"
pdf.output(pdf_output_path)

pdf_output_path &#8203;``【oaicite:0】``&#8203;
