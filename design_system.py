"""
design_system.py — AgroYield Design System
Mini design system berbasis CSS custom properties + Python component functions.
Konsep mirip CVA (Class Variance Authority) tapi untuk Streamlit.
"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════════════════

TOKENS = {
    "color": {
        "primary-950": "#0A1F14",
        "primary-900": "#1C3D2E",
        "primary-800": "#2D6A4F",
        "primary-700": "#3A7D54",
        "primary-600": "#52B788",
        "primary-200": "#C8DECE",
        "primary-100": "#EEF5EC",
        "primary-50": "#F4F6F3",
        "neutral-900": "#1A202C",
        "neutral-700": "#2D3748",
        "neutral-500": "#718096",
        "neutral-400": "#A0AEC0",
        "neutral-200": "#E2E8E0",
        "neutral-100": "#F7FAFC",
        "neutral-50": "#FFFFFF",
        "success-bg": "#D1F0DC",
        "success-text": "#1A6B3C",
        "warning-bg": "#FEF3C7",
        "warning-text": "#92600A",
        "danger-bg": "#FEE2E2",
        "danger-text": "#991B1B",
        "info-bg": "#DBEAFE",
        "info-text": "#1E40AF",
    },
    "font": {
        "family": "'Inter', 'Segoe UI', system-ui, sans-serif",
        "size-xs": "0.65rem",
        "size-sm": "0.78rem",
        "size-base": "0.9rem",
        "size-md": "1rem",
        "size-lg": "1.2rem",
        "size-xl": "1.7rem",
        "size-2xl": "2.2rem",
        "weight-bold": "700",
        "weight-black": "800",
    },
    "radius": {
        "sm": "6px",
        "md": "10px",
        "lg": "14px",
        "full": "9999px",
    },
}

C = TOKENS["color"]
F = TOKENS["font"]
R = TOKENS["radius"]


# ══════════════════════════════════════════════════════════════════════════════
# 2. CSS INJECTION
# ══════════════════════════════════════════════════════════════════════════════

def inject_css() -> str:
    return f"""
<style>
:root {{
    --c-primary-950: {C['primary-950']};
    --c-primary-900: {C['primary-900']};
    --c-primary-800: {C['primary-800']};
    --c-primary-700: {C['primary-700']};
    --c-primary-600: {C['primary-600']};
    --c-primary-200: {C['primary-200']};
    --c-primary-100: {C['primary-100']};
    --c-primary-50: {C['primary-50']};
    --c-neutral-900: {C['neutral-900']};
    --c-neutral-700: {C['neutral-700']};
    --c-neutral-500: {C['neutral-500']};
    --c-neutral-400: {C['neutral-400']};
    --c-neutral-200: {C['neutral-200']};
    --c-neutral-100: {C['neutral-100']};
    --c-neutral-50: {C['neutral-50']};
    --c-success-bg: {C['success-bg']};
    --c-success-text: {C['success-text']};
    --c-warning-bg: {C['warning-bg']};
    --c-warning-text: {C['warning-text']};
    --c-danger-bg: {C['danger-bg']};
    --c-danger-text: {C['danger-text']};
    --c-info-bg: {C['info-bg']};
    --c-info-text: {C['info-text']};
    --f-family: {F['family']};
    --f-xs: {F['size-xs']};
    --f-sm: {F['size-sm']};
    --f-base: {F['size-base']};
    --f-md: {F['size-md']};
    --f-lg: {F['size-lg']};
    --f-xl: {F['size-xl']};
    --f-2xl: {F['size-2xl']};
    --r-sm: {R['sm']};
    --r-md: {R['md']};
    --r-lg: {R['lg']};
    --r-full: {R['full']};
}}

/* ── Base ── */
html, body, [class*="css"] {{ font-family: var(--f-family); }}
.stApp {{ background: var(--c-primary-50); }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--c-primary-50); }}
::-webkit-scrollbar-thumb {{ background: var(--c-primary-200); border-radius: var(--r-full); }}
::-webkit-scrollbar-thumb:hover {{ background: var(--c-primary-600); }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: var(--c-neutral-50);
    border-right: 1px solid var(--c-neutral-200);
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 1.5rem; }}

