# 🏏 IPL Auction Team Selector

A Python-based IPL auction simulator that picks the **optimal 11-player squad** from a player pool using a hybrid **Greedy + 0/1 Knapsack (Dynamic Programming)** algorithm — while respecting real IPL constraints.

---

## 📋 Features

- ✅ Budget-aware selection (supports decimal budgets like `90.5 Cr`)
- ✅ Exactly 11 players selected
- ✅ Maximum 4 foreign players enforced
- ✅ Mandatory role composition guaranteed
- ✅ Optimises for highest total team rating within constraints

---

## 🧠 Algorithm

Selection happens in two phases:

### Phase 1 — Greedy (Mandatory Roles)
Fills the required role slots first using a **rating/cost ratio** greedy heuristic:

| Role           | Minimum Required |
|----------------|-----------------|
| Batsman        | 3               |
| Wicket Keeper  | 1               |
| All-Rounder    | 2               |
| Bowler         | 4               |

> `WK-Batsman` counts toward both Batsman and Wicket Keeper quotas.

### Phase 2 — Dynamic Programming (Remaining Slots)
Fills leftover slots using a **3D 0/1 Knapsack**:

```
dp[i][w][f] = max rating achievable using:
  - first i players considered
  - budget w remaining
  - f foreign slots remaining
```

The DP maximises total rating while respecting both the budget and foreign player cap simultaneously.

---

## 🚀 Getting Started

### Requirements

- Python 3.7+
- No external dependencies

### Run

```bash
python ipl_team_selector.py
```

```
Enter auction budget (e.g. 90 or 90.5): 95

🏏 SELECTED TEAM
---------------------------------------------
Virat Kohli        Batsman         Rs.15Cr
Jasprit Bumrah     Bowler          Rs.14Cr
...

SUMMARY
---------------------------------------------
Players Selected : 11
Total Rating    : 975
Total Spent     : Rs. 93 Cr
Foreign Players : 2 / 4
```

---

## 👥 Player Pool

| Name             | Role           | Cost (Cr) | Rating | Country     |
|------------------|----------------|-----------|--------|-------------|
| Virat Kohli      | Batsman        | 15        | 95     | India       |
| Rohit Sharma     | Batsman        | 14        | 92     | India       |
| David Warner     | Batsman        | 12        | 88     | Australia   |
| Babar Azam       | Batsman        | 13        | 90     | Pakistan    |
| KL Rahul         | WK-Batsman     | 11        | 83     | India       |
| Ben Stokes       | All-Rounder    | 14        | 93     | England     |
| Hardik Pandya    | All-Rounder    | 13        | 88     | India       |
| Ravindra Jadeja  | All-Rounder    | 12        | 89     | India       |
| MS Dhoni         | Wicket Keeper  | 12        | 91     | India       |
| Jos Buttler      | Wicket Keeper  | 13        | 90     | England     |
| Jasprit Bumrah   | Bowler         | 14        | 95     | India       |
| Pat Cummins      | Bowler         | 13        | 92     | Australia   |
| Mitchell Starc   | Bowler         | 11        | 88     | Australia   |
| Kagiso Rabada    | Bowler         | 10        | 87     | S. Africa   |
| Trent Boult      | Bowler         | 8         | 83     | New Zealand |

---

## ⚙️ Configuration

You can customise the selector by modifying parameters in `select_team()`:

| Parameter     | Default | Description                        |
|---------------|---------|------------------------------------|
| `budget`      | Input   | Total auction budget in Crores      |
| `max_players` | `11`    | Maximum squad size                  |
| `max_foreign` | `4`     | Maximum foreign players allowed     |

To add players, extend the list in `get_player_pool()`:

```python
{"name": "Player Name", "cost": 10, "rating": 85, "role": "Bowler", "country": "India"}
```

**Valid roles:** `Batsman`, `WK-Batsman`, `All-Rounder`, `Wicket Keeper`, `Bowler`

---

## 🐛 Bugs Fixed

Three bugs were identified and fixed from the original implementation:

| # | Location | Bug | Fix |
|---|----------|-----|-----|
| 1 | Backtrack init | `f = foreign_count` indexed wrong DP cell | Changed to `f = max_foreign - foreign_count` |
| 2 | Backtrack loop | `slots_left` computed but never enforced — could select >11 players | Added `slots_filled` counter with early break |
| 3 | Backtrack guard | `f < 0` guard never triggered correctly | Changed to `w < 0` to catch budget underflow |

---

## 📁 Project Structure

```
IPL-Auction-Team-Selector/
│
├── src.py   # Main script
└── README.md              # This file
```

---

## 📄 License

MIT — free to use and modify.
