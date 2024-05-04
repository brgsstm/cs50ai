from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A cannot be both a knight and a knave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    # if A is a knight, the sentence would be true
    Implication(AKnight, And(AKnight, AKnave)),

    # if A is a knave the sentence would be false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # for A and B, they cannot be both a knight and a knave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # if A is a knight, the sentence would be true
    # so both would be knaves
    Implication(AKnight, And(AKnave, BKnave)),

    # if A is a knave, the sentence would be false
    # so both would not be knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # for A and B, they cannot be both a knight and a knave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # if A is a knight, both the same kind
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # if A is a knave, both not the same kind
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # if B is a knight, both are different kinds
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # if B is a knave, both are not different kinds
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A B and C cannot be both a knight and a knave, they are on or the other
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # If B is a knight, his sentences would be true #
    # B says "A said 'I am a knave'." would be true
    Implication(BKnight, And(
        # A could be a knight or a knave
        Implication(AKnight, AKnave),
        # else not
        Implication(AKnave, Not(AKnave)),
    )),
    # B says "C is a knave." would be true
    Implication(BKnight, CKnave),

    # If B is a knave, his sentences would be false #
    # B says "A said 'I am a knave'." would be false
    Implication(BKnave, And(
        # A could be a knight or a knave
        Implication(AKnight, AKnight),
        # else not
        Implication(AKnave, Not(AKnight))
    )),
    # B says "C is a knave." would be false
    Implication(BKnave, Not(CKnave)),

    # If C is a knight, A is a knight:
    Implication(CKnight, AKnight),
    # If C is a knave, A is not a knight:
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
