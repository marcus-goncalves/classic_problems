from sys import getsizeof
from random import choice

class GeneCompression:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def __str__(self) -> str:
        return self.decompress()

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1 # define a sentinel

        for nucleotide in gene.upper():
            self.bit_string <<= 2 # move 2 bits to the left

            if nucleotide == 'A':
                self.bit_string |= 0b00
            elif nucleotide == 'C':
                self.bit_string |= 0b01
            elif nucleotide == 'G':
                self.bit_string |= 0b10
            elif nucleotide == 'T':
                self.bit_string |= 0b11
            else:
                raise ValueError('Nucleotide invalid: {}'.format(nucleotide))
        
    def decompress(self) -> str:
        gene: str = ''

        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11

            if bits == 0b00:
                gene += 'A'
            elif bits == 0b01:
                gene += 'C'
            elif bits == 0b10:
                gene += 'G'
            elif bits == 0b11:
                gene += 'T'
            else:
                raise ValueError('Invalid Bits: {}'.format(bits))
        
        return gene[::-1]

if __name__ == "__main__":
    sequence: str = ''.join([choice(['A', 'C', 'G', 'T']) for i in range(0, 100)])
    print(sequence)
    print('-' * 50)
    print('Original Size: {}'.format(getsizeof(sequence)))
    compressed_seq: GeneCompression = GeneCompression(sequence)
    print('Compacted Size: {}'.format(getsizeof(compressed_seq.bit_string)))
    print(compressed_seq)
    print('Validation: {}'.format(sequence == compressed_seq.decompress()))
