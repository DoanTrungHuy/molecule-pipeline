class Screener:
    def screen(self, props, filters):
        filters = self._ensure_dict(filters)

        max_viol = filters["max_violations"]
        violations = 0

        for key, thr in filters.items():
            if key == "max_violations":
                continue

            if key not in props:
                continue

            val = props[key]
            
            if val <= thr:
                violations += 1

        return violations <= max_viol, violations
