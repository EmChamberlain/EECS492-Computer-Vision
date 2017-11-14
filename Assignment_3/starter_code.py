import glob, math, os, re, string, sys

class PreProcess:

    def __init__(self): pass

    ## Function to print the confusion matrix.
    ## Argument 1: "actual" is a list of integer class labels, one for each test example.
    ## Argument 2: "predicted" is a list of integer class labels, one for each test example.
    ## "actual" is the list of actual (ground truth) labels.
    ## "predicted" is the list of labels predicted by your classifier.
    ## "actual" and "predicted" MUST be in one-to-one correspondence.
    ## That is, actual[i] and predicted[i] stand for testfile[i].
    def printConfMat(self, actual, predicted):
        all_labels = sorted(set(actual + predicted))
        assert (len(actual) == len(predicted))
        confmat = {}  ## Confusion Matrix
        for i, a in enumerate(actual): confmat[(a, predicted[i])] = confmat.get((a, predicted[i]), 0) + 1
        print
        print
        print "0".zfill(2),   ## Actual labels column (aka first column)
        for label2 in all_labels:
            print str(label2).zfill(2),
        print
        for label in all_labels:
            print str(label).zfill(2),
            for label2 in all_labels:
                print str(confmat.get((label, label2), 0)).zfill(2),
            print


    ## Function to remove leading, trailing, and extra space from a string.
    ## Inputs a string with extra spaces.
    ## Outputs a string with no extra spaces.
    def remove_extra_space(self, input_string):
        return re.sub("\s+", " ", input_string.strip())

    ## Tokenizer.
    ## Input: string
    ## Output: list of lowercased words from the string
    def word_tokenize(self, input_string):
        extra_space_removed = self.remove_extra_space(input_string)
        punctuation_removed = "".join([x for x in extra_space_removed if x not in string.punctuation])
        lowercased = punctuation_removed.lower()
        return lowercased.split()




class BernoulliNaiveBayes:

    def read_truth(self):
        truth = {}
        with open("test_ground_truth.txt") as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]
        self.letter = self.train_test_dir[self.train_test_dir.find("/problem") + 8:self.train_test_dir.find("/problem") + 9]
        for line in content:
            if line.find("problem" + self.letter) != -1:
                example = line[line.find(self.letter + "sample") + 7: line.find(self.letter + "sample") + 9]
                author = line[-2:]
                truth[example] = author
        return truth


    def __init__(self, train_test_dir, vocab, p = None):
        self.train_test_dir = train_test_dir
        self.vocab = vocab
        self.p = p
        self.prior = {}
        self.condprob = {}
        self.all_labels = []
        self.truth = self.read_truth()
        self.predicted = {}
        self.frequency = {key: 0 for key in self.vocab}


    ## Define Train function
    def train(self):

        author_dict = {}  # N_{ci}
        author_occur = {}  # N_c
        train_total_count = 0  # N

        filepath = self.train_test_dir + "?train??-*.txt"
        filenames = glob.glob(filepath)
        for filename in filenames:
            dict_temp = {key: False for key in self.vocab}
            author = filename[filename.find("train") + 5: filename.find("train") + 7]
            # example = filename[-5:-4]
            f = open(filename, 'r')
            words = self.p.word_tokenize(f.read())

            if author not in self.all_labels:
                author_dict[author] = {key: 0 for key in self.vocab}
                author_occur[author] = 0
                self.all_labels.append(author)
            author_occur[author] += 1
            train_total_count += 1
            for word in words:
                if word in self.vocab:
                    dict_temp[word] = True
                    self.frequency[word] += 1
            for word in dict_temp:
                if dict_temp[word]:
                    author_dict[author][word] += 1



        for author in self.all_labels:
            self.prior[author] = float(author_occur[author]) / float(train_total_count)
            self.condprob[author] = {}
            for word in author_dict[author]:
                self.condprob[author][word] = float((author_dict[author][word] + 1)) / float((author_occur[author] + 2))


    ## Define Test function
    def test(self):
        filepath = self.train_test_dir + "?sample??.txt"
        filenames = glob.glob(filepath)

        for filename in filenames:
            example = filename[filename.find("sample") + 6: filename.find(".txt")]
            f = open(filename, 'r')
            words = self.p.word_tokenize(f.read())

            best_label = None
            max_log_prob = 0
            for label in self.all_labels:
                log_prob = math.log(self.prior[label], 2)
                for vocab_word in self.vocab:
                    if vocab_word in words:
                        log_prob += math.log(self.condprob[label][vocab_word], 2)
                    else:
                        log_prob += math.log(1 - self.condprob[label][vocab_word], 2)

                if best_label is None:
                    best_label = label
                    max_log_prob = log_prob

                if max_log_prob < log_prob:
                    best_label = label
                    max_log_prob = log_prob

            self.predicted[example] = best_label








