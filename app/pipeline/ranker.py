class Ranker:
    def score(self, props, violations):
        return props["qed"] - 0.1 * violations
