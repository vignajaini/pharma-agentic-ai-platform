def compute_innovation_score(profile):
    score = 0

    market = profile.get("market", {})
    ms = market.get("market_size", 0)

    if ms > 1_000_000_000:
        score += 30
    elif ms > 100_000_000:
        score += 20
    else:
        score += 10

    trials = profile.get("trials", [])
    score += min(len(trials) * 5, 25)

    patents = profile.get("patents", [])
    expired = sum(1 for p in patents if p.get("status") == "expired")
    score += min(expired * 5, 20)

    papers = profile.get("web", {}).get("top_papers", [])
    score += min(len(papers) * 5, 15)

    return min(score, 100)
