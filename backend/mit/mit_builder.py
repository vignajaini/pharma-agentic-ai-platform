from .innovation_score import compute_innovation_score

class MITBuilder:
    def build(self, molecule, market, trade, patents, trials, web, internal):
        profile = {
            "molecule": molecule,
            "market": market,
            "trade": trade,
            "patents": patents,
            "trials": trials,
            "web": web,
            "internal": internal,
            "highlights": []
        }

        if market:
            profile["highlights"].append(f"Market size: {market.get('market_size')}")

        if patents:
            profile["highlights"].append(f"{len(patents)} patent documents identified")

        if trials:
            profile["highlights"].append(f"{len(trials)} clinical trials found")

        profile["innovation_score"] = compute_innovation_score(profile)
        return profile
