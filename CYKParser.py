import random


class CYK:

    def __init__(self, folderpath):

        self.grammar_rules = self.rules(folderpath)
        self.nonterminals, self.terminals = self.get_all_nonterminals(self.grammar_rules)

    def rules(self, folderpath):
        rules = dict()
        for line in open(folderpath, encoding='utf-8'):
            sentences = list()
            non_terminals = list()

            if line != "\n":
                if not line.startswith("#") and line != "\n": # comment line control

                    line = line.replace("\n", "").strip().split("\t")

                    if any("#" in word for word in line): # if "#" token in separated words

                        terminal = line[1].split("#")[0]  # seperate with according to "#" token

                        sentences.append(line[0])
                        sentences.append(terminal)

                        non_terminals.append(sentences[1])

                        # dict values are 2d arrays.
                        # Because a non-terminal can get more than one right hand side
                        # exp: NP->Pronoun, NP->NP Det Noun, NP->NP PP
                        if sentences[0] not in rules.keys():
                            rules[sentences[0]] = list()
                            rules[sentences[0]].append(non_terminals)
                        else:
                            rules[sentences[0]].append(non_terminals)

                    else:  # if "#" token not in separated words

                        lines = line[0].split(" ") # split for some gaps in line

                        # if last element of lines is like ['NP', '', 'Pronoun']
                        # use that variable --> lines
                        if len(lines) > 1 and lines[len(lines)-1] != "":
                            non_terminals.append(lines[2])

                        # if last element of lines is like ['NP', '']
                        # use that variable --> line which is the outermost
                        else:
                            # lines[0] = lines[0].strip()
                            non_terminals.append(line[1])

                        # dict values are 2d arrays.
                        # Because a non-terminal can get more than one right hand side
                        # exp: NP->Pronoun, NP->NP Det Noun, NP->NP PP
                        if lines[0] not in rules.keys():
                            rules[lines[0]] = list()
                            rules[lines[0]].append(non_terminals)
                        else:
                            rules[lines[0]].append(non_terminals)

        return rules

    # The purpose of this function, starting from the initial rule,
    # comes to the terminal node by choosing random rules.
    # Then random words are selected from these leaf nodes.
    # takes 'ROOT' and rules as parameters.
    # returns generated random sentences
    def create_sentence(self, root, rules):

        all_rules = list()
        non_terminals = list() # for get non-terminals
        terminals = list() # for get terminals
        punctuations = list() # for get punctuation

        non_terminals.append(root)
        all_rules.append(non_terminals)

        while len(all_rules) != 0:
            # It was kept in the 2D list
            # since non-terminals will continue while adding and branching.
            if len(all_rules) == 1:
                curr = all_rules[0][0]
                all_rules[0].remove(all_rules[0][0])

                if not all_rules[0]:
                    all_rules.remove(all_rules[0])
            # If it has passed to a new branch,
            # it takes the first element of that branch as current.
            else:
                curr = all_rules[-1][0]
                all_rules[-1].remove(all_rules[-1][0])

                if not all_rules[-1]:
                    all_rules.remove(all_rules[-1])

            flag = False
            non_terminals = []
            unit = random.choices(rules[curr])[0][0].split() # random rule is selected

            for element in unit:

                if element in rules: # terminal in rules
                    flag = True
                    non_terminals.append(element) # terminals
                else:
                    # If after the non-terminal, the terminal is looped,
                    # it triggers the flag and is added to terminal s3.
                    if flag:
                        punctuations.append(element) # punctuation
                    else:
                        terminals.append(element) # non-terminals

            # the list is reset each time, its copy is placed in the general list before reset.
            if flag:
                all_rules.append(non_terminals.copy())

        # words are combined in the list of s2 and then s3.
        sentence = " ".join(terminals) + " " + " ".join(punctuations)

        return sentence

    # it takes random sentences with words and generates sentence.
    # returns that sentence
    def create_sentence_with_words(self, terminals):

        words = list()
        sentence = list()

        for terminal in terminals: # terminals in the list are moved in to another list
            words.append(terminal[1])

        for i in range(8): # sentence length
            sentence.append(random.choices(words)[0])

        return sentence

    # it generates random sentences according to sentence length and sentence number.
    # The generate process starts from root and follows the rules in an iterative way.
    # write generated sentences to output file
    # return generated sentences.
    def randsentence(self, rules, text_file):

        all_sentences = list()
        for i in range(1000):

            sentence = self.create_sentence('ROOT', rules)
            sentence_split = sentence.split()
            if (len(sentence_split) > 5) and (15 > len(sentence_split)): # sentence length
                all_sentences.append(sentence_split)

            if len(all_sentences) > 20: # sentence number
                break

        with open(text_file, "w") as file:
            for sentence in all_sentences:
                sentence = " ".join(sentence)
                file.write(sentence + "\n")

        return all_sentences

    # it generates random sentences according to sentence length and sentence number.
    # The generate process consists of collecting all terminal words and selecting them randomly.
    # write generated sentences to output file
    # return generated sentences.
    def randsentence_with_words(self, terminals, text_file):

        all_sentences = list()
        for i in range(1000):

            sentence = self.create_sentence_with_words(terminals)

            all_sentences.append(sentence)

            if len(all_sentences) > 10: # sentence number
                break

        with open(text_file, "w") as file:
            for sentence in all_sentences:
                sentence = " ".join(sentence)
                file.write(sentence + "\n")

        return all_sentences

    # Finds non-terminals of that sentence then return this array.
    def get_nonterminal_of_sentence(self, sentence):

        lefthand_side = list()

        rules_keys = list(self.grammar_rules.keys())

        for word in sentence:
            for key in rules_keys:
                for values in self.grammar_rules[key]:
                    if [word] == values: # if words in dict
                        lefthand_side.append(key) # find key, left hand side

        return lefthand_side

    # Finds all non-terminals of the rules dictionary then return this array.
    def get_all_nonterminals(self, rules):

        nonterminals = list()
        terminals = list()

        for key in rules:
            for values in rules[key]:
                for value in values:
                    if str.islower(value):  # if is terminal
                        terminals.append([key, value])
                    else:
                        nonterminals.append([key, value])

        return nonterminals, terminals

    # creates set of string from concatenation of each character in first
    # to each character in second
    # parameters are first and second set of characters
    # then returns set of desired values
    def get_cell_rule(self, first, second, left, right):

        rule = set()
        if first == set() or second == set():
            return set()

        # for exp: first is Verb and second is Pronoun
        # there is no such rule that 'Verb Pronoun' but there is
        # condition which is NP -> Pronoun and
        # then there is cond. like NP -> Verb NP
        # therefore this loop renews the array.
        for i in second:
            if i in right:
                second.clear()
                second.add(left[right.index(i)])

        # for exp: first is Verb and second is Pronoun
        # there is no such rule that 'Verb Pronoun' but there is
        # condition which is NP -> Pronoun and
        # then there is cond. like NP -> Verb NP
        # therefore this loop renews the array.
        for i in first:
            if i in right:
                first.clear()
                first.add(left[right.index(i)])

        for f_rule in first:
            for s_rule in second:
                rule.add(f_rule + " " + s_rule)
        return rule

    # This function is find out whether the sentence is grammatically correct.
    # Take the sentences and nonterminals(rules) as parameters
    def CYKParser(self, sentences, nonterminals):

        for sentence in sentences:
            words = sentence
            # If it fulfills the condition,
            # it takes the part after this string into the table.
            if "is it true that" in " ".join(sentence):
                if "." or "!" or "?" in " ".join(sentence):
                    # punctuation at the end of the sentence is not included in the table.
                    sentence = sentence[:-1]

                # finds the non-terminals of the remaining sentence.
                non_terminals_of_sentence = self.get_nonterminal_of_sentence(sentence[4:])
                n = len(sentence[4:])

            # it takes whole part of string into the table.
            else:
                if "." or "!" or "?" in " ".join(sentence):
                    # punctuation at the end of the sentence is not included in the table.
                    sentence = sentence[:-1]

                # find non-terminals of that sentence
                non_terminals_of_sentence = self.get_nonterminal_of_sentence(sentence)
                n = len(sentence)

            # creates left hand and right hand side lists for non-terminals.
            left = [n_ter[0] for n_ter in nonterminals]
            right = [n_ter[1] for n_ter in nonterminals]

            # Initialize empty table
            table = [[set() for j in range(n - i)] for i in range(n)]

            # Initialize first row of table
            for w in range(n):
                init_symbols = non_terminals_of_sentence[w] # non-terminal of that word
                table[0][w].add(init_symbols) # fill the table that non-terminal

            # It goes from the bottom up to the last element,
            # evaluating the cells individually.
            # It deals with all states and sets for each cell.
            for row in range(1, n): # fills the rows from the 2nd row according to bottom up.
                for col in range(n - row): # column cell in the row.
                    for k in range(row):
                        # find models of that cell. exp: unigram-bigram, bigram-unigram
                        cell_rule = self.get_cell_rule(table[k][col], table[row - k - 1][col + k + 1], left, right)
                        for rule in cell_rule:
                            if rule in right:
                                table[row][col].add(left[right.index(rule)])

            # if the last element of table contains "S" the input belongs to the grammar
            if 'S' in table[-1][-1]:
                print("CORRECT -->", " ".join(words))
            else:
                print("INCORRECT -->", " ".join(words))


if __name__ == '__main__':

    grammar_file = "cfg.gr"
    cyk = CYK(grammar_file)
    text_file = "output.txt"

    generated_sentences = cyk.randsentence(cyk.grammar_rules, text_file)
    generated_sentences_with_words = cyk.randsentence_with_words(cyk.terminals, text_file)

    # combine generated words by rule and generated random words .
    generated_sentences.extend(generated_sentences_with_words)

    cyk.CYKParser(generated_sentences, cyk.nonterminals)

