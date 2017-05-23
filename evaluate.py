from __future__ import print_function
import sys
sys.path.insert(0, 'src')
import scipy.misc
from argparse import ArgumentParser
from collections import defaultdict
import time
import json
import subprocess
import helper


"""
Trump Twitter LSTM

"""

import tensorflow as tf
import numpy

def trainModel():
    """
    From make-tweet.py
    """
    _, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess()
    seq_length, load_dir = helper.load_params()
    print('Done')


    def get_tensors(loaded_graph):
        """
        Get input, initial state, final state, and probabilities tensor from <loaded_graph>
        """
        InputTensor = loaded_graph.get_tensor_by_name("input:0")
        InitialStateTensor = loaded_graph.get_tensor_by_name("initial_state:0")
        FinalStateTensor = loaded_graph.get_tensor_by_name("final_state:0")
        ProbsTensor = loaded_graph.get_tensor_by_name("probs:0")

        return InputTensor, InitialStateTensor, FinalStateTensor, ProbsTensor


    def pick_word(probabilities, int_to_vocab):
        """
        Pick the next word in the generated text
        """
        # TODO: Implement Function
        #one_hot_encoded = np.argmax(probabilities, axis=0)
        one_hot_encoded = np.random.choice(len(int_to_vocab),p=probabilities)
        next_word = int_to_vocab[one_hot_encoded]

        return next_word


    # ## Generate TV Script
    # This will generate the TV script for you.  Set `gen_length` to the length of TV script you want to generate.
    gen_length = 30 # length of a tweet
    #prime_word = '@'
    choice = np.random.choice(len(int_to_vocab))
    prime_word = int_to_vocab[choice]
    prime_word

    loaded_graph = tf.Graph()
    with tf.Session(graph=loaded_graph) as sess:
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # Get Tensors from loaded model
        input_text, initial_state, final_state, probs = get_tensors(loaded_graph)

        # Sentences generation setup
        gen_sentences = [prime_word ]# + ':']
        prev_state = sess.run(initial_state, {input_text: np.array([[1]])})

        # Generate sentences
        for n in range(gen_length):
            # Dynamic Input
            dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
            dyn_seq_length = len(dyn_input[0])

            # Get Prediction
            probabilities, prev_state = sess.run(
                [probs, final_state],
                {input_text: dyn_input, initial_state: prev_state})

            pred_word = pick_word(probabilities[dyn_seq_length-1], int_to_vocab)

            gen_sentences.append(pred_word)

        # Remove tokens
        tweet = ' '.join(gen_sentences)
        for key, token in token_dict.items():
            ending = ' ' if key in ['\n', '(', '"'] else ''
            tweet = tweet.replace(' ' + token.lower(), key)
        tweet = tweet.replace('\n ', '\n')
        tweet = tweet.replace('( ', '(')
        tweet = tweet.replace('\\', '')
        tweet = tweet.replace('\/', '')
        tweet = tweet.replace('\"', '')
        tweet = tweet.replace('  ', ' ')

    return tweet


    # plt.plot(test_X, test_Y, 'bo', label='Testing data')
    # plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
    # plt.legend()
    # plt.show()
def main():
    tweet_text = trainModel()
    text_file = open("/output/console_evalute_py.txt", "w")
    text_file.write("tweet_text)
    text_file.close()

if __name__ == '__main__':
    main()
