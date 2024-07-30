from typing import Literal
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

Person = Literal["A", "B", "C"]
Role = Literal["Knight", "Knave"]

people: list[Person] = ["A", "B", "C"]
roles: list[Role] = ["Knight", "Knave"]

def create_person_is_role_symbol(person: Person, role: Role):
    return Symbol(person + " is a " + role)

def add_general_facts(knowledge: And, available_people: list[Person]):
    """
    Adds general logical facts about people and roles

    Args:
        available_people: The people to consider when adding facts, so we dont add redundant facts for irrelevant people for the puzzle and reduce computation required
    """
    for person in available_people:
        personIsKnight = create_person_is_role_symbol(person, "Knight")
        personIsKnave = create_person_is_role_symbol(person, "Knave")
        # people can be either role
        knowledge.add(Or(personIsKnight, personIsKnave))
        # people cannot be both roles
        knowledge.add(Not(And(personIsKnight, personIsKnave)))

    knight_symbols = [create_person_is_role_symbol(person, "Knight") for person in available_people]
    knave_symbols = [create_person_is_role_symbol(person, "Knave") for person in available_people]

    # if all are one role then none are the other role, and vice versa
    knowledge.add(Biconditional(And(*knave_symbols), And(*map(lambda s: Not(s), knight_symbols))))
    knowledge.add(Biconditional(And(*knight_symbols), And(*map(lambda s: Not(s), knave_symbols))))

    # if some are one role then some are the other role, and vice versa
    knowledge.add(Biconditional(Or(*knight_symbols), Or(*knave_symbols)))

def add_claim_by_person(
    knowledge: And,
    claim: And | Or | Implication | Not | Symbol,
    person: Person
):
    """
    Args:
        claim: Logical representation of a claim made by the person which may or may not be true
        person: Person who made the claim
    """
    personIsKnight = create_person_is_role_symbol(person, "Knight")
    personIsKnave = create_person_is_role_symbol(person, "Knave")
    # If person is telling the truth then they are a knight
    knowledge.add(Implication(claim, personIsKnight))
    # If person is lying then they are a knave
    knowledge.add(Implication(Not(claim), personIsKnave))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And()
add_general_facts(knowledge0, available_people=["A"])
add_claim_by_person(
    knowledge=knowledge0,
    person='A',
    claim=And(AKnight, AKnave),  # "I am both a knight and a knave."
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And()
add_general_facts(knowledge1, ["A", "B"])
add_claim_by_person(
    knowledge=knowledge1,
    person='A',
    claim=And(AKnave, BKnave),  # "We are both knaves."
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And()
add_general_facts(knowledge2, ["A", "B"])
a_b_are_same_kind_claim = Or(
    And(AKnave, BKnave),
    And(AKnight, BKnight)
)
add_claim_by_person(
    knowledge=knowledge2,
    person='A',
    claim=a_b_are_same_kind_claim,  # "We are the same kind."
)
add_claim_by_person(
    knowledge=knowledge2,
    person='B',
    claim=Not(a_b_are_same_kind_claim),  # "We are of different kinds."
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And()
add_general_facts(knowledge3, ["A", "B", "C"])
add_claim_by_person(
    knowledge=knowledge3,
    person='A',
    claim=Or(AKnight, AKnave),  # "I am a knight." or "I am a knave."
)
# NOTE: assuming B's claim of "A said 'I am a knave'." is a trick as we cant represent what people "say" using the given symbols, just what roles they have
add_claim_by_person(
    knowledge=knowledge3,
    person='B',
    claim=CKnave,  # "C is a knave."
)
add_claim_by_person(
    knowledge=knowledge3,
    person='C',
    claim=AKnight,  # "A is a knight."
)

def main():
    puzzles = [
        ("Puzzle 0", knowledge0, ["A"]),
        ("Puzzle 1", knowledge1, ["A", "B"]),
        ("Puzzle 2", knowledge2, ["A", "B"]),
        ("Puzzle 3", knowledge3, ["A", "B", "C"])
    ]
    for puzzle, knowledge, relevant_people in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for person in relevant_people:
                for role in roles:
                    symbol = create_person_is_role_symbol(person, role)
                    if model_check(knowledge, symbol):
                        print(f"    {symbol}")

if __name__ == "__main__":
    main()

