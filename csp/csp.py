class csp(object):

    def __init__(self, domains,arcs, constraint):
        self.domains = domains # key -> [1-9]
        self.arcs = arcs
        self.constraint = constraint

    def show_domains(self):
        print('Dominio:')
        for key in self.domains:
            print('%s :' %(key)),
            print(self.domains[key])

    def show_arcs(self):
        print('Vizinho:')
        for key in self.arcs:
            print('%s :' %(key)),
            print(' '.join(self.arcs[key]))

    
