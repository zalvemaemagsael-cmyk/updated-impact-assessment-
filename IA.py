import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Impact Assessment – DOST SETUP 4.0 iFund",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .block-container { padding: 1.2rem 1rem 3rem 1rem; max-width: 780px; margin: auto; }

  .page-title { font-size: 18px; font-weight: 700; color: #1a1a1a; margin-bottom: 1px; }
  .page-sub   { font-size: 12px; color: #888; margin-bottom: 14px; }

  .period-badge {
    display: inline-block;
    background: #dbeafe; color: #1d4ed8;
    font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    float: right; margin-top: 2px;
  }

  /* Metric cards row */
  .metrics-row { display: flex; gap: 10px; margin: 18px 0 20px 0; }
  .metric-card {
    flex: 1; background: #f9fafb; border-radius: 10px;
    padding: 12px 14px; border: 1px solid #e5e7eb;
  }
  .metric-label { font-size: 11px; color: #9ca3af; font-weight: 500; margin-bottom: 4px; }
  .metric-value { font-size: 26px; font-weight: 700; line-height: 1.1; }
  .metric-sub   { font-size: 11px; color: #9ca3af; margin-top: 2px; }
  .mv-default { color: #1a1a1a; }
  .mv-green   { color: #16a34a; }
  .mv-orange  { color: #d97706; }
  .mv-red     { color: #dc2626; }

  /* Section label */
  .section-label {
    font-size: 11px; font-weight: 700; color: #6b7280;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin: 20px 0 10px 0;
  }

  /* Output cards grid */
  .output-grid { display: flex; gap: 12px; margin-bottom: 12px; }
  .output-card {
    flex: 1; border-radius: 10px; padding: 14px 16px;
    border: 1.5px solid #e5e7eb; background: #fff;
    min-width: 0;
  }
  .output-card.red-border   { border-color: #fca5a5; }
  .output-card.green-border { border-color: #86efac; }
  .output-card.orange-border{ border-color: #fcd34d; }

  .card-type  { font-size: 10px; font-weight: 700; color: #9ca3af; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 5px; }
  .card-title { font-size: 13px; font-weight: 700; color: #111; margin-bottom: 10px; line-height: 1.3; }

  .trow { display: flex; justify-content: space-between; font-size: 12px; color: #374151; margin-bottom: 2px; }
  .trow-val { font-weight: 600; }

  .progress-track { background: #e5e7eb; border-radius: 4px; height: 5px; margin: 8px 0; overflow: hidden; }
  .progress-fill-green  { background: #22c55e; height: 5px; border-radius: 4px; }
  .progress-fill-red    { background: #ef4444; height: 5px; border-radius: 4px; }
  .progress-fill-orange { background: #f59e0b; height: 5px; border-radius: 4px; }

  .verdict-row { display: flex; justify-content: space-between; align-items: center; margin: 8px 0 6px 0; }

  .badge-accomplished    { background: #dcfce7; color: #15803d; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
  .badge-partial         { background: #fef9c3; color: #a16207; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
  .badge-not-accomplished{ background: #fee2e2; color: #b91c1c; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }

  .pct-label { font-size: 11px; color: #9ca3af; }

  .card-note { font-size: 11px; color: #6b7280; margin-top: 8px; line-height: 1.4; }

  /* Non-quant card extras */
  .nq-actual-label { font-size: 10px; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: .05em; margin: 8px 0 3px 0; }
  .nq-actual-text  { font-size: 12px; color: #374151; line-height: 1.4; margin-bottom: 10px; }
  .verdict-label-inline { font-size: 11px; color: #6b7280; font-weight: 500; }

  /* Overall verdict row */
  .overall-row {
    display: flex; justify-content: space-between; align-items: center;
    border: 1.5px solid #e5e7eb; border-radius: 10px;
    padding: 12px 16px; margin-top: 20px; background: #f9fafb;
  }
  .overall-label { font-size: 13px; font-weight: 600; color: #374151; }
  .overall-badge-green { color: #16a34a; font-size: 13px; font-weight: 600; }
  .overall-badge-orange { color: #d97706; font-size: 13px; font-weight: 600; }
  .overall-badge-red { color: #dc2626; font-size: 13px; font-weight: 600; }

  /* Objectives card */
  .objectives-card {
    background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 6px;
  }
  .obj-eyebrow {
    font-size: 10px; font-weight: 700; color: #9ca3af;
    text-transform: uppercase; letter-spacing: .05em; margin-bottom: 4px;
  }
  .obj-general-text { font-size: 13px; color: #111; line-height: 1.45; margin-bottom: 14px; }
  .obj-item { margin-bottom: 12px; }
  .obj-item:last-child { margin-bottom: 0; }
  .obj-item-text { font-size: 12.5px; color: #374151; line-height: 1.4; margin-bottom: 5px; }
  .obj-item-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }
  .obj-pct-label { font-size: 11px; color: #9ca3af; }

  /* Progress Check */
  .pc-toggle-wrap { margin: 4px 0 14px 0; }
  .pc-metrics-row { display: flex; gap: 10px; margin-bottom: 14px; }
  .pc-metric-card {
    flex: 1; background: #f9fafb; border-radius: 10px;
    padding: 12px 14px; border: 1px solid #e5e7eb;
  }
  .pc-metric-label { font-size: 11px; color: #9ca3af; font-weight: 500; margin-bottom: 4px; }
  .pc-metric-value { font-size: 22px; font-weight: 700; line-height: 1.1; color: #1a1a1a; }
  .pc-metric-sub-up   { font-size: 11px; color: #16a34a; margin-top: 3px; font-weight: 600; }
  .pc-metric-sub-down { font-size: 11px; color: #dc2626; margin-top: 3px; font-weight: 600; }
  .pc-metric-sub-flat { font-size: 11px; color: #9ca3af; margin-top: 3px; font-weight: 600; }

  .pc-table-card {
    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 12px;
  }
  .pc-table-title { font-size: 13px; font-weight: 700; color: #111; margin-bottom: 8px; }
  .pc-table-head { display: flex; justify-content: space-between; font-size: 10.5px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: .04em; padding-bottom: 4px; border-bottom: 1px solid #f1f1f1; margin-bottom: 4px; }
  .pc-table-row  { display: flex; justify-content: space-between; font-size: 12.5px; color: #374151; padding: 5px 0; border-bottom: 1px solid #f6f6f6; }
  .pc-table-row:last-child { border-bottom: none; font-weight: 700; color: #111; }
  .pc-col-metric { flex: 1.4; }
  .pc-col { flex: 1; text-align: right; }
  .pc-chg-up   { color: #16a34a; font-weight: 600; }
  .pc-chg-down { color: #dc2626; font-weight: 600; }
  .pc-chg-flat { color: #9ca3af; font-weight: 600; }
  .pc-dash { color: #c1c5cb; }

  /* hide streamlit default header decoration */
  div[data-testid="stDecoration"] { display: none; }
  header { visibility: hidden; }
  .stSelectbox > label { display: none !important; }
  div[data-baseweb="select"] { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA SOURCE: SUPABASE ───────────────────────────────────────────────────
#
# Expected schema (create these tables in your Supabase project):
#
#   msmes
#     id            uuid / bigint  primary key
#     name          text
#     address       text
#
#   semesters
#     id            uuid / bigint  primary key
#     msme_id       fk -> msmes.id
#     name          text   e.g. "S2 2024 (Jul – Dec 2024)"
#     period_badge  text   e.g. "S2 2024 · July – December 2024"
#     overall       text   "accomplished" | "partially accomplished" | "not accomplished"
#     sort_order    int    (optional, controls ordering of semesters)
#
#   quantifiable_outputs
#     id            uuid / bigint  primary key
#     semester_id   fk -> semesters.id
#     title         text
#     target_val    text (nullable)
#     target_unit   text (nullable)
#     actual_val    text (nullable)
#     actual_unit   text (nullable)
#     verdict       text
#     pct           int
#     note          text
#     sort_order    int (optional)
#
#   non_quantifiable_outputs
#     id              uuid / bigint  primary key
#     semester_id     fk -> semesters.id
#     title           text
#     actual          text
#     default_verdict text
#     sort_order      int (optional)
#
#   msme_objectives
#     id            uuid / bigint  primary key
#     msme_id       fk -> msmes.id
#     general       text            e.g. "This project aims to improve..."
#
#   msme_specific_objectives
#     id                uuid / bigint  primary key
#     msme_id           fk -> msmes.id
#     text              text
#     linked_quant      int[]   (indices into that MSME's quantifiable_outputs, per semester, used to compute progress)
#     linked_nonquant   int[]   (indices into that MSME's non_quantifiable_outputs)
#     sort_order        int (optional)
#
#   msme_baseline (Pre-PIS / baseline figures, one row per MSME)
#     id                uuid / bigint  primary key
#     msme_id           fk -> msmes.id
#     land              numeric
#     building          numeric
#     equipment         numeric
#     working_capital   numeric
#     employment_direct   int
#     employment_indirect int
#     sales_local       numeric
#     sales_export      numeric
#
#   msme_progress_current (Current figures, one row per MSME per semester)
#     id                uuid / bigint  primary key
#     msme_id           fk -> msmes.id
#     semester_id       fk -> semesters.id
#     land              numeric (nullable)
#     building          numeric (nullable)
#     equipment         numeric (nullable)
#     working_capital   numeric (nullable)
#     employment_direct   int (nullable)
#     employment_indirect int (nullable)
#     sales_local       numeric (nullable)
#     sales_export      numeric (nullable)
#
# Credentials are read from Streamlit secrets (.streamlit/secrets.toml):
#
#   SUPABASE_URL = "https://xxxxx.supabase.co"
#   SUPABASE_KEY = "your-service-role-or-anon-key"
#
# Install the client with: pip install supabase

import os
from supabase import create_client, Client
from demo_data import DEMO_REPORTS


@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
    if not url or not key:
        raise RuntimeError(
            "Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY "
            "in .streamlit/secrets.toml or as environment variables."
        )
    return create_client(url, key)


@st.cache_data(ttl=300, show_spinner="Loading data from Supabase…")
def load_reports():
    """Fetch MSMEs, semesters, and outputs from Supabase and reshape them
    into the same nested structure the UI expects (mirrors the old REPORTS dict)."""
    supabase = get_supabase_client()

    msmes_resp = supabase.table("msmes").select("*").execute()
    semesters_resp = (
        supabase.table("semesters")
        .select("*")
        .order("sort_order", desc=False, nullsfirst=False)
        .execute()
    )
    quant_resp = (
        supabase.table("quantifiable_outputs")
        .select("*")
        .order("sort_order", desc=False, nullsfirst=False)
        .execute()
    )
    nonquant_resp = (
        supabase.table("non_quantifiable_outputs")
        .select("*")
        .order("sort_order", desc=False, nullsfirst=False)
        .execute()
    )

    msmes = msmes_resp.data or []
    semesters = semesters_resp.data or []
    quant_rows = quant_resp.data or []
    nonquant_rows = nonquant_resp.data or []

    # Objectives / progress-check tables are optional — if they don't exist
    # yet in Supabase, these sections simply won't be shown.
    def safe_select(table_name, order_col=None):
        try:
            q = supabase.table(table_name).select("*")
            if order_col:
                q = q.order(order_col, desc=False, nullsfirst=False)
            return q.execute().data or []
        except Exception:
            return []

    objectives_rows = safe_select("msme_objectives")
    specific_obj_rows = safe_select("msme_specific_objectives", "sort_order")
    baseline_rows = safe_select("msme_baseline")
    progress_current_rows = safe_select("msme_progress_current")

    objectives_by_msme = {row["msme_id"]: row.get("general", "") for row in objectives_rows}

    specific_by_msme = {}
    for row in specific_obj_rows:
        specific_by_msme.setdefault(row["msme_id"], []).append({
            "text": row.get("text", ""),
            "linked_quant": row.get("linked_quant") or [],
            "linked_nonquant": row.get("linked_nonquant") or [],
        })

    baseline_by_msme = {}
    for row in baseline_rows:
        baseline_by_msme[row["msme_id"]] = {
            "assets": {
                "land": row.get("land"), "building": row.get("building"),
                "equipment": row.get("equipment"), "working_capital": row.get("working_capital"),
            },
            "employment": {"direct": row.get("employment_direct"), "indirect": row.get("employment_indirect")},
            "gross_sales": {"local": row.get("sales_local"), "export": row.get("sales_export")},
        }

    current_by_msme_sem = {}
    sem_id_to_name = {sem["id"]: sem["name"] for sem in semesters}
    for row in progress_current_rows:
        sem_name = sem_id_to_name.get(row.get("semester_id"))
        if not sem_name:
            continue
        has_assets = any(row.get(k) is not None for k in ("land", "building", "equipment", "working_capital"))
        has_emp = any(row.get(k) is not None for k in ("employment_direct", "employment_indirect"))
        has_sales = any(row.get(k) is not None for k in ("sales_local", "sales_export"))
        current_by_msme_sem.setdefault(row["msme_id"], {})[sem_name] = {
            "assets": ({"land": row.get("land"), "building": row.get("building"),
                        "equipment": row.get("equipment"), "working_capital": row.get("working_capital")}
                       if has_assets else None),
            "employment": ({"direct": row.get("employment_direct"), "indirect": row.get("employment_indirect")}
                           if has_emp else None),
            "gross_sales": ({"local": row.get("sales_local"), "export": row.get("sales_export")}
                            if has_sales else None),
        }

    # group outputs by semester_id
    quant_by_sem = {}
    for row in quant_rows:
        quant_by_sem.setdefault(row["semester_id"], []).append({
            "title": row.get("title"),
            "target_val": row.get("target_val"),
            "target_unit": row.get("target_unit"),
            "actual_val": row.get("actual_val"),
            "actual_unit": row.get("actual_unit"),
            "verdict": row.get("verdict", "not accomplished"),
            "pct": row.get("pct", 0),
            "note": row.get("note", ""),
        })

    nonquant_by_sem = {}
    for row in nonquant_rows:
        nonquant_by_sem.setdefault(row["semester_id"], []).append({
            "title": row.get("title"),
            "actual": row.get("actual", ""),
            "default_verdict": row.get("default_verdict", "not accomplished"),
        })

    # group semesters by msme_id
    semesters_by_msme = {}
    for sem in semesters:
        semesters_by_msme.setdefault(sem["msme_id"], []).append(sem)

    reports = {}
    for msme in msmes:
        msme_id = msme["id"]
        sem_dict = {}
        for sem in semesters_by_msme.get(msme_id, []):
            sem_id = sem["id"]
            sem_dict[sem["name"]] = {
                "period_badge": sem.get("period_badge", sem["name"]),
                "quantifiable": quant_by_sem.get(sem_id, []),
                "non_quantifiable": nonquant_by_sem.get(sem_id, []),
                "overall": sem.get("overall", "not accomplished"),
            }
        general_obj = objectives_by_msme.get(msme_id)
        specific_objs = specific_by_msme.get(msme_id)
        objectives = None
        if general_obj or specific_objs:
            objectives = {"general": general_obj or "", "specific": specific_objs or []}

        msme_baseline = baseline_by_msme.get(msme_id)
        progress_check = None
        if msme_baseline:
            progress_check = {
                "baseline": msme_baseline,
                "current": current_by_msme_sem.get(msme_id, {}),
            }

        reports[msme["name"]] = {
            "address": msme.get("address", ""),
            "semesters": sem_dict,
            "objectives": objectives,
            "progress_check": progress_check,
        }

    return reports


def supabase_configured() -> bool:
    url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL", ""))
    key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY", ""))
    return bool(url and key)


using_demo_data = False

if supabase_configured():
    try:
        REPORTS = load_reports()
        if not REPORTS:
            st.warning("Connected to Supabase, but no MSME records were found yet. Showing demo data instead.")
            REPORTS = DEMO_REPORTS
            using_demo_data = True
    except Exception as e:
        st.warning(
            "⚠️ Could not load data from Supabase, so demo data is being shown instead.\n\n"
            f"Details: {e}"
        )
        REPORTS = DEMO_REPORTS
        using_demo_data = True
else:
    REPORTS = DEMO_REPORTS
    using_demo_data = True

if using_demo_data:
    st.info("📦 Running on **demo data** — add SUPABASE_URL / SUPABASE_KEY to `.streamlit/secrets.toml` to use live data.")

VERDICT_OPTIONS = ["Accomplished", "Partially accomplished", "Not accomplished"]

def verdict_badge(v):
    v_lower = v.lower()
    if v_lower == "accomplished":
        return "accomplished", "✓ Accomplished", "#badge-accomplished"
    elif v_lower == "partially accomplished":
        return "partial", "— Partially accomplished", "#badge-partial"
    else:
        return "not", "✕ Not accomplished", "#badge-not-accomplished"

def badge_html(v):
    _, label, _ = verdict_badge(v)
    v_lower = v.lower()
    if v_lower == "accomplished":
        cls = "badge-accomplished"
    elif v_lower == "partially accomplished":
        cls = "badge-partial"
    else:
        cls = "badge-not-accomplished"
    return f'<span class="{cls}">{label}</span>'

def progress_color(v):
    v_lower = v.lower()
    if v_lower == "accomplished":
        return "progress-fill-green"
    elif v_lower == "partially accomplished":
        return "progress-fill-orange"
    return "progress-fill-red"

def card_border(v):
    v_lower = v.lower()
    if v_lower == "accomplished":
        return "green-border"
    elif v_lower == "partially accomplished":
        return "orange-border"
    return "red-border"

def fmt_money(v):
    if v is None:
        return "—"
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "—"
    if abs(v) >= 1_000_000:
        return f"₱{v/1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"₱{v/1_000:.1f}K"
    return f"₱{v:,.0f}"

def fmt_count(v):
    if v is None:
        return "—"
    try:
        return f"{int(v):,}"
    except (TypeError, ValueError):
        return "—"

def pct_change(baseline, current):
    if baseline in (None, 0) or current is None:
        return None
    try:
        return round((float(current) - float(baseline)) / float(baseline) * 100)
    except (TypeError, ValueError, ZeroDivisionError):
        return None

def chg_html(baseline, current, is_money=True):
    pct = pct_change(baseline, current)
    if pct is None:
        return '<span class="pc-dash">—</span>'
    cls = "pc-chg-up" if pct > 0 else ("pc-chg-down" if pct < 0 else "pc-chg-flat")
    sign = "+" if pct >= 0 else ""
    return f'<span class="{cls}">{sign}{pct}%</span>'

def default_verdict_index(dv):
    dv_lower = dv.lower()
    if dv_lower == "accomplished":
        return 0
    elif dv_lower == "partially accomplished":
        return 1
    return 2

# ── UI ────────────────────────────────────────────────────────────────────────

st.markdown('<div class="page-title">Impact assessment</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">DOST SETUP 4.0 iFund Program — Region VI</div>', unsafe_allow_html=True)

msme_names = list(REPORTS.keys())
sel_msme = st.selectbox("MSME", msme_names, label_visibility="collapsed")

msme_data = REPORTS[sel_msme]
sem_names = list(msme_data["semesters"].keys())
sel_sem = st.selectbox("Semester", sem_names, label_visibility="collapsed")

sem_data = msme_data["semesters"][sel_sem]
period_badge = sem_data["period_badge"]
quant_outputs = sem_data["quantifiable"]
nonquant_outputs = sem_data["non_quantifiable"]

st.markdown(f'<div class="period-badge">{period_badge}</div>', unsafe_allow_html=True)
st.markdown("<div style='clear:both; height:4px;'></div>", unsafe_allow_html=True)

# ── Metrics ─────────────────────────────────────────────────────────────────
total_outputs = len(quant_outputs) + len(nonquant_outputs)
accomplished = sum(1 for o in quant_outputs if o["verdict"].lower() == "accomplished")
partial = sum(1 for o in quant_outputs if o["verdict"].lower() == "partially accomplished")
not_acc = sum(1 for o in quant_outputs if o["verdict"].lower() == "not accomplished")
# non-quant defaults
accomplished += sum(1 for o in nonquant_outputs if o["default_verdict"].lower() == "accomplished")
partial += sum(1 for o in nonquant_outputs if o["default_verdict"].lower() == "partially accomplished")
not_acc += sum(1 for o in nonquant_outputs if o["default_verdict"].lower() == "not accomplished")

pct_acc  = f"{round(accomplished/total_outputs*100)}% of outputs" if total_outputs else "—"
pct_part = f"{round(partial/total_outputs*100)}% of outputs" if total_outputs else "—"
pct_not  = f"{round(not_acc/total_outputs*100)}% of outputs" if total_outputs else "—"

st.markdown(f"""
<div class="metrics-row">
  <div class="metric-card">
    <div class="metric-label">Total outputs</div>
    <div class="metric-value mv-default">{total_outputs}</div>
    <div class="metric-sub">this semester</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Accomplished</div>
    <div class="metric-value mv-green">{accomplished}</div>
    <div class="metric-sub">{pct_acc}</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Partially accomplished</div>
    <div class="metric-value mv-orange">{partial}</div>
    <div class="metric-sub">{pct_part}</div>
  </div>
  <div class="metric-card">
    <div class="metric-label">Not accomplished</div>
    <div class="metric-value mv-red">{not_acc}</div>
    <div class="metric-sub">{pct_not}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Objectives ────────────────────────────────────────────────────────────────
objectives = msme_data.get("objectives")
if objectives:
    st.markdown('<div class="section-label">Project Objectives</div>', unsafe_allow_html=True)

    general_html = f"""
<div class="objectives-card">
  <div class="obj-eyebrow">General Objective</div>
  <div class="obj-general-text">{objectives.get('general', '')}</div>
"""
    st.markdown(general_html + '<div class="obj-eyebrow">Specific Objectives</div>', unsafe_allow_html=True)

    for i, obj in enumerate(objectives.get("specific", []), start=1):
        linked_pcts = []

        for qi in obj.get("linked_quant", []):
            if qi < len(quant_outputs):
                linked_pcts.append(quant_outputs[qi]["pct"])

        for ni in obj.get("linked_nonquant", []):
            if ni < len(nonquant_outputs):
                dv = nonquant_outputs[ni]["default_verdict"].lower()
                linked_pcts.append(100 if dv == "accomplished" else 50 if dv == "partially accomplished" else 0)

        if linked_pcts:
            obj_pct = round(sum(linked_pcts) / len(linked_pcts))
        else:
            obj_pct = 0

        if obj_pct >= 100:
            prog_cls, verdict_lbl = "progress-fill-green", "accomplished"
        elif obj_pct > 0:
            prog_cls, verdict_lbl = "progress-fill-orange", "partially accomplished"
        else:
            prog_cls, verdict_lbl = "progress-fill-red", "not accomplished"

        st.markdown(f"""
<div class="obj-item">
  <div class="obj-item-text">{i}. {obj['text']}</div>
  <div class="progress-track"><div class="{prog_cls}" style="width:{obj_pct}%;"></div></div>
  <div class="obj-item-footer">
    {badge_html(verdict_lbl)}
    <span class="obj-pct-label">{obj_pct}% progress</span>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Progress Check (Pre vs Post-Implementation) ──────────────────────────────
progress_check = msme_data.get("progress_check")
if progress_check:
    st.markdown('<div class="section-label">Progress Check — Pre vs Post-Implementation</div>', unsafe_allow_html=True)

    view_mode = st.radio(
        "View", ["Semestral (selected period)", "Annual (latest period)"],
        horizontal=True, label_visibility="collapsed", key=f"pc_view_{sel_msme}"
    )

    baseline = progress_check.get("baseline", {})
    current_by_sem = progress_check.get("current", {})

    if view_mode.startswith("Annual"):
        current = current_by_sem.get(sem_names[-1])
    else:
        current = current_by_sem.get(sel_sem)
    current = current or {}

    b_assets = baseline.get("assets", {})
    c_assets = current.get("assets")
    b_assets_total = sum(v for v in b_assets.values() if v is not None) if b_assets else None
    c_assets_total = sum(v for v in c_assets.values() if v is not None) if c_assets else None

    b_emp = baseline.get("employment", {})
    c_emp = current.get("employment")
    b_emp_total = sum(v for v in b_emp.values() if v is not None) if b_emp else None
    c_emp_total = sum(v for v in c_emp.values() if v is not None) if c_emp else None

    b_sales = baseline.get("gross_sales", {})
    c_sales = current.get("gross_sales")
    b_sales_total = sum(v for v in b_sales.values() if v is not None) if b_sales else None
    c_sales_total = sum(v for v in c_sales.values() if v is not None) if c_sales else None

    def sub_html(baseline_val, current_val):
        pct = pct_change(baseline_val, current_val)
        if pct is None:
            return '<div class="pc-metric-sub-flat">not yet reported</div>'
        cls = "pc-metric-sub-up" if pct > 0 else ("pc-metric-sub-down" if pct < 0 else "pc-metric-sub-flat")
        sign = "+" if pct >= 0 else ""
        return f'<div class="{cls}">{sign}{pct}% vs Pre-PIS</div>'

    st.markdown(f"""
<div class="pc-metrics-row">
  <div class="pc-metric-card">
    <div class="pc-metric-label">Assets</div>
    <div class="pc-metric-value">{fmt_money(c_assets_total) if c_assets_total is not None else fmt_money(b_assets_total)}</div>
    {sub_html(b_assets_total, c_assets_total)}
  </div>
  <div class="pc-metric-card">
    <div class="pc-metric-label">Employment</div>
    <div class="pc-metric-value">{fmt_count(c_emp_total)}</div>
    {sub_html(b_emp_total, c_emp_total)}
  </div>
  <div class="pc-metric-card">
    <div class="pc-metric-label">Gross Sales</div>
    <div class="pc-metric-value">{fmt_money(c_sales_total)}</div>
    {sub_html(b_sales_total, c_sales_total)}
  </div>
</div>
""", unsafe_allow_html=True)

    # Trend: assets across all semesters vs flat Pre-PIS baseline
    trend_rows = []
    for sname in sem_names:
        sem_current = current_by_sem.get(sname) or {}
        sem_assets = sem_current.get("assets")
        sem_assets_total = sum(v for v in sem_assets.values() if v is not None) if sem_assets else None
        trend_rows.append({
            "Period": sname,
            "Current Assets": sem_assets_total if sem_assets_total is not None else None,
            "Pre-PIS Asset Baseline": b_assets_total,
        })
    trend_df = pd.DataFrame(trend_rows).set_index("Period")
    if trend_df["Current Assets"].notna().any():
        st.markdown('<div class="pc-table-title" style="margin-top:4px;">Assets Trend</div>', unsafe_allow_html=True)
        st.line_chart(trend_df, height=200)

    # Assets table
    st.markdown(f"""
<div class="pc-table-card">
  <div class="pc-table-title">Assets</div>
  <div class="pc-table-head"><span class="pc-col-metric">Metric</span><span class="pc-col">Pre-PIS</span><span class="pc-col">Current</span><span class="pc-col">Chg</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Land</span><span class="pc-col">{fmt_money(b_assets.get('land'))}</span><span class="pc-col">{fmt_money((c_assets or {}).get('land')) if c_assets else fmt_money(b_assets.get('land'))}</span><span class="pc-col">{chg_html(b_assets.get('land'), (c_assets or {}).get('land') if c_assets else b_assets.get('land'))}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Building</span><span class="pc-col">{fmt_money(b_assets.get('building'))}</span><span class="pc-col">{fmt_money((c_assets or {}).get('building')) if c_assets else fmt_money(b_assets.get('building'))}</span><span class="pc-col">{chg_html(b_assets.get('building'), (c_assets or {}).get('building') if c_assets else b_assets.get('building'))}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Equipment</span><span class="pc-col">{fmt_money(b_assets.get('equipment'))}</span><span class="pc-col">{fmt_money((c_assets or {}).get('equipment')) if c_assets else fmt_money(b_assets.get('equipment'))}</span><span class="pc-col">{chg_html(b_assets.get('equipment'), (c_assets or {}).get('equipment') if c_assets else b_assets.get('equipment'))}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Working Cap.</span><span class="pc-col">{fmt_money(b_assets.get('working_capital'))}</span><span class="pc-col">{fmt_money((c_assets or {}).get('working_capital')) if c_assets else fmt_money(b_assets.get('working_capital'))}</span><span class="pc-col">{chg_html(b_assets.get('working_capital'), (c_assets or {}).get('working_capital') if c_assets else b_assets.get('working_capital'))}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Total</span><span class="pc-col">{fmt_money(b_assets_total)}</span><span class="pc-col">{fmt_money(c_assets_total) if c_assets_total is not None else fmt_money(b_assets_total)}</span><span class="pc-col">{chg_html(b_assets_total, c_assets_total if c_assets_total is not None else b_assets_total)}</span></div>
</div>
""", unsafe_allow_html=True)

    # Employment table
    st.markdown(f"""
<div class="pc-table-card">
  <div class="pc-table-title">Employment Generated</div>
  <div class="pc-table-head"><span class="pc-col-metric">Metric</span><span class="pc-col">Pre-PIS</span><span class="pc-col">Current</span><span class="pc-col">Chg</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Direct</span><span class="pc-col">{fmt_count(b_emp.get('direct'))}</span><span class="pc-col">{fmt_count((c_emp or {}).get('direct')) if c_emp else '—'}</span><span class="pc-col">{chg_html(b_emp.get('direct'), (c_emp or {}).get('direct') if c_emp else None)}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Indirect</span><span class="pc-col">{fmt_count(b_emp.get('indirect'))}</span><span class="pc-col">{fmt_count((c_emp or {}).get('indirect')) if c_emp else '—'}</span><span class="pc-col">{chg_html(b_emp.get('indirect'), (c_emp or {}).get('indirect') if c_emp else None)}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Total</span><span class="pc-col">{fmt_count(b_emp_total)}</span><span class="pc-col">{fmt_count(c_emp_total)}</span><span class="pc-col">{chg_html(b_emp_total, c_emp_total)}</span></div>
</div>
""", unsafe_allow_html=True)

    # Gross Sales table
    st.markdown(f"""
<div class="pc-table-card">
  <div class="pc-table-title">Gross Sales</div>
  <div class="pc-table-head"><span class="pc-col-metric">Metric</span><span class="pc-col">Pre-PIS</span><span class="pc-col">Current</span><span class="pc-col">Chg</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Local</span><span class="pc-col">{fmt_money(b_sales.get('local'))}</span><span class="pc-col">{fmt_money((c_sales or {}).get('local')) if c_sales else '—'}</span><span class="pc-col">{chg_html(b_sales.get('local'), (c_sales or {}).get('local') if c_sales else None)}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Export</span><span class="pc-col">{fmt_money(b_sales.get('export'))}</span><span class="pc-col">{fmt_money((c_sales or {}).get('export')) if c_sales else '—'}</span><span class="pc-col">{chg_html(b_sales.get('export'), (c_sales or {}).get('export') if c_sales else None)}</span></div>
  <div class="pc-table-row"><span class="pc-col-metric">Total</span><span class="pc-col">{fmt_money(b_sales_total)}</span><span class="pc-col">{fmt_money(c_sales_total)}</span><span class="pc-col">{chg_html(b_sales_total, c_sales_total)}</span></div>
</div>
""", unsafe_allow_html=True)

# ── Quantifiable Outputs ─────────────────────────────────────────────────────
if quant_outputs:
    st.markdown('<div class="section-label">Quantifiable Outputs</div>', unsafe_allow_html=True)

    pairs = [quant_outputs[i:i+2] for i in range(0, len(quant_outputs), 2)]
    for pair in pairs:
        cols = st.columns(2)
        for col, item in zip(cols, pair):
            with col:
                border_cls = card_border(item["verdict"])
                prog_cls   = progress_color(item["verdict"])
                pct        = item["pct"]
                has_values = item["target_val"] is not None

                target_row = ""
                actual_row = ""
                if has_values:
                    target_row = f'<div class="trow"><span>Target</span><span class="trow-val">{item["target_val"]} {item["target_unit"]}</span></div>'
                    actual_row = f'<div class="trow"><span>Actual</span><span class="trow-val">{item["actual_val"]} {item["actual_unit"]}</span></div>'

                note_html = f'<div class="card-note">{item["note"]}</div>' if item["note"] else ""
                pct_lbl = f'{pct}% of target'

                st.markdown(f"""
<div class="output-card {border_cls}">
  <div class="card-type">Quantifiable</div>
  <div class="card-title">{item['title']}</div>
  {target_row}
  {actual_row}
  <div class="progress-track"><div class="{prog_cls}" style="width:{pct}%;"></div></div>
  <div class="verdict-row">
    {badge_html(item['verdict'])}
    <span class="pct-label">{pct_lbl}</span>
  </div>
  {note_html}
</div>
""", unsafe_allow_html=True)

        # fill empty slot if odd
        if len(pair) == 1:
            pass

# ── Non-Quantifiable Outputs ─────────────────────────────────────────────────
if nonquant_outputs:
    st.markdown('<div class="section-label">Non-Quantifiable Outputs</div>', unsafe_allow_html=True)

    nq_pairs = [nonquant_outputs[i:i+2] for i in range(0, len(nonquant_outputs), 2)]

    # Store verdicts in session state
    if "nq_verdicts" not in st.session_state:
        st.session_state["nq_verdicts"] = {}

    state_key_prefix = f"{sel_msme}_{sel_sem}"

    for pair_idx, pair in enumerate(nq_pairs):
        cols = st.columns(2)
        for col_idx, (col, item) in enumerate(zip(cols, pair)):
            with col:
                state_key = f"{state_key_prefix}_nq_{pair_idx}_{col_idx}"
                default_idx = default_verdict_index(item["default_verdict"])

                chosen = st.selectbox(
                    f"Verdict for: {item['title'][:30]}",
                    VERDICT_OPTIONS,
                    index=default_idx,
                    key=state_key,
                    label_visibility="collapsed"
                )

                border_cls = card_border(chosen)
                st.markdown(f"""
<div class="output-card {border_cls}" style="margin-top:-8px;">
  <div class="card-type">Non-Quantifiable</div>
  <div class="card-title">{item['title']}</div>
  <div class="nq-actual-label">Actual accomplishment</div>
  <div class="nq-actual-text">{item['actual']}</div>
  <div style="display:flex; align-items:center; gap:8px; margin-top:6px;">
    <span class="verdict-label-inline">Verdict (PSTO):</span>
  </div>
</div>
""", unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:4px;">{badge_html(chosen)}</div>', unsafe_allow_html=True)

# ── Overall semester verdict ─────────────────────────────────────────────────
overall = sem_data["overall"]
if overall.lower() == "accomplished":
    overall_html = '<span class="overall-badge-green">✓ Accomplished</span>'
elif overall.lower() == "partially accomplished":
    overall_html = '<span class="overall-badge-orange">— Partially accomplished</span>'
else:
    overall_html = '<span class="overall-badge-red">✕ Not accomplished</span>'

st.markdown(f"""
<div class="overall-row">
  <div style="display:flex;align-items:center;gap:8px;">
    <span style="font-size:16px;">📊</span>
    <span class="overall-label">Overall semester verdict</span>
  </div>
  {overall_html}
</div>
""", unsafe_allow_html=True)

st.markdown("<br><p style='font-size:11px;color:#ccc;text-align:center;'>DOST-VI SETUP 4.0 iFund Program · Region VI</p>", unsafe_allow_html=True)
