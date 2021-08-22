from collections import defaultdict


class Automaton:
    def __init__(self, words):
        self.max_states = sum([len(word) for word in words])
        self.max_char = 26
        self.out = [0] * (self.max_states + 1)
        self.fail = [-1] * (self.max_states + 1)
        self.goto = [[-1] * self.max_char for _ in range(self.max_states + 1)]
        self.words = [word.upper() for word in words]
        self.states = self.__build_automaton()

    def __build_automaton(self):
        states = -1

        for i in range(len(self.words)):
            word = self.words[i]
            current_state = 0

            for char in word:
                ch = ord(char) - 65

                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1
                current_state = self.goto[current_state][ch]
            self.out[current_state] |= (1 << i)

        for ch in range(self.max_char):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0

        queue = []

        for ch in range(self.max_char):
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        while queue:
            state = queue.pop(0)

            for ch in range(self.max_char):
                if self.goto[state][ch] != -1:
                    failure = self.fail[state]

                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]

                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
                    self.out[self.goto[state][ch]] |= self.out[failure]

                    # Insert the next level node (of Trie) in Queue
                    queue.append(self.goto[state][ch])
        return states

    def __find_next_state(self, current_state, next_input):
        ans = current_state
        ch = ord(next_input) - 65  # the char A has a decimal value of 65
        while self.goto[ans][ch] == -1:
            ans = self.fail[ans]

        return self.goto[ans][ch]

    def search(self, haystack):
        haystack = haystack.upper()
        current_state = 0
        result = defaultdict(list)

        for i in range(len(haystack)):
            current_state = self.__find_next_state(current_state, haystack[i])

            if self.out[current_state] == 0:
                continue

            for j in range(len(self.words)):
                if (self.out[current_state] & (1 << j)) > 0:
                    word = self.words[j]

                    result[word].append(i - len(word) + 1)
        return result
