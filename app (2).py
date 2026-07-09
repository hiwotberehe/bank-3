import streamlit as st
import pandas as pd
from datetime import datetime
import os
from num2words import num2words
from fpdf import FPDF

st.set_page_config(page_title="Oromia Bank - Cash Withdrawal Form", page_icon="🏦", layout="centered")

# ---------- STYLING ----------
st.markdown("""
<style>
.bank-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 3px solid #000;
    padding-bottom: 10px;
    margin-bottom: 15px;
}
.bank-title {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 1px;
}
.bank-sub {
    font-size: 14px;
    color: #444;
}
.bank-name {
    font-size: 24px;
    font-weight: 800;
    color: #7a1f1f;
    text-align: right;
}
.section-box {
    border: 1px solid #999;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 14px;
    background-color: #fafafa;
}
.denom-total {
    font-weight: 700;
    font-size: 18px;
    color: #145214;
}
.ai-box {
    border: 1px dashed #6a4fd6;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 14px;
    background-color: #f5f2ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- DEFAULT / SESSION STATE ----------
DEFAULTS = {
    "branch_name": "",
    "account_type": "Saving Account (Herrega Qusannoo)",
    "other_specify": "",
    "full_name": "",
    "account_no": "",
    "amount_words": "",
    "amount_number": 0,
    "x200": 0, "x100": 0, "x50": 0, "x10": 0, "x5": 0, "x1": 0, "cents": 0.0,
    "cust1_name": "", "cust1_sign": "", "cust1_phone": "",
    "cust2_name": "", "cust2_sign": "", "cust2_phone": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def load_demo():
    """Fill the form with sample data matching the original paper form example."""
    st.session_state.update({
        "branch_name": "Gerji",
        "account_type": "Demand Account (Herrega Socho'aa)",
        "other_specify": "",
        "full_name": "Jorgu Adulu Bilisaa",
        "account_no": "1907478600007",
        "amount_words": "twenty thousand",
        "amount_number": 20000,
        "x200": 100, "x100": 0, "x50": 0, "x10": 0, "x5": 0, "x1": 0, "cents": 0.0,
        "cust1_name": "Jorgu Adulu Bilisaa", "cust1_sign": "J. Adulu", "cust1_phone": "0911234567",
        "cust2_name": "", "cust2_sign": "", "cust2_phone": "",
    })


def clear_form():
    st.session_state.update(DEFAULTS)


def ai_auto_words():
    """AI helper: convert the numeric amount into words automatically."""
    amt = int(st.session_state.get("amount_number", 0))
    if amt > 0:
        words = num2words(amt).replace("-", " ")
        st.session_state["amount_words"] = words


def ai_auto_denomination():
    """AI helper: compute the optimal (fewest-note) denomination breakdown for the amount."""
    amt = int(st.session_state.get("amount_number", 0))
    remainder_cents = round(st.session_state.get("amount_number", 0) - amt, 2)
    notes = [200, 100, 50, 10, 5, 1]
    counts = {}
    remaining = amt
    for n in notes:
        counts[n] = remaining // n
        remaining = remaining % n
    st.session_state["x200"] = int(counts[200])
    st.session_state["x100"] = int(counts[100])
    st.session_state["x50"] = int(counts[50])
    st.session_state["x10"] = int(counts[10])
    st.session_state["x5"] = int(counts[5])
    st.session_state["x1"] = int(counts[1])
    st.session_state["cents"] = float(remainder_cents)


# ---------- HEADER ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="bank-title">CASH WITHDRAWAL FORM</div>', unsafe_allow_html=True)
    st.markdown('<div class="bank-sub">Unka Baasiin Ittiin Ajajamu / ገንዘብ ወጪ ማድረጊያ ቅፅ</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="bank-name">Oromia Bank</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- DEMO CONTROLS ----------
d_col1, d_col2 = st.columns(2)
with d_col1:
    st.button("🎬 Load Demo Data", on_click=load_demo, use_container_width=True,
              help="Fills the form with a sample withdrawal so you can see how it works")
with d_col2:
    st.button("🧹 Clear Form", on_click=clear_form, use_container_width=True)

# ---------- BRANCH ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
branch_name = st.text_input("Branch / Damee (ቅርንጫፍ)", key="branch_name", placeholder="Enter branch name")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- ACCOUNT TYPE ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("**Account Type**")
account_type = st.radio(
    "Herrega Qusannoo / የሂሳብ ዓይነት",
    ["Saving Account (Herrega Qusannoo)",
     "Special Saving Account (Herrega Qusannoo Addaa)",
     "Demand Account (Herrega Socho'aa)",
     "Other (Specify)"],
    key="account_type",
)
other_specify = ""
if account_type == "Other (Specify)":
    other_specify = st.text_input("Kan Biroo / ሌላ ካልሆነ ይግለጹ (Specify)", key="other_specify")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CUSTOMER / ACCOUNT INFO ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    full_name = st.text_input("Full Name / Maqaa Guutuu (ሙሉ ስም)", key="full_name")
with c2:
    account_no = st.text_input("A/C No. / Lakk. Herrega (የሂሳብ ቁጥር)", key="account_no")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- AMOUNT ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
amount_number = st.number_input("Amount in Number / Qarshii (በቁጥር)", min_value=0, step=1, format="%d", key="amount_number")
amount_words = st.text_input("Amount in Words / Hanga Qarshii Jechaan (በፊደል)", key="amount_words")

st.markdown('<div class="ai-box">', unsafe_allow_html=True)
st.markdown("🤖 **AI Assist**")
st.button("✨ Auto-write Amount in Words", on_click=ai_auto_words,
           help="Automatically spells out the numeric amount in words")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- DENOMINATION ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("**Denomination Needed / Jijjiirraa Qarshii Barbaaddani**")

st.markdown('<div class="ai-box">', unsafe_allow_html=True)
st.markdown("🤖 **AI Assist**")
st.button("✨ Auto-calculate Denomination (fewest notes)", on_click=ai_auto_denomination,
           help="Automatically works out the optimal note breakdown for the amount entered above")
st.markdown('</div>', unsafe_allow_html=True)

d1, d2, d3, d4, d5, d6, d7 = st.columns(7)
with d1:
    x200 = st.number_input("X 200", min_value=0, step=1, key="x200")
with d2:
    x100 = st.number_input("X 100", min_value=0, step=1, key="x100")
with d3:
    x50 = st.number_input("X 50", min_value=0, step=1, key="x50")
with d4:
    x10 = st.number_input("X 10", min_value=0, step=1, key="x10")
with d5:
    x5 = st.number_input("X 5", min_value=0, step=1, key="x5")
with d6:
    x1 = st.number_input("X 1", min_value=0, step=1, key="x1")
with d7:
    cents = st.number_input("CENTS", min_value=0.0, step=0.01, format="%.2f", key="cents")

denom_total = (x200 * 200) + (x100 * 100) + (x50 * 50) + (x10 * 10) + (x5 * 5) + (x1 * 1) + cents
st.markdown(f'<p class="denom-total">Denomination Total: {denom_total:,.2f}</p>', unsafe_allow_html=True)

if amount_number > 0 and denom_total != amount_number:
    st.warning(f"⚠️ Denomination total ({denom_total:,.2f}) does not match Amount in Number ({amount_number:,}). Try the AI auto-calculate button above.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------- CUSTOMER 1 & 2 ----------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("**Customer Signatures**")
cc1, cc2 = st.columns(2)
with cc1:
    st.markdown("① Customer 1")
    cust1_name = st.text_input("Name of Customer / Maqaa Maamilaa (1)", key="cust1_name")
    cust1_sign = st.text_input("Signature / Mallattoo (1) — type name or initials", key="cust1_sign")
    cust1_phone = st.text_input("Tel/Mob / Bilbila (1)", key="cust1_phone")
with cc2:
    st.markdown("② Customer 2")
    cust2_name = st.text_input("Name of Customer / Maqaa Maamilaa (2)", key="cust2_name")
    cust2_sign = st.text_input("Signature / Mallattoo (2) — type name or initials", key="cust2_sign")
    cust2_phone = st.text_input("Tel/Mob / Bilbila (2)", key="cust2_phone")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Notice: Passbook must accompany with this form.")

st.markdown("---")


# ---------- PDF RECEIPT GENERATOR ----------
def generate_receipt_pdf(record: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Oromia Bank - Cash Withdrawal Receipt", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generated: {record['Timestamp']}", ln=True, align="C")
    pdf.ln(6)

    pdf.set_font("Helvetica", "", 11)
    rows = [
        ("Branch", record["Branch"]),
        ("Account Type", record["Account Type"]),
        ("Full Name", record["Full Name"]),
        ("Account No.", record["Account No"]),
        ("Amount in Words", record["Amount in Words"]),
        ("Amount in Number", f"{record['Amount in Number']:,}"),
        ("Denomination (200s)", record["X200"]),
        ("Denomination (100s)", record["X100"]),
        ("Denomination (50s)", record["X50"]),
        ("Denomination (10s)", record["X10"]),
        ("Denomination (5s)", record["X5"]),
        ("Denomination (1s)", record["X1"]),
        ("Cents", record["Cents"]),
        ("Denomination Total", f"{record['Denomination Total']:,.2f}"),
        ("Customer 1 Name", record["Customer1 Name"]),
        ("Customer 1 Signature", record["Customer1 Signature"]),
        ("Customer 1 Phone", record["Customer1 Phone"]),
        ("Customer 2 Name", record["Customer2 Name"]),
        ("Customer 2 Signature", record["Customer2 Signature"]),
        ("Customer 2 Phone", record["Customer2 Phone"]),
    ]
    for label, value in rows:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 8, str(label), border=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, str(value), border=1, ln=True)

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 6, "Notice: Passbook must accompany with this form.")

    return bytes(pdf.output(dest="S"))


# ---------- SUBMIT ----------
if st.button("✅ Submit Withdrawal Form", use_container_width=True):
    if not branch_name or not full_name or not account_no or amount_number <= 0:
        st.error("Please fill in Branch, Full Name, Account Number, and Amount before submitting.")
    else:
        record = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Branch": branch_name,
            "Account Type": other_specify if account_type == "Other (Specify)" else account_type,
            "Full Name": full_name,
            "Account No": account_no,
            "Amount in Words": amount_words,
            "Amount in Number": amount_number,
            "X200": x200, "X100": x100, "X50": x50, "X10": x10, "X5": x5, "X1": x1, "Cents": cents,
            "Denomination Total": denom_total,
            "Customer1 Name": cust1_name, "Customer1 Signature": cust1_sign, "Customer1 Phone": cust1_phone,
            "Customer2 Name": cust2_name, "Customer2 Signature": cust2_sign, "Customer2 Phone": cust2_phone,
        }

        file_path = "withdrawal_records.csv"
        df_new = pd.DataFrame([record])
        if os.path.exists(file_path):
            df_new.to_csv(file_path, mode="a", header=False, index=False)
        else:
            df_new.to_csv(file_path, mode="w", header=True, index=False)

        st.success("Form submitted and saved successfully!")
        st.write("### Submitted Details")
        st.table(pd.DataFrame([record]).T.rename(columns={0: "Value"}))

        # ---- Export formats ----
        exp1, exp2, exp3 = st.columns(3)
        with exp1:
            csv_bytes = pd.DataFrame([record]).to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ CSV", data=csv_bytes,
                                file_name=f"withdrawal_{account_no}.csv", mime="text/csv",
                                use_container_width=True)
        with exp2:
            pdf_bytes = generate_receipt_pdf(record)
            st.download_button("⬇️ PDF Receipt", data=pdf_bytes,
                                file_name=f"withdrawal_{account_no}.pdf", mime="application/pdf",
                                use_container_width=True)
        with exp3:
            import io
            xlsx_buf = io.BytesIO()
            with pd.ExcelWriter(xlsx_buf, engine="openpyxl") as writer:
                pd.DataFrame([record]).to_excel(writer, index=False, sheet_name="Withdrawal")
            st.download_button("⬇️ Excel", data=xlsx_buf.getvalue(),
                                file_name=f"withdrawal_{account_no}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True)

# ---------- VIEW ALL RECORDS ----------
with st.expander("📋 View All Saved Withdrawal Records"):
    if os.path.exists("withdrawal_records.csv"):
        df_all = pd.read_csv("withdrawal_records.csv")
        st.dataframe(df_all, use_container_width=True)

        e1, e2 = st.columns(2)
        with e1:
            st.download_button("⬇️ Download all as CSV", data=df_all.to_csv(index=False).encode("utf-8"),
                                file_name="all_withdrawal_records.csv", mime="text/csv",
                                use_container_width=True)
        with e2:
            import io
            xlsx_buf_all = io.BytesIO()
            with pd.ExcelWriter(xlsx_buf_all, engine="openpyxl") as writer:
                df_all.to_excel(writer, index=False, sheet_name="Records")
            st.download_button("⬇️ Download all as Excel", data=xlsx_buf_all.getvalue(),
                                file_name="all_withdrawal_records.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True)
    else:
        st.info("No records saved yet.")
