import sys
from train import inference, model_
import tensorlayer as tl

"""
Trained with 50 epochs and a batch of 32
"""

# When file is ran
if __name__ == "__main__":
    # Trying to load model to get response
    try:
        load_weights = tl.files.load_npz(name='model.npz')
        tl.files.assign_weights(load_weights, model_)
    except Exception as e:
        print(e)
        print('AI not connected')
    
    # Creating while loop
    while True:
        text = input("> ")
        if text == 'exit':
            break
        
        top_n = 1
        for i in range(top_n):
            sentence = inference(text, top_n)
            print(" >", ' '.join(sentence))