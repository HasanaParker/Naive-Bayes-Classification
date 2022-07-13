"""

Hasana Parker
CS51A: Assignment 7
March 21st, 2022

"""

# _______________________________________
# Training


# Question 1
def get_file_counts(filename):
    """
    This function takes a file and returns a dictionary with the number of times each word occurs in the file.
    :param filename: (file) a file
    :return: a dictionary with the number of times a word occurs in a file
    """
    file = open(filename, "r")
    word_count_dict = {}

    for line in file:
        list_of_words = line.split()  # Make the words in the sentence into a list

        for word in list_of_words:
            if word in word_count_dict:
                word_count_dict[word] += 1  # keeps track of the amount of times a word appears.
            else:
                word_count_dict[word] = 1  # making it so that if the word is not present in the dictionary, set to 1

    file.close()

    return word_count_dict


# Question 2
def counts_to_probs(dictionary, num):
    """
    This function takes a dictionary and divides the value of each key by a number that is inputted into the function.
    :param dictionary: (dict) Any dictionary
    :param num: (int) any integer
    :return: a dictionary with the same keys as the original dictionary with the values of that original dictionary
    divided by num.
    """
    divided_dict = {}

    for key in dictionary:
        value = dictionary[key]  # setting what the value is
        new_val = value/num  # dividing the value by the num and setting it as the new value
        divided_dict[key] = new_val  # Putting the new value in a new dictionary, with the same key

    return divided_dict


# Question 3
def train_model(filename):
    """
    This function takes a file and returns a dictionary with each word and its probability to be good or bad.
    :param filename: (file) any file
    :return: dictionary with words as keys and probabilities as values.
    """
    file = open(filename, "r")
    word_prob_dict = {}

    line_count = 0  # Counting the lines in the file
    for line in file:
        line_count += 1

    file.close()
    word_count_dict = get_file_counts(filename)  # calling previous function to return a list of the word and how many
    # times it occurs
    word_prob_dict = counts_to_probs(word_count_dict, line_count)  # takes the dictionary made from the function above,
    # and divides the amount of time the word occurs by the number of lines in the file to get the probability.

    return word_prob_dict


# _______________________________________
# Classifying

# Question 4
def get_probability(word_prob_dict, sentence):
    """
    This function returns the probability of an entire sentence
    :param word_prob_dict: (dict) dictionary of word probabilities
    :param sentence: (str) a sentence representing a review.
    :return: (int) the probability of the review.
    """
    word_list = sentence.split()

    string_prob = 1 # setting a start probability that we can multiply by.

    for word in word_list:
        lower_word = word.lower()  # Making the words lowercase.
        if lower_word in word_prob_dict.keys():  # if the word is present in the dictionary
            string_prob *= word_prob_dict[lower_word]  # Multiply the value of the word by the string probability
        else:
            string_prob *= 0.00009

    return string_prob


# Question 5
def classify(review_string, positive_dict, negative_dict):
    """
    This function returns positive or negative for a review depending on if the probability of positive is higher than
    the probability for negative.
    :param review_string: (str) a sentence representing a review
    :param positive_dict: (dict) a dictionary of positive word probabilities
    :param negative_dict: (dict) a dictionary of negative word probabilities.
    :return: (str) Positive or negative
    """
    positive_probability = get_probability(positive_dict, review_string) # getting the probability of the string being
    # positive by calling a previous function
    negative_probability = get_probability(negative_dict, review_string)

    if positive_probability >= negative_probability:
        return "positive"
    else:
        return "negative"


# To test the function use:
# neg_model = train_model("simple.negative")
# pos_model = train_model("simple.positive")
# classify("I hated that movie", pos_model, neg_model)
# 'negative'
# classify("I loved that movie", pos_model, neg_model)
# 'positive'


