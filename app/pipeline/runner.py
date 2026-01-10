from app.pipeline.planner import Planner
from app.pipeline.generator import Generator
from app.pipeline.evaluator import Evaluator
from app.pipeline.screener import Screener
from app.pipeline.ranker import Ranker
from app.run_store import run_store

class PipelineRunner:
    def run(self, config, run_id=None):
        planner = Planner()

        plan = planner.plan(
            config["objective"],
            config["filters"],
            config["seeds"],
            config["num_candidates"],
            config.get("rounds"),
            config.get("top_k")
        )

        generator = Generator()
        evaluator = Evaluator()
        screener = Screener()
        ranker = Ranker()

        seeds = plan["seeds"]
        final_results = []

        rounds = plan["rounds"]
        top_k = plan["top_k"]

        for r in range(rounds):
            candidates = generator.generate(seeds, plan["num_candidates"])

            evaluated = []
            invalid = 0
            for smi in candidates:
                props = evaluator.evaluate(smi)
                if not props:
                    invalid += 1
                    continue
                evaluated.append((smi, props))

            passed = []
            failed = 0
            for smi, props in evaluated:
                ok, violations = screener.screen(props, plan["filters"])
                if ok:
                    score = ranker.score(props, violations)
                    passed.append({"smiles": smi, "score": score, "violations": violations, "properties": props})
                else:
                    failed += 1

            passed.sort(key=lambda x: x["score"], reverse=True)
            sel = passed[:top_k]

            seeds = [x["smiles"] for x in sel]

            final_results = sel

            if not seeds:
                break

        return final_results