/* ── Input Widgets ── */
.stSelectbox label, .stSlider label, .stNumberInput label {{
    font-size: var(--f-xs) !important;
    font-weight: {F['weight-bold']} !important;
    color: var(--c-neutral-700) !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.stSelectbox > div > div {{
    border: 1.5px solid var(--c-primary-200) !important;
    border-radius: var(--r-sm) !important;
    background: var(--c-neutral-100) !important;
}}
.stNumberInput > div > div > input {{
    border: 1.5px solid var(--c-primary-200) !important;
    border-radius: var(--r-sm) !important;
    background: var(--c-neutral-100) !important;
}}
.stSlider > div > div > div > div {{
    background: var(--c-primary-800) !important;
}}

/* ── Button ── */
.stButton > button {{
    background: var(--c-primary-800) !important;
    color: var(--c-neutral-50) !important;
    border: none !important;
    border-radius: var(--r-md) !important;
    padding: 0.6rem 1.4rem !important;
    font-size: var(--f-base) !important;
    font-weight: {F['weight-bold']} !important;
    width: 100% !important;
    letter-spacing: 0.02em;
    transition: background 0.18s ease, transform 0.1s ease !important;
}}
.stButton > button:hover {{ background: var(--c-primary-900) !important; }}
.stButton > button:active {{ transform: scale(0.98) !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: transparent;
    border-bottom: 2px solid var(--c-primary-200);
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: var(--r-sm) var(--r-sm) 0 0;
    border: none;
    padding: 8px 18px;
    font-size: var(--f-sm);
    font-weight: {F['weight-bold']};
    color: var(--c-neutral-500);
    transition: color 0.15s;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: var(--c-primary-800);
}}
.stTabs [aria-selected="true"] {{
    background: var(--c-neutral-50) !important;
    color: var(--c-primary-900) !important;
    border-bottom: 3px solid var(--c-primary-800) !important;
}}

/* ── Metric ── */
[data-testid="metric-container"] {{
    background: var(--c-neutral-50);
    border: 1px solid var(--c-primary-200);
    border-radius: var(--r-md);
    padding: 0.8rem 1rem;
}}
[data-testid="metric-container"] label {{
    color: var(--c-neutral-500) !important;
    font-size: var(--f-xs) !important;
    font-weight: {F['weight-bold']} !important;
    text-transform: uppercase;
}}
[data-testid="metric-container"] .value {{
    color: var(--c-primary-900) !important;
}}

/* ── Info / Warning / Error ── */
.stInfo, .stWarning, .stError {{
    border-radius: var(--r-md) !important;
    border-left: 4px solid !important;
}}
.stInfo {{ border-left-color: var(--c-primary-700) !important; }}
.stWarning {{ border-left-color: #D97706 !important; }}
.stError {{ border-left-color: #DC2626 !important; }}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid var(--c-primary-200);
    border-radius: var(--r-md);
    overflow: hidden;
}}
[data-testid="stDataFrame"] thead th {{
    background: var(--c-primary-100) !important;
    color: var(--c-primary-900) !important;
    font-weight: {F['weight-bold']} !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    font-weight: {F['weight-bold']} !important;
    color: var(--c-primary-900) !important;
}}
.streamlit-expanderHeader:hover {{
    color: var(--c-primary-800) !important;
}}

/* ══ COMPONENTS ══ */

.ds-hero {{
    background: var(--c-primary-900);
    border-radius: var(--r-lg);
    padding: 1.4rem 2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.1rem;
}}
.ds-hero__icon {{ font-size: 2.4rem; line-height: 1; }}
.ds-hero__title {{
    font-size: var(--f-xl);
    font-weight: {F['weight-black']};
    color: var(--c-neutral-50);
    margin: 0;
    letter-spacing: -0.5px;
}}
.ds-hero__sub {{ font-size: var(--f-sm); color: var(--c-primary-600); margin: 3px 0 0; }}

.ds-card {{
    background: var(--c-neutral-50);
    border: 1px solid var(--c-primary-200);
    border-radius: var(--r-md);
    padding: 1.1rem 1.3rem;
    transition: box-shadow 0.2s ease;
}}
.ds-card:hover {{
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

.ds-card--stat {{ text-align: center; padding: 1.2rem 1rem; }}
.ds-card--stat .ds-card__label {{
    font-size: var(--f-xs);
    font-weight: {F['weight-bold']};
    color: var(--c-neutral-500);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.45rem;
}}
.ds-card--stat .ds-card__value {{
    font-size: var(--f-2xl);
    font-weight: {F['weight-black']};
    color: var(--c-primary-900);
    line-height: 1;
}}
.ds-card--stat .ds-card__unit {{
    font-size: var(--f-xs);
    color: var(--c-neutral-400);
    margin-top: 4px;
}}

.ds-card--mini {{ padding: 0.9rem 1.1rem; }}
.ds-card--mini .ds-card__label {{
    font-size: var(--f-xs);
    font-weight: {F['weight-bold']};
    color: var(--c-neutral-400);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.ds-card--mini .ds-card__value {{
    font-size: 1.4rem;
    font-weight: {F['weight-black']};
    color: var(--c-primary-900);
    margin-top: 2px;
}}

.ds-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: var(--r-full);
    font-size: var(--f-sm);
    font-weight: {F['weight-bold']};
    line-height: 1.4;
}}
.ds-badge--success {{ background: var(--c-success-bg); color: var(--c-success-text); }}
.ds-badge--warning {{ background: var(--c-warning-bg); color: var(--c-warning-text); }}
.ds-badge--danger {{ background: var(--c-danger-bg); color: var(--c-danger-text); }}
.ds-badge--info {{ background: var(--c-info-bg); color: var(--c-info-text); }}
.ds-badge--neutral {{ background: var(--c-neutral-200); color: var(--c-neutral-700); }}
.ds-badge--lg {{ font-size: var(--f-base); padding: 6px 16px; }}

.ds-alert {{
    border-radius: 0 var(--r-md) var(--r-md) 0;
    padding: 0.85rem 1.1rem;
    margin-top: 0.9rem;
    font-size: var(--f-base);
    border-left: 4px solid;
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
}}
.ds-alert--success {{ background: var(--c-primary-100); border-color: var(--c-primary-700); color: #2D5040; }}
.ds-alert--warning {{ background: var(--c-warning-bg); border-color: #D97706; color: var(--c-warning-text); }}
.ds-alert--danger {{ background: var(--c-danger-bg); border-color: #DC2626; color: var(--c-danger-text); }}
.ds-alert--info {{ background: var(--c-info-bg); border-color: #2563EB; color: var(--c-info-text); }}

.ds-section-title {{
    font-size: var(--f-md);
    font-weight: {F['weight-bold']};
    color: var(--c-primary-900);
    margin: 1.3rem 0 0.7rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--c-primary-200);
}}

.ds-divider {{ border: none; border-top: 1px solid var(--c-neutral-200); margin: 0.9rem 0; }}

.ds-label {{
    font-size: var(--f-xs);
    font-weight: {F['weight-bold']};
    color: var(--c-neutral-400);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0.9rem 0 0.35rem;
    display: block;
}}
</style>
"""


# ══════════════════════════════════════════════════════════════════════════════
# 3. COMPONENT FUNCTIONS (mirip CVA — base + variant)
# ══════════════════════════════════════════════════════════════════════════════

def hero(title: str, subtitle: str, icon: str = "🌾") -> str:
    return f"""
    <div class="ds-hero">
        <div class="ds-hero__icon">{icon}</div>
        <div>
            <div class="ds-hero__title">{title}</div>
            <div class="ds-hero__sub">{subtitle}</div>
        </div>
    </div>"""


def card_stat(label: str, value: str, unit: str = "") -> str:
    return f"""
    <div class="ds-card ds-card--stat">
        <div class="ds-card__label">{label}</div>
        <div class="ds-card__value">{value}</div>
        <div class="ds-card__unit">{unit}</div>
    </div>"""


def card_stat_badge(label: str, badge_html: str) -> str:
    return f"""
    <div class="ds-card ds-card--stat">
        <div class="ds-card__label">{label}</div>
        <div style="margin-top:0.55rem">{badge_html}</div>
    </div>"""


def card_mini(label: str, value: str) -> str:
    return f"""
    <div class="ds-card ds-card--mini">
        <div class="ds-card__label">{label}</div>
        <div class="ds-card__value">{value}</div>
    </div>"""


def badge(
    text: str,
    variant: str = "neutral",  # success | warning | danger | info | neutral
    size: str = "base",  # base | lg
    icon: str = "",
) -> str:
    size_cls = "ds-badge--lg" if size == "lg" else ""
    icon_html = f'<span aria-hidden="true">{icon}</span>' if icon else ""
    return f'<span class="ds-badge ds-badge--{variant} {size_cls}">{icon_html}{text}</span>'


def alert(
    message: str,
    variant: str = "success",  # success | warning | danger | info
    icon: str = "💡",
    bold_prefix: str = "Rekomendasi:",
) -> str:
    return f"""
    <div class="ds-alert ds-alert--{variant}">
        <span>{icon}</span>
        <span><b>{bold_prefix}</b> {message}</span>
    </div>"""


def section_title(text: str) -> str:
    return f'<div class="ds-section-title">{text}</div>'


def divider() -> str:
    return '<hr class="ds-divider">'


def label(text: str) -> str:
    return f'<span class="ds-label">{text}</span>'


# ── Namespace shorthand ───────────────────────────────────────────────────────
class ds:
    """
    Pakai di app.py:
        from design_system import ds, inject_css
        st.markdown(ds.hero("AgroYield", "Subtitle"), unsafe_allow_html=True)
        st.markdown(ds.badge("Tinggi", variant="success", size="lg"), unsafe_allow_html=True)
        st.markdown(ds.alert("Kondisi baik."), unsafe_allow_html=True)
    """
    hero = staticmethod(hero)
    card_stat = staticmethod(card_stat)
    card_stat_badge = staticmethod(card_stat_badge)
    card_mini = staticmethod(card_mini)
    badge = staticmethod(badge)
    alert = staticmethod(alert)
    section_title = staticmethod(section_title)
    divider = staticmethod(divider)
    label = staticmethod(label)
    inject_css = staticmethod(inject_css)
    tokens = TOKENS