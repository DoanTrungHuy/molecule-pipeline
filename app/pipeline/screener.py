class Screener:
    def screen(self, props, filters):
        max_viol = filters["max_violations"]
        violations = 0

        for key, thr in filters.items():
            if key == "max_violations":
                continue

            if key not in props:
                continue

            val = props[key]

            if val > thr:
                violations += 1

            # print(f"Screening {key}: value={val}, threshold={thr}, violations={violations}")

        return violations <= max_viol, violations
