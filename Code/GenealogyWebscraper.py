import sys
import requests

'''
This finds the set of ancestors for a set of mathematicians from mathgenealogy.org.
It is very brute force-y, so if they reformat their website, it will probably break.
Users can add as many IDs to the start as they want, and get the complete \"family tree\" as output.
Input: A list of IDs (from https://www.mathgenealogy.org)
Output: A tree of ancestors in the GraphViz Dot format (https://graphviz.org/doc/info/lang.html)

How to run:
From Command line
python GenealogyWebscraper.py id1 id2 ... idn
Calling within a python script
find([id1, id2, ..., idn])
'''

class Person:
    def __init__(self, name, ident,classification):
        self.name = name
        self.ident = ident
        self.classification = classification
        self.parents = []
        self.children = []

'''
Input: List of IDs for the origin nodes
Output: Graph containing all ancestors of these nodes
'''
def find(starting_ids):
    graph = []
    added = []
    stack = []
    # Do the whole thing for the first people first, then run the noraml loop
    for current in starting_ids:
        added += [current]
        url = "https://www.mathgenealogy.org/id.php?id=" + current
        r = requests.get(url, allow_redirects=True)
        name = getName(str(r.text))
        c = getClass(str(r.content))
        p = Person(name,current,c)
        p.parents = getParents(str(r.content))
        p.children = getChildren(str(r.content))
        for p_prime in p.parents:
            if p_prime not in stack and p_prime not in added:
                stack += [p_prime]
        graph += [p]
    # Main loop
    while stack != []:
        current = stack[0]
        stack = stack[1:]
        added += [current]
        url = "https://www.mathgenealogy.org/id.php?id=" + current
        r = requests.get(url, allow_redirects=True)
        name = getName(str(r.text))
        c = getClass(str(r.content))
        p = Person(name,current,c)
        p.parents = getParents(str(r.content))
        p.children = getChildren(str(r.content))
        for p_prime in p.parents:
            if p_prime not in stack and p_prime not in added:
                stack += [p_prime]
        graph += [p]
    return makeGraphViz(graph)


'''
Input: Graph (using the person class above)
Output: GraphViz dot format digraph (Supervisor -> Student)
'''
def makeGraphViz(g): # Make a representation of the graph using the graph viz dot lang.
    output = "digraph D {\nnode [shape=record];\n"
    # make the nodes
    for p in g:
        output += p.ident + " [label=\"" + p.name + "\"]\n"
    # make the edges
    for p in g:
        parents = "{ "
        for p_prime in p.parents:
            parents += p_prime + ","
        parents = parents[:-1] + "}"
        if p.parents != []:
            output += parents + " -> " + p.ident + ";\n"
    output += "}"
    return output


'''
Input: HTML code from a mathgeneolagy webpage
Output: The name of the person
'''
def getName(webpage):
    for l in webpage.split('\n'):
        if "<title>" in l:
            return (l[7:]).split(" - ")[0]
    return None


'''
Input: HTML code from a mathgeneolagy webpage
Output: The classification of their thesis
'''
def getClass(webpage):
    for l in webpage.split('\\n'):
        if "Mathematics Subject Classification:" in l:
            return l.split("Mathematics Subject Classification:")[1].split("&")[0]
    return 0

# Going to leave mostly blank atm, may fix later
def getChildren(webpage):
    if "No students known." in webpage:
        return []
    return []
    

'''
Input: HTML code from a mathgeneolagy webpage
Output: List of ids of the supervisors
'''
def getParents(webpage):
    if ("Advisor: Unknown" in webpage) and ("Advisor 1" not in webpage) and ("Advisor: <a" not in webpage):
        return []
    parents = []
    count = 0
    for l in webpage.split('\\n'):
        if "Advisor" in l:
            l_prime = l
            if "Advisor: <a" in l:
                p1 = l_prime.split("Advisor: ")[1].split("href=\"id.php?id=")
                p2 = p1[1]
                p3 = p2.split('\"')[0]
                parents += [p3]
                # parents += [l_prime.split("Advisor: ")[1].split("href=\"id.php?id=")[1].split('\"')[0]]
            for i in range(1,100): # Brute force advisor combos
                if "Advisor " + str(i) in l_prime:
                    parents += [l_prime.split("Advisor " + str(i))[1].split("href=\"id.php?id=")[1].split('\"')[0] ]
    return parents


'''
Code to run as a command line program.
'''
if __name__ == "__main__":
    print(find(sys.argv[1:]))
