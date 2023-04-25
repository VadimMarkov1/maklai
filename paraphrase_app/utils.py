import itertools
import nltk


def find_nouns_positions(tree_string):
    """
    The function finds noun phrases consisting of multiple NP separated by tags comma or CC (conjunctive inversion),
    groups them and returns them together with their positions in the main tree
    """
    tree = nltk.tree.Tree.fromstring(tree_string)
    nouns = []
    for subtree in tree.subtrees(filter=lambda s: s.label() == "NP"):
        step = 0
        for i in range(len(subtree)):
            if i <= step != 0:
                continue
            if subtree[i].label() == "NP":
                p = i
                nouns_group = []
                nouns_positions = []
                while p + 2 <= len(subtree) and (subtree[p+1].label() == "CC" or subtree[p+1].label() == ",") \
                        and subtree[p+2].label() == "NP":
                    nouns_group.append((subtree[p+2]))
                    p += 2
                    step = p
                if nouns_group:
                    nouns_group.insert(0, subtree[i])
                    for noun in nouns_group:
                        for pos in tree.treepositions():
                            if tree[pos] == noun:
                                nouns_positions.append(pos)
                    nouns.append([nouns_group, nouns_positions])
    return nouns


def generate_nouns_permutations(tree, nouns, limit=20):
    """
    The function generates variants of permutations of corresponding noun phrases with each other
     in a number not exceeding the given limit
     """
    tree = nltk.tree.Tree.fromstring(tree)
    perms = []
    noun_positions = []
    for noun in nouns:
        noun_positions.extend(noun[1])
        perms_group = []
        for perm in itertools.permutations(noun[0]):
            perms_group.append(perm)
        perms.append(perms_group)
    perm_options = itertools.product(*perms)
    results = []
    for option in perm_options:
        variant = []
        for noun_group in option:
            for noun in noun_group:
                variant.append(noun)
        new_tree = tree.copy(deep=True)
        for noun, pos in zip(variant, noun_positions):
            copy_noun = noun.copy(deep=True)
            new_tree[pos] = copy_noun
        if new_tree.pformat(margin=999) != tree.pformat(margin=999):
            results.append({"tree": new_tree.pformat(margin=999)})
        if len(results) == limit:
            return results
    return results
