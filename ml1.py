
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
    S = ['0'] * n
    G = [['?'] * n]

    for row in data:
        x, label = row[:-1], row[-1]

        if label == "Yes":
            G = [g for g in G if all(
                g[i] == '?' or g[i] == x[i]
                for i in range(n)
            )]

            for i in range(n):
                if S[i] == '0':
                    S[i] = x[i]
                elif S[i] != x[i]:
                    S[i] = '?'

        else:
            new_G = []
            for g in G:
                if all(g[i] == '?' or g[i] == x[i]
                       for i in range(n)):
                    for i in range(n):
                        if S[i] != '0' and S[i] != '?' and S[i] != x[i]:
                            h = g.copy()
                            h[i] = S[i]
                            new_G.append(h)
                else:
                    new_G.append(g)

            G = new_G

    return S, G



print("Find-S Hypothesis:", find_s(data))

S, G = candidate_elimination(data)

print("\nCandidate Elimination Results:")
print("Specific Hypothesis S:", S)
print("General Hypotheses G:")
for g in G:
    print(g)
