def disjunction(operands, is_exclusive):
    return True in operands if is_exclusive else any(operands)


print(disjunction([False, True, True, True], True))
