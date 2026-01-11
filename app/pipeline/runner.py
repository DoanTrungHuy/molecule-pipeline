from app.pipeline.planner import Planner
from app.pipeline.generator import Generator
from app.pipeline.evaluator import Evaluator
from app.pipeline.screener import Screener
from app.pipeline.ranker import Ranker
from app.run_store import run_store

class PipelineRunner:
    def run(self, config, run_id=None):
        try:
            planner = Planner()

            plan = planner.plan(
                filters=config["filters"],
                seeds=config["seeds"],
                num_candidates=config["num_candidates"],
                rounds=config.get("rounds"),
                top_k=config.get("top_k")
            )

            generator = Generator()
            evaluator = Evaluator()
            screener = Screener()
            ranker = Ranker()

            seeds = plan["seeds"]
            dummy_seeds = seeds.copy()
            final_results = []

            rounds = plan["rounds"]
            top_k = plan["top_k"]

            for r in range(rounds):
                candidates = generator.generate(dummy_seeds, plan["num_candidates"])

                evaluated = []
                for smi in candidates:
                    props = evaluator.evaluate(smi)
                    if not props:
                        continue
                    evaluated.append((smi, props))

                passed = []
                for smi, props in evaluated:
                    ok, violations = screener.screen(props, plan["filters"])
                    if ok:
                        score = ranker.score(props, violations)
                        passed.append({"smiles": smi, "score": score, "violations": violations, "properties": props})

                # print(dummy_seeds)
                if len(passed) == 0:
                    break

                passed.sort(key=lambda x: x["score"], reverse=True)
                top_smiles = passed[:top_k]
                dummy_seeds = [entry["smiles"] for entry in top_smiles]
                final_results = top_smiles

            return final_results
                
        except Exception as e:
            if run_id:
                run_store.fail(run_id, str(e))
            raise e