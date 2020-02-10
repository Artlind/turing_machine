import copy
import pygraphviz as pgv


class rub():
    """
    rippon class
    """
    def __init__(self, values):
        if values[0] != '0':
            self.values = ['0'] + values
        elif values[-1] != '0':
            self.values = values + ['0']
        else:
            self.values = values
    def read(self, pos):
        output = copy.copy(self.values)
        output[pos] = ">" + output[pos] + "<"
        while output[0] == '0' or output[-1] == '0':
            output.remove('0')
        return output

def machine(values, states):
    """
    Computes the output of a turing machines with states as states and
    values as the input rippon

    states is a list of dictionnaries like so :
        {input_digit : (value to overwrite, new state number, where does the head goes)}

    The last element of states has to be the final state
    """
    ruban = rub(values)
    state = states[0]
    pos = 1
    while state != states[-1]:
        apply = state[ruban.values[pos]]
        ruban.values[pos], state, pos = apply[0], states[apply[1]], pos+apply[2]
        ruban = rub(ruban.values)
        print(ruban.read(pos))
    return ruban.read(pos)

def graph(states):
    """
    Computes a graph on pygraphiz to look at the machine
    """
    graph = pgv.AGraph(directed=True)
    for i, state in enumerate(states):
        prev = 'E{}'.format(i)
        for read in state:
            next = 'E{}'.format(state[read][1])
            move = '+'
            if state[read][2] == -1:
                move = '-'
            graph.add_edge(prev, next)
            if graph.get_edge(prev, next).attr['label'] is not None:
                graph.get_edge(prev, next).attr['label'] += '\n{} ==> '.format(read)+ '{}, '.format(state[read][0])+ move
            else:
                graph.get_edge(prev, next).attr['label'] = '{} ==> '.format(read)+ '{}, '.format(state[read][0])+ move
    graph.layout('dot')
    graph.draw("graphe of the machine.png")
    graph.close()
    return


"""
Machine to do multiplication by 2
E0  =     {'0': ['0', 3, -1], '3': ['3', 0, 1], '1': ['2', 1, 1]}
E1  =     {'1': ['1', 1, 1],'3': ['3', 1, 1], '0': ['3', 2, -1]}
E2  =     {'3': ['3', 2, -1], '1': ['1', 2, -1], '2': ['2', 0, 1]}
E3  =     {'3': ['1', 3, -1], '2': ['1', 3, -1], '0': ['0', 4, 1]}
E4  =     {}
"""