from collections import defaultdict


class KMP:
    def __init__(self, needle, haystack):
        self.needle = needle.upper()
        self.haystack = haystack.upper()

    def __partial_match_table(self):
        pmt = [0]

        for i in range(1, len(self.needle)):
            j = pmt[i-1]

            while j > 0 and self.needle[j] != self.needle[i]:
                j = pmt[j-1]
            pmt.append(j + 1 if self.needle[j] == self.needle[i] else j)
        return pmt

    def search(self):
        partial = self.__partial_match_table()
        result = defaultdict(list)
        j = 0

        for i in range(len(self.haystack)):
            while j > 0 and self.haystack[i] != self.needle[j]:
                j = partial[j - 1]
            if self.haystack[i] == self.needle[j]:
                j += 1
            if j == len(self.needle):
                result[self.needle].append(i - (j-1))
                j = partial[j - 1]
        return result
