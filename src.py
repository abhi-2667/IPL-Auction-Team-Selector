# ================================================================
# 🏏 IPL Auction Simulator – Team Selector
# Greedy selection for mandatory roles + DP (0/1 Knapsack)
# Constraints: Budget, max players, role balance, foreign limit
# ================================================================

INDIA = "India"

def get_player_pool():
    # Static player pool (cost in Cr, rating out of 100)
    return [
        {"name":"Virat Kohli","cost":15,"rating":95,"role":"Batsman","country":"India"},
        {"name":"Rohit Sharma","cost":14,"rating":92,"role":"Batsman","country":"India"},
        {"name":"David Warner","cost":12,"rating":88,"role":"Batsman","country":"Australia"},
        {"name":"Babar Azam","cost":13,"rating":90,"role":"Batsman","country":"Pakistan"},
        {"name":"KL Rahul","cost":11,"rating":83,"role":"WK-Batsman","country":"India"},

        {"name":"Ben Stokes","cost":14,"rating":93,"role":"All-Rounder","country":"England"},
        {"name":"Hardik Pandya","cost":13,"rating":88,"role":"All-Rounder","country":"India"},
        {"name":"Ravindra Jadeja","cost":12,"rating":89,"role":"All-Rounder","country":"India"},

        {"name":"MS Dhoni","cost":12,"rating":91,"role":"Wicket Keeper","country":"India"},
        {"name":"Jos Buttler","cost":13,"rating":90,"role":"Wicket Keeper","country":"England"},

        {"name":"Jasprit Bumrah","cost":14,"rating":95,"role":"Bowler","country":"India"},
        {"name":"Pat Cummins","cost":13,"rating":92,"role":"Bowler","country":"Australia"},
        {"name":"Mitchell Starc","cost":11,"rating":88,"role":"Bowler","country":"Australia"},
        {"name":"Kagiso Rabada","cost":10,"rating":87,"role":"Bowler","country":"S. Africa"},
        {"name":"Trent Boult","cost":8,"rating":83,"role":"Bowler","country":"New Zealand"},
    ]

def is_foreign(player):
    # Foreign player check
    return player["country"] != INDIA

def select_team(players, budget, max_players=11, max_foreign=4):
    SCALE = 10                    # support decimal budgets
    budget = int(budget * SCALE)

    mandatory_roles = {
        "Batsman":3,
        "Wicket Keeper":1,
        "All-Rounder":2,
        "Bowler":4
    }

    selected = []
    foreign_count = 0
    remaining_budget = budget

    # -------- Greedy: satisfy mandatory roles --------
    for role, cnt in mandatory_roles.items():
        valid = ["Batsman","WK-Batsman"] if role == "Batsman" else [role]

        pool = sorted(
            [p for p in players if p["role"] in valid and p not in selected],
            key=lambda x: x["rating"] / x["cost"],
            reverse=True
        )

        for p in pool:
            if cnt == 0:
                break

            cost = int(p["cost"] * SCALE)

            if cost > remaining_budget:
                continue
            if is_foreign(p) and foreign_count >= max_foreign:
                continue

            selected.append(p)
            remaining_budget -= cost

            if is_foreign(p):
                foreign_count += 1

            cnt -= 1

    # -------- DP: fill remaining slots optimally --------
    remaining = [p for p in players if p not in selected]
    slots_left = max_players - len(selected)
    n = len(remaining)
    W = remaining_budget

    # dp[i][w][f] = max rating using first i players
    dp = [[[0] * (max_foreign + 1) for _ in range(W + 1)] for _ in range(n + 1)]
    choose = [[[False] * (max_foreign + 1) for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = remaining[i - 1]
        cost = int(p["cost"] * SCALE)
        rating = p["rating"]
        foreign = 1 if is_foreign(p) else 0

        for w in range(W + 1):
            for f in range(max_foreign + 1):
                dp[i][w][f] = dp[i - 1][w][f]

                if cost <= w and f >= foreign:
                    val = dp[i - 1][w - cost][f - foreign] + rating
                    if val > dp[i][w][f]:
                        dp[i][w][f] = val
                        choose[i][w][f] = True

    # Backtracking DP result
    w = W
    f = max_foreign - foreign_count
    slots_filled = 0

    for i in range(n, 0, -1):
        if slots_filled >= slots_left or w < 0:
            break

        if choose[i][w][f]:
            p = remaining[i - 1]
            selected.append(p)
            w -= int(p["cost"] * SCALE)

            if is_foreign(p):
                f -= 1

            slots_filled += 1

    total_rating = sum(p["rating"] for p in selected)
    return selected, total_rating

def main():
    players = get_player_pool()
    budget = float(input("Enter auction budget (e.g. 90 or 90.5): "))

    team, rating = select_team(players, budget)

    print("\n🏏 SELECTED TEAM")
    print("-" * 45)

    spent = 0
    foreign = 0

    for p in team:
        spent += p["cost"]
        if is_foreign(p):
            foreign += 1
        print(f"{p['name']:<18} {p['role']:<15} Rs.{p['cost']}Cr")

    print("\nSUMMARY")
    print("-" * 45)
    print("Players Selected :", len(team))
    print("Total Rating    :", rating)
    print("Total Spent     : Rs.", spent, "Cr")
    print("Foreign Players :", foreign, "/ 4")

if __name__ == "__main__":
    main()
