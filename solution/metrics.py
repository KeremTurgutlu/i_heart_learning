import numpy as np

def dice_score(pred, targ):
    """
    Sorensen dice score:
    https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient

    pred (np.array): prediction boolean mask
    targ (np.array): target boolean mask
    """
    pred = pred.flatten()
    targ = targ.flatten()
    return 2 * sum(pred * targ) / (sum(pred) + sum(targ))

def test_dice():
    """unit test for dice_score function"""
    preds = [

        np.array([[1, 1, 0],
                  [0, 0, 0],
                  [1, 0, 1]]),

        np.array([[1, 1, 1],
                  [1, 0, 1],
                  [0, 0, 0]])
    ]

    targs = [

        np.array([[0, 0, 1],
                  [0, 0, 0],
                  [0, 1, 0]]),

        np.array([[0, 1, 0],
                  [1, 1, 0],
                  [0, 1, 1]])
    ]

    answer = [0., 0.4]

    for pred, targ, ans in zip(preds, targs, answer):
        assert ans == dice_score(pred, targ)
    print("Test passed")