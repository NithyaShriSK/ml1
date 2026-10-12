
import pandas as pd

df = pd.read_csv("ml_exp1.csv")
data = df.astype(str).values.tolist()


def find_s(data):
    h = ['0'] * (len(data[0]) - 1)

    for row in data:
        if row[-1] == "Yes":
            for i in range(len(h)):
                if h[i] == '0':
                    h[i] = row[i]
                elif h[i] != row[i]:
                    h[i] = '?'

    return h



def candidate_elimination(data):
    n = len(data[0]) - 1
    domains = [set(row[i] for row in data) for i in range(n)]

    S = [('0',) * n]
    G = [('?',) * n]

    def covers(h, x):
        return all(h[i] == '?' or h[i] == x[i]
                   for i in range(n))

    def more_general(h1, h2):
        return all(a == '?' or a == b
                   for a, b in zip(h1, h2))

    for row in data:
        x, label = row[:-1], row[-1]

        if label == "Yes":
            G = [g for g in G if covers(g, x)]

            new_S = []
            for s in S:
                if covers(s, x):
                    new_S.append(s)
                else:
                    h = list(s)
                    for i in range(n):
                        if h[i] == '0':
                            h[i] = x[i]
                        elif h[i] != x[i]:
                            h[i] = '?'
                    new_S.append(tuple(h))

            S = new_S

        else:
            new_G = []
            for g in G:
                if covers(g, x):
                    for i in range(n):
                        if g[i] == '?':
                            for val in domains[i]:
                                if val != x[i]:
                                    h = list(g)
                                    h[i] = val
                                    h = tuple(h)

                                    if any(more_general(h, s) for s in S):
                                        new_G.append(h)
                else:
                    new_G.append(g)

            G = new_G

    return [list(s) for s in S], [list(g) for g in G]



print("Find-S Hypothesis:", find_s(data))

S, G = candidate_elimination(data)

print("\nCandidate Elimination Results:")
print("Specific Hypothesis S:", S)
print("General Hypotheses G:")
for g in G:
    print(g)
