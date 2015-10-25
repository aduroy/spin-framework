#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: Antonin Duroy
'''

import re
import random
import matplotlib.pyplot as plt

from collections import OrderedDict
from text_similarity import jaccard_similarity, cosine_similarity, jaro_winkler_similarity
from tree import SpinTree
from utils import insert_at_position

class Spin():
    
    def __init__(self, masterspin=None, input_file=None):
        # Placeholders used for building tree representation
        self.placeholders = OrderedDict([])
        if masterspin is not None:
            self.masterspin = masterspin
        elif input_file is not None:
            self.masterspin = self.__open_file(input_file)
        else:
            raise ValueError("A masterspin must be specified.")
    
    def unspin(self, delimiter='|'):
        """ Generate a spun from the masterspin
        """
        spun_string = self.masterspin
        while True:
            spun_string, n = re.subn('{([^{}]*)}',
                lambda m: random.choice(m.group(1).split(delimiter)),
                spun_string)
            if n == 0:
                break
        return spun_string.strip()
    
    def build_tree(self, delimiter='|'):
        """ Build a tree representation of the masterspin
        e.g.:
            masterpin: {a|{b|c}}{d|e}
            tree:
                (AND)
                +--- (OR)
                |    +--- a
                |    +--- (OR)
                |         +--- b
                |         +--- c
                +--- (OR)
                     +--- d
                     +--- e
        """
        def repl(a):
            """ Replacement function for every non-overlapping occurrence of pattern in re.subn()
            """
            perforations = a.group(1).split(delimiter)
            parent = SpinTree(or_=True)
            placeholder = '__NODE__'+str(random.randint(0, 10000))
            while placeholder in self.placeholders:
                placeholder = '__NODE__'+str(random.randint(0, 10000))
            insert_index = -1
            for perfo in perforations:
                s_perfo = [perfo]
                for ph in self.placeholders:
                    for i, chunk in enumerate(s_perfo):
                        if isinstance(chunk, SpinTree):
                            continue
                        sp = chunk.split(ph)
                        if len(sp) == 2: # Because every placeholder is unique
                            s_perfo = [node for node in s_perfo[:i] + [sp[0], self.placeholders[ph], sp[1]] + s_perfo[i+1:] if node != '']
                            insert_index = list(self.placeholders.keys()).index(ph)
                            self.placeholders.pop(ph)
                            break
                if len(s_perfo) == 1 and not isinstance(s_perfo[0], SpinTree):
                    child = SpinTree(value=perfo)
                elif len(s_perfo) == 1 and isinstance(s_perfo[0], SpinTree):
                    child = s_perfo[0]
                else:
                    child = SpinTree(and_=True)
                    for and_child in s_perfo:
                        if isinstance(and_child, SpinTree):
                            child.add_child(and_child)
                        else:
                            child.add_child(SpinTree(value=and_child))
                parent.add_child(child)
            # Insert the new placeholder at the right position
            self.placeholders = insert_at_position(self.placeholders, insert_index, (placeholder, parent))
            return placeholder
        
        masterspin = self.masterspin
        while True:
            masterspin, n = re.subn('{([^{}]*)}',
                repl,
                masterspin)
            if n == 0:
                s_masterspin = [masterspin]
                for ph in self.placeholders:
                    for i, chunk in enumerate(s_masterspin):
                        if isinstance(chunk, SpinTree):
                            continue
                        sp = chunk.split(ph)
                        if len(sp) == 2: # Because every placeholder is unique
                            s_masterspin = [node for node in s_masterspin[:i] + [sp[0], self.placeholders[ph], sp[1]] + s_masterspin[i+1:] if node != '']
                            self.placeholders.pop(ph)
                            break
                if len(s_masterspin) == 1 and not isinstance(s_masterspin[0], SpinTree):
                    return SpinTree(value=masterspin)
                elif len(s_masterspin) == 1 and isinstance(s_masterspin[0], SpinTree):
                    return s_masterspin[0]
                else:
                    final_tree = SpinTree(and_=True)
                    for and_child in s_masterspin:
                        if isinstance(and_child, SpinTree):
                            final_tree.add_child(and_child)
                        else:
                            final_tree.add_child(SpinTree(value=and_child))
                    return final_tree
    
    def plot_duplicate_evolution(self, iterations, save_file=None):
        """ Generate n (=iterations) spuns and compare their similarities 2 by 2, then plot
        or save the results in order to visualize the masterpin limit
        """
        def add_subplot(x, y, title, position):
            """
            """
            plt.subplot(position)
            plt.bar(x, y)
            plt.grid(True)
            plt.title(title)
            x1,x2,y1,y2 = plt.axis()
            plt.axis((x1,x2,y1,1))
        
        spuns = []
        x = []
        jaccard_sim = []
        jaro_winkler_sim = []
        cosine_sim = []
        for i in range(iterations):
            x.append(i)
            new_spun = self.unspin()
            tmp_max_jaccard = 0
            tmp_max_jaro_winkler = 0
            tmp_max_cosine = 0
            for spun in spuns:
                split_spun = spun.split()
                split_new_spun = new_spun.split()
                tmp_max_jaccard = max(tmp_max_jaccard, jaccard_similarity(split_new_spun, split_spun))
                tmp_max_jaro_winkler = max(tmp_max_jaro_winkler, jaro_winkler_similarity(split_new_spun, split_spun))
                tmp_max_cosine = max(tmp_max_cosine, cosine_similarity(split_new_spun, split_spun))
                
            jaccard_sim.append(tmp_max_jaccard)
            jaro_winkler_sim.append(tmp_max_jaro_winkler)
            cosine_sim.append(tmp_max_cosine)
            spuns.append(new_spun)
        
        # Jaccard
        add_subplot(x, sorted(jaccard_sim), 'Jaccard', 311)
        
        # Jaro Winkler
        add_subplot(x, sorted(jaro_winkler_sim), 'Jaro Winkler', 312)
        
        # Cosine
        add_subplot(x, sorted(cosine_sim), 'Cosine', 313)
        
        if save_file is not None:
            plt.savefig(save_file)
        else:
            plt.show()
    
    def __open_file(self, path):
        with open(path, "r", encoding='utf-8') as masterspin:
            return masterspin.read()


if __name__ == "__main__":
#    spin = Spin(input_file='')
    spin = Spin("{My name is|I{ am|'m}} John Doe and I {truly|really} love the {spintax|spin framework}{.|!}")
    tree = spin.build_tree()
    print(tree)
    spin.plot_duplicate_evolution(25)