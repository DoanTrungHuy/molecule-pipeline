class Planner:
    def plan(self, objective, filters, seeds, num_candidates, rounds, top_k):
        return {
            "num_candidates": num_candidates,
            "objective": objective,
            "filters": filters,
            "seeds": seeds,
            "rounds": rounds,
            "top_k": top_k
        }