# Question 6
def sentiment_analyzer(pos_file, neg_file):
    """
    This function trains a positive and a negative model using the files in the parameters, and then repeatedly
    asks the user to enter a sentence, to which the function outputs whether the sentence is positive or negative.
    :param pos_file: (file) positive example file
    :param neg_file: (file) negative example file
    :return: (str) positive or negative
    """
    pos_model = train_model(pos_file)  # training the positive file
    neg_model = train_model(neg_file)

    user_sentence = input("Enter a sentence:")  # prompting the user
    while user_sentence != "":
        print(classify(user_sentence, pos_model, neg_model))  # calling the classify function

        user_sentence = input("Enter a sentence:")


# _______________________________________
# Evaluation

# Question 7
def line_count(filename):
    """
    This function is a helper function that counts the lines in a file.
    :param filename: (file) any file
    :return: (int) line count
    """
    file = open(filename, "r")

    line_counter = 0

    for line in file:
        line_counter += 1
    file.close()

    return line_counter


def get_accuracy(pos_test_file, neg_test_file, pos_train_file, neg_train_file):
    """
    This function is working to classify just how accurate our model is by calculating the proportion of classifications
    outputted correctly.
    :param pos_test_file: (file) positive test file
    :param neg_test_file: (file) negative test file
    :param pos_train_file: (file) positive training file
    :param neg_train_file: (file) negative training file
    :return: (float) the accuracy of positive, negative, and total accuracy.
    """
    pos_train_model = train_model(pos_train_file)  # training the model on the training files.
    neg_train_model = train_model(neg_train_file)

    pos_file = open(pos_test_file, "r")  # opening the positive file
    positive_counter = 0  # setting a counter

    for line in pos_file:
        pos_neg = classify(line, pos_train_model, neg_train_model)  # pos_neg stands for what the answer to classify is
        if pos_neg == "positive":  # counting each time the model guesses positive
            positive_counter += 1

    pos_file.close()

    positive_accuracy = positive_counter / line_count(pos_test_file)  # dividing the amount of time the model said that
    # the review was positive by the amount of lines in the file, all of which are positive

    # repeating the same steps with the negative model.
    neg_file = open(neg_test_file, "r")
    negative_counter = 0

    for line in neg_file:
        pos_neg2 = classify(line, pos_train_model, neg_train_model)
        if pos_neg2 == "negative":
            negative_counter += 1
    neg_file.close()

    total_lines = (line_count(pos_test_file) + line_count(neg_test_file))

    print("Positive accuracy: " + str(positive_counter / line_count(pos_test_file)))
    print("Negative accuracy: " + str(negative_counter/ line_count(neg_test_file)))
    print("Total accuracy: " + str((positive_counter + negative_counter) / total_lines))


# Question 8
"""
Positive accuracy: 0.960431654676259
Negative accuracy: 0.7043795620437956
Total accuracy: 0.9098124098124099

The positive accuracy was 96%, the negative accuracy was 70%, and the total accuracy was 70%. This data shows that the 
model is very good at predicting what sentences are positive but not so well at predicting which are negative.
I was surprise to see that the positive data model was 96% accurate, with the overall total accuracy being 90%. 
I expected the numbers to be way lower. It's amazing just how much the computer can learn with just one line of code.

Some examples of when the model would make mistakes and guess incorrectly would be in the case where the sentence 
includes some kind of negative phrase, that is conveying positivity. For instance, the model guessed word for sentences
like "why do I like this", saying that it was a negative instead of a positive review. The model would also get confused
on statements like this, "I like this so much that I hate it", making it a negative review instead of a positive one. 
Also would guess incorrectly for a phrase like, "I love hating this movie." with the model thinking this to be a 
positive review, when in fact it is negative.

For the sentence, "Why do I hate this". I ran each individual word through the sentiment analyzer function and saw what
the function returned (positive or negative) for each word. In this case, "Why" returned negative,"do" returned
negative "I" returned positive, "like" returned positive, and "this" returned negative. With the ratio of positive 
to negative being 2/3. Since Negative made up the majority of the sentence, when I ran the entire sentence through it
returned negative. The amount of negative words to positive words doesn't have much of an impact on why the function
ultimately comes back negative. The fact is that the words that were negative outweighs the words that are positive,
is why the sentence ultimately came back negative.I went through this exact process for my other 2 sentences.

"""