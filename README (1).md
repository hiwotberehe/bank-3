# 🏦 Oromia Bank — Cash Withdrawal Form (Digitized)

A Streamlit app that digitizes the paper "Cash Withdrawal Form" into a fillable web form, with the same fields as the original — plus a demo mode, AI-assisted auto-fill, and multi-format export.

## Form fields (matching the original paper form)

- Branch / Damee
- Account type: Saving Account / Special Saving Account / Demand Account / Other (Specify)
- Full Name / Maqaa Guutuu
- A/C No. / Lakk. Herrega
- Amount in Words
- Amount in Number
- Denomination Needed: X200, X100, X50, X10, X5, X1, Cents (with auto-calculated total + mismatch warning)
- Two customer blocks: Name, Signature, Tel/Mob (matching ① and ② on the paper form)

## ✨ What's new

**🎬 Demo mode**
- "Load Demo Data" button instantly fills every field with a sample withdrawal (based on the example form) so you can see the whole flow without typing anything.
- "Clear Form" resets everything back to blank.

**🤖 AI-assisted features**
- **Auto-write Amount in Words** — type the numeric amount, click the button, and it spells the amount out in words for you (e.g. `20000` → `twenty thousand`).
- **Auto-calculate Denomination** — click the button and it works out the optimal (fewest-note) breakdown of 200/100/50/10/5/1 notes needed to make up the entered amount, and fills the denomination row automatically.
- A live mismatch warning tells you if your manual denomination entries don't add up to the stated amount.

**📄 Additional export formats**
On submit, in addition to saving the record to a running log, you can download the withdrawal as:
- **CSV** — for spreadsheets / record-keeping
- **PDF Receipt** — a formatted, printable bank-style receipt
- **Excel (.xlsx)** — a single-record spreadsheet

You can also export **all saved records** at once as CSV or Excel from the "View All Saved Withdrawal Records" section.

## Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit application |
| `requirements.txt` | Python dependencies |
| `run_on_colab.ipynb` | Notebook to launch the app from Google Colab via a public ngrok link |

## Option 1 — Run on Google Colab (no local install needed)

1. Go to [Google Colab](https://colab.research.google.com) and upload `run_on_colab.ipynb` (File → Upload notebook).
2. Get a **free** ngrok authtoken: sign up at https://dashboard.ngrok.com/get-started/your-authtoken and copy your token.
3. Run the notebook cells in order:
   - Cell 1 installs `streamlit`, `pyngrok`, and the app's dependencies.
   - Cell 2 prompts you to upload `app.py` — select it from your computer.
   - Cell 3: paste your ngrok authtoken where indicated (`NGROK_AUTH_TOKEN = "..."`).
   - Cell 4 launches the app and prints a public URL like `https://xxxx.ngrok-free.app`.
4. Click the printed URL to open your digitized form in the browser.
5. To stop the app: run `ngrok.kill()` and `process.terminate()` in a new cell.

## Option 2 — Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Option 3 — Deploy permanently (free) on Streamlit Community Cloud

1. Push `app.py` and `requirements.txt` to a GitHub repository.
2. Go to https://share.streamlit.io, sign in with GitHub, and click "New app".
3. Select your repo, branch, and `app.py` as the entry point, then deploy.
4. You'll get a permanent public link (e.g. `https://yourapp.streamlit.app`) that doesn't require Colab or ngrok each time.

## Notes

- Submitted records are stored in `withdrawal_records.csv` in the app's working directory. On Colab/ngrok this resets each session — download your records before closing.
- For a real handwritten signature pad instead of typed text, the app can be extended with `streamlit-drawable-canvas` — ask if you'd like that added.
- Bilingual (Amharic/Oromo) labels are already included alongside English on each field, matching the original paper form.
- The "AI Assist" features (amount-to-words and denomination optimizer) run locally with simple, deterministic logic — no external API key or internet connection is required for them to work.
