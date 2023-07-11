from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
A_Says = And(AKnight, AKnave)
knowledge0 = And(
    # Definition of Knight and Knave
    Implication(AKnight, A_Says),
    Implication(AKnave, Not(A_Says)),
    # Rules                           
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A_Says = And(AKnave, BKnave)
knowledge1 = And(
    # Definition of Knight and Knave
    Implication(AKnight, A_Says),
    Implication(AKnave, Not(A_Says)),
    # Rules                           
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A_Says = Or(And(AKnave, BKnave), And(AKnight, BKnight))
B_Says = Or(And(AKnave, BKnight), And(AKnight, BKnave))
knowledge2 = And(
    # Definition of Knight and Knave
    Implication(AKnight, A_Says),
    Implication(AKnave, Not(A_Says)),
    Implication(BKnight, B_Says),
    Implication(BKnave, Not(B_Says)),
    # Rules                           
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_Says = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
B_Says = And(Implication(AKnave, Not(AKnight)), CKnave)
C_Says = AKnight
knowledge3 = And(
    # Definition of Knight and Knave
    Implication(AKnight, A_Says),
    Implication(AKnave, Not(A_Says)),
    Implication(BKnight, B_Says),
    Implication(BKnave, Not(B_Says)),
    Implication(CKnight, C_Says),
    Implication(CKnave, Not(C_Says)),
    # Rules                           
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
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
