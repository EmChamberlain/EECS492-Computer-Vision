from starter_code import PreProcess
from starter_code import BernoulliNaiveBayes
import sys, math
# import matplotlib.pyplot as plt

def get_vocab_list(vocab):
    with open(vocab) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def main():


    preP = PreProcess()
    BNB = BernoulliNaiveBayes(sys.argv[1], get_vocab_list("stopwords.txt"), preP)
    BNB.train()
    BNB.test()


    print "Directory: " + BNB.train_test_dir
    print

    total = 0
    correct = 0
    for example in BNB.truth:
        total += 1
        if BNB.truth[example] == BNB.predicted[example]:
            correct += 1
    print "Test Accuracy: " + str(float(correct) / float(total))
    fixed_actual = [-1] * len(BNB.truth)
    for example in BNB.truth:
        fixed_actual[int(example) - 1] = int(BNB.truth[example])
    fixed_predicted = [-1] * len(BNB.predicted)
    for example in BNB.predicted:
        fixed_predicted[int(example) - 1] = int(BNB.predicted[example])
    preP.printConfMat(fixed_actual, fixed_predicted)
    print


    CCE = {}
    for vocab_word in BNB.vocab:
        sum = 0
        for label in BNB.all_labels:
            sum += BNB.prior[label] * BNB.condprob[label][vocab_word] * math.log(BNB.condprob[label][vocab_word], 2)
        CCE[vocab_word] = -1 * sum
    CCE_sorted = [(k, CCE[k]) for k in sorted(CCE, key=CCE.get, reverse=True)]
    for x in range(20):
        print "#" + str(x + 1).zfill(2) + ": " + str(CCE_sorted[x])
    print


    freq_sorted = [k for k in sorted(BNB.frequency, key=BNB.frequency.get, reverse=True)]
    num_elem = 10
    x_axis = []
    y_axis = []
    while num_elem <= (len(freq_sorted) + 10):
        x_axis.append(num_elem)
        preP_temp = PreProcess()
        BNB_temp = BernoulliNaiveBayes(sys.argv[1], freq_sorted[:num_elem], preP_temp)
        BNB_temp.train()
        BNB_temp.test()
        total = 0
        correct = 0
        for example in BNB_temp.truth:
            total += 1
            if BNB_temp.truth[example] == BNB_temp.predicted[example]:
                correct += 1
        y_axis.append(float(correct) / float(total))
        num_elem += 10
    print "x-axis: " + str(x_axis)
    print "y-axis: " + str(y_axis)

    # *******************************
    """
    plt.plot(x_axis, y_axis, 'ro-')
    plt.title("Feature Curve for problem" + BNB.letter)
    plt.xlabel("Number of Features")
    plt.ylabel("Accuracy")
    plt.show()
    """
    # *******************************

    print






if __name__ == "__main__":
    main()
