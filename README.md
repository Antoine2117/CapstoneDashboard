# Phi LinkedIn Intelligence — Dashboard

Interactive Streamlit dashboard for the AUB MSBA capstone *"From Reach to Conversion: A LinkedIn Analytics Framework for Phi Management Group."*

Five department pages — Leadership, Business Development, Marketing, Analytics, Account Management — each wired to the real underlying data from the capstone.

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

The app opens at `http://localhost:8501`.

---

## Deploy to Streamlit Cloud (free, public URL)

### One-time setup

1. **Create a GitHub repository** and push this entire `dashboard/` folder to it. The folder structure must be:

   ```
   dashboard/
   ├── Home.py
   ├── requirements.txt
   ├── README.md
   ├── .streamlit/
   │   └── config.toml
   ├── pages/
   │   ├── 1_📈_Leadership.py
   │   ├── 2_📞_Business_Development.py
   │   ├── 3_✍️_Marketing.py
   │   ├── 4_📊_Analytics.py
   │   └── 5_🏢_Account_Management.py
   ├── data/   ← all CSVs
   └── utils.py
   ```

2. **Go to** [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.

3. **Click "New app"** and connect to your repo.

4. **App settings:**
   - Repository: `your-username/your-repo-name`
   - Branch: `main`
   - Main file path: `Home.py`
   - App URL: pick something like `phi-linkedin-intelligence`

5. **Click "Deploy"**. First boot takes 2–3 minutes while Streamlit Cloud installs dependencies. Subsequent loads are instant.

You'll get a public URL like `https://phi-linkedin-intelligence.streamlit.app`.

### Update flow

Push to GitHub → Streamlit Cloud redeploys automatically within seconds.

---

## Adding password protection later

The dashboard ships **public** by default. To switch to password-protected:

1. In **Streamlit Cloud → your app → Settings → Secrets**, add:

   ```toml
   DASHBOARD_PASSWORD = "your-chosen-password"
   ```

2. In `utils.py`, find the `password_gate()` function and change `ENABLED = False` to `ENABLED = True`.

3. Push the change. The app will now show a password prompt on the home page and every department page.

4. Share the password with the people who should have access.

---

## What's in each page

| Page | Audience | Contents |
|------|----------|----------|
| **Home** | All | Hero, 4 headline numbers, 7-act narrative, navigation |
| **📈 Leadership** | Phi leadership | KPI strip, 17,311 → 36 funnel, 12-month projection, 3 recommendations |
| **📞 Business Development** | BD team | 1,003 warm leads (filterable by role/seniority/min reactions), priority intersection |
| **✍️ Marketing** | Content team | Interactive lift roadmap (slider), 8-point checklist, content-family playbook, 90-day calendar |
| **📊 Analytics** | Analysts | Variance decomposition, 30-path multiverse (interactive hover), audience overlap, models inventory |
| **🏢 Account Management** | Account managers | 21 buying-committee accounts (filterable + drill-down), sector breakdowns |

---

## Editing the data

To refresh the dashboard with new scrape data, replace the CSVs in `data/` with new versions following the same schemas. Cached values reload automatically on next visit.

Schema reference (key files):

- `phi_warm_leads_external.csv` — 1,003 rows · `reactor_id, n_reactions, name, position, role, seniority, inferred_company, linkedinUrl`
- `phi_buying_committees_classified.csv` — 13 rows · `inferred_company, n_unique_employees, n_total_reactions, avg_reactions_per_employee, confidence_tier, matched_client, matched_sector, account_type`
- `audience_overlap_full.csv` — 3,718 rows · `reactor_id, ..., reactions_mark, reactions_micheline, reactions_phi_page, total_reactions, segment`
- `multiverse_results.csv` — 30 rows · `metric, outlier_drop_pct, baseline, compared_to, ratio, gap_holds`

---

## Credits

**Antoine Saade** · AUB MSBA Capstone · Spring 2026
Suliman S. Olayan School of Business, American University of Beirut
Company representative: **Celine Ghantous**, Senior Manager, Phi Management Group

Built on Streamlit, Plotly, pandas. Theme: navy `#1F4E79`, amber `#C08552`, paper `#FAF7F2`.
