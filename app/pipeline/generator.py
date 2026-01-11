import random

class Generator:
    def generate(self, seeds, n):
        generated_smiles = set(seeds)

        if len(generated_smiles) >= n:
            return list(generated_smiles)[:n]

        candidate_pool = list(seeds)
        atoms_to_add = ['C', 'O', 'N', 'S']
        max_attempts = n * 10
        attempts = 0

        while len(generated_smiles) < n and attempts < max_attempts:
            attempts += 1
            if not candidate_pool:
                break

            smiles = random.choice(candidate_pool)
            num_operations = random.randint(1, 4)
            
            for _ in range(num_operations):
                letter_indices = [i for i, char in enumerate(smiles) if char.isalpha()]
                if not letter_indices:
                    continue

                op = random.randint(0, 1)
                pos = random.choice(letter_indices)
                
                if op == 0 and len(smiles) > 1:
                    smiles = smiles[:pos] + smiles[pos+1:]
                elif op == 1:
                    atom = random.choice(atoms_to_add)
                    smiles = smiles[:pos] + atom + smiles[pos:]

            if smiles and smiles not in generated_smiles:
                generated_smiles.add(smiles)

        return list(generated_smiles)[:n]
