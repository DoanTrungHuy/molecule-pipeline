import random

class Generator:
    def generate(self, seeds, n):
        results = []

        for seed in seeds:
            results.append(seed.replace("C", "CC", 1))
            results.append(seed.replace("Cl", "F"))
            results.append(seed + "C")
            results.append(seed.replace("F", "Cl"))

        random.shuffle(results)
        return list(set(results))[:n]
