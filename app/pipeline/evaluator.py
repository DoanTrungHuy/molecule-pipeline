from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, QED

class Evaluator:
    def evaluate(self, smiles):
        mol = Chem.MolFromSmiles(smiles)
        
        if not mol:
            return None

        return {
            "mw": Descriptors.MolWt(mol),
            "logp": Crippen.MolLogP(mol),
            "hbd": Descriptors.NumHDonors(mol),
            "hba": Descriptors.NumHAcceptors(mol),
            "tpsa": Descriptors.TPSA(mol),
            "rotb": Descriptors.NumRotatableBonds(mol),
            "qed": QED.qed(mol)
        }
