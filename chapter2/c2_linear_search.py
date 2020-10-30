"""
nucleotide: smaller part of a gene
codon: a sequence of 3 nucleotides
gene: a sequence of codons

"""

from enum import IntEnum
from typing import Tuple, List
from random import choice

Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]

def str_to_gene(s: str) -> Gene:
    gene: Gene = []

    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    
    return gene

def linear_search(gene: Gene, search_term: Codon) -> bool:
    for codon in gene:
        if codon == search_term:
            return True
    return False



if __name__ == "__main__":
    gene_str = ''.join([choice(['A', 'C', 'G', 'T']) for i in range(0,64)])

    print(gene_str)
    my_gene: Gene = str_to_gene(gene_str)

    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)

    print(linear_search(my_gene, acg))
    print(linear_search(my_gene, gat))

    print(acg in my_gene) # Every class implemented __contains__ can do this

