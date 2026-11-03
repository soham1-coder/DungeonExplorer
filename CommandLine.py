import argparse
import random

from Difficulty import Difficulties

def getDifficulty():
    parser = argparse.ArgumentParser(description="Maze description")

    parser.add_argument("--difficulty", choices=["Easy", "Normal", "Hard"], default= "Normal", help= "Choose the difficulty")

    args = parser.parse_args()

    difficulty = Difficulties[args.difficulty]
    print(f"Difficulty: {args.difficulty} ({difficulty.description()})")
    return difficulty