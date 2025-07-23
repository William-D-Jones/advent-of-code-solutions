import sys
from collections import defaultdict

def is_order(dict_rules, l_pages):
    dict_before = {l_pages[i]: l_pages[0:i] for i in range(len(l_pages))}
    order_result = True
    for page in dict_before.keys():
        if any(test in dict_rules[page] for test in dict_before[page]):
            order_result = False
            break
    return order_result

def fix_order(dict_rules, l_pages):
    new_page_set = [l_pages[0]]
    for i in range(1, len(l_pages)):
        page = l_pages[i]
        for j in range(len(new_page_set)):
            if new_page_set[j] in dict_rules[page]:
                new_page_set = new_page_set[0:j] + [page] + new_page_set[j:]
                break
        if len(new_page_set) <= i:
            new_page_set.append(page)
    return new_page_set

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
rules = True
Rules = []
Pages = []
for x in X:
    if x != '':
        if rules:
            Rules.append(list(map(int, x.split('|'))))
        else:
            Pages.append(list(map(int, x.split(','))))
    else:
        rules = False
dict_rules = defaultdict(list)
for rule in Rules:
    dict_rules[rule[0]].append(rule[1])

ans1 = 0
ans2 = 0
for page_set in Pages:
    if is_order(dict_rules, page_set):
        ans1 += page_set[(len(page_set) - 1) // 2]
    else:
        new_page_set = fix_order(dict_rules, page_set)
        ans2 += new_page_set[(len(new_page_set) - 1) // 2]
print(ans1)
print(ans2)

