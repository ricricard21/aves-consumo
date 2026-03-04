import sqlite3
from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st

DB_PATH = "consumo_estandar.db"

# =========================================================
# ESTÁNDARES (Hy-Line Brown) — alimento (g/ave/día) y agua (ml/ave/día)
# =========================================================
HYLINE_BROWN_STDS = [
    {"semana": 1, "alimento_min_g": 14, "alimento_max_g": 15, "agua_min_ml": 21, "agua_max_ml": 30},
    {"semana": 2, "alimento_min_g": 17, "alimento_max_g": 21, "agua_min_ml": 26, "agua_max_ml": 42},
    {"semana": 3, "alimento_min_g": 23, "alimento_max_g": 25, "agua_min_ml": 35, "agua_max_ml": 50},
    {"semana": 4, "alimento_min_g": 27, "alimento_max_g": 29, "agua_min_ml": 41, "agua_max_ml": 58},
    {"semana": 5, "alimento_min_g": 34, "alimento_max_g": 36, "agua_min_ml": 51, "agua_max_ml": 72},
    {"semana": 6, "alimento_min_g": 38, "alimento_max_g": 40, "agua_min_ml": 57, "agua_max_ml": 80},
    {"semana": 7, "alimento_min_g": 41, "alimento_max_g": 43, "agua_min_ml": 62, "agua_max_ml": 86},
    {"semana": 8, "alimento_min_g": 45, "alimento_max_g": 47, "agua_min_ml": 68, "agua_max_ml": 94},
    {"semana": 9, "alimento_min_g": 49, "alimento_max_g": 53, "agua_min_ml": 74, "agua_max_ml": 106},
    {"semana": 10, "alimento_min_g": 52, "alimento_max_g": 56, "agua_min_ml": 78, "agua_max_ml": 112},
    {"semana": 11, "alimento_min_g": 58, "alimento_max_g": 62, "agua_min_ml": 87, "agua_max_ml": 124},
    {"semana": 12, "alimento_min_g": 62, "alimento_max_g": 66, "agua_min_ml": 93, "agua_max_ml": 132},
    {"semana": 13, "alimento_min_g": 67, "alimento_max_g": 71, "agua_min_ml": 101, "agua_max_ml": 142},
    {"semana": 14, "alimento_min_g": 70, "alimento_max_g": 74, "agua_min_ml": 105, "agua_max_ml": 148},
    {"semana": 15, "alimento_min_g": 72, "alimento_max_g": 76, "agua_min_ml": 108, "agua_max_ml": 152},
    {"semana": 16, "alimento_min_g": 75, "alimento_max_g": 79, "agua_min_ml": 113, "agua_max_ml": 158},
    {"semana": 17, "alimento_min_g": 78, "alimento_max_g": 82, "agua_min_ml": 117, "agua_max_ml": 164},
    {"semana": 18, "alimento_min_g": 82, "alimento_max_g": 88, "agua_min_ml": 123, "agua_max_ml": 176},
    {"semana": 19, "alimento_min_g": 85, "alimento_max_g": 91, "agua_min_ml": 128, "agua_max_ml": 182},
    {"semana": 20, "alimento_min_g": 91, "alimento_max_g": 97, "agua_min_ml": 137, "agua_max_ml": 194},
    {"semana": 21, "alimento_min_g": 95, "alimento_max_g": 101, "agua_min_ml": 143, "agua_max_ml": 202},
    {"semana": 22, "alimento_min_g": 99, "alimento_max_g": 105, "agua_min_ml": 149, "agua_max_ml": 210},
    {"semana": 23, "alimento_min_g": 103, "alimento_max_g": 109, "agua_min_ml": 155, "agua_max_ml": 218},
    {"semana": 24, "alimento_min_g": 105, "alimento_max_g": 111, "agua_min_ml": 158, "agua_max_ml": 222},
    {"semana": 25, "alimento_min_g": 106, "alimento_max_g": 112, "agua_min_ml": 159, "agua_max_ml": 224},
    {"semana": 26, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 27, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 28, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 29, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 30, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 31, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 32, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 33, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 34, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 35, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 36, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 37, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 38, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 39, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 40, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 41, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 42, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 43, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 44, "alimento_min_g": 108, "alimento_max_g": 114, "agua_min_ml": 162, "agua_max_ml": 228},
    {"semana": 45, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
    {"semana": 46, "alimento_min_g": 107, "alimento_max_g": 113, "agua_min_ml": 161, "agua_max_ml": 226},
]

RAZAS = {
    "Hy-Line Brown": {
        "inicio_postura_semana": 18,
        "estandares": pd.DataFrame(HYLINE_BROWN_STDS),
    }
}

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        raza TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        aves_iniciales INTEGER NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lote_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        semana INTEGER NOT NULL,
        aves_vivas INTEGER NOT NULL,
        modo TEXT NOT NULL,
        alimento_std_kg REAL NOT NULL,
        agua_std_l REAL NOT NULL,
        alimento_real_kg REAL,
        agua_real_l REAL,
        UNIQUE(lote_id, fecha),
        FOREIGN KEY(lote_id) REFERENCES lotes(id)
    )
    """)
    conn.commit()
    conn.close()

def fetch_lotes():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM lotes ORDER BY id DESC", conn)
    conn.close()
    return df

def add_lote(nombre, raza, fecha_inicio, aves_iniciales):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lotes (nombre, raza, fecha_inicio, aves_iniciales) VALUES (?, ?, ?, ?)",
        (nombre, raza, fecha_inicio, aves_iniciales)
    )
    conn.commit()
    conn.close()

def fetch_registros(lote_id: int):
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM registros WHERE lote_id = ? ORDER BY fecha ASC",
        conn,
        params=(lote_id,)
    )
    conn.close()
    return df

def upsert_registro(lote_id, fecha, semana, aves_vivas, modo, al_std_kg, ag_std_l, al_real_kg, ag_real_l):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO registros (lote_id, fecha, semana, aves_vivas, modo, alimento_std_kg, agua_std_l, alimento_real_kg, agua_real_l)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(lote_id, fecha)
        DO UPDATE SET semana=excluded.semana,
                      aves_vivas=excluded.aves_vivas,
                      modo=excluded.modo,
                      alimento_std_kg=excluded.alimento_std_kg,
                      agua_std_l=excluded.agua_std_l,
                      alimento_real_kg=excluded.alimento_real_kg,
                      agua_real_l=excluded.agua_real_l
    """, (lote_id, fecha, semana, aves_vivas, modo, al_std_kg, ag_std_l, al_real_kg, ag_real_l))
    conn.commit()
    conn.close()

def get_std_for_week(std_df: pd.DataFrame, semana: int):
    if std_df.empty:
        return None
    max_week = int(std_df["semana"].max())
    semana_use = min(max(1, int(semana)), max_week)
    row = std_df[std_df["semana"] == semana_use]
    if row.empty:
        return None
    r = row.iloc[0]
    return {
        "semana": int(r["semana"]),
        "al_min": float(r["alimento_min_g"]),
        "al_max": float(r["alimento_max_g"]),
        "ag_min": float(r["agua_min_ml"]),
        "ag_max": float(r["agua_max_ml"]),
    }

def pick_targets(std, modo: str):
    if modo == "Mínimo":
        return std["al_min"], std["ag_min"]
    if modo == "Máximo":
        return std["al_max"], std["ag_max"]
    return (std["al_min"] + std["al_max"]) / 2.0, (std["ag_min"] + std["ag_max"]) / 2.0

def calc_std_totals(aves_vivas: int, g_ave: float, ml_ave: float):
    al_kg = (g_ave * aves_vivas) / 1000.0
    ag_l = (ml_ave * aves_vivas) / 1000.0
    return al_kg, ag_l

def status_vs_range(valor: float, vmin: float, vmax: float):
    if valor < vmin:
        return "🔴 Bajo"
    if valor > vmax:
        return "🔴 Alto"
    return "🟢 OK"

def inject_css():
    st.markdown("""
    <style>
      .block-container { padding-top: 1.8rem; padding-bottom: 2.2rem; max-width: 1200px; }
      h1,h2,h3 { letter-spacing: -0.4px; }
      .muted { opacity: 0.85; }
      .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 12px 34px rgba(0,0,0,0.22);
      }
      .card:hover { border-color: rgba(255,255,255,0.16); transform: translateY(-1px); transition: 0.15s; }
      .pill {
        display:inline-block; padding: 6px 10px; border-radius: 999px;
        background: rgba(240,160,58,0.20); border: 1px solid rgba(240,160,58,0.35);
        font-weight: 800; font-size: 0.9rem;
      }
      div.stButton>button {
        border-radius: 14px;
        padding: 0.7rem 1rem;
        font-weight: 800;
      }
      .stButton>button:focus { outline: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_html=True)

def svg_image(path: str):
    p = Path(path)
    if p.exists():
        st.image(str(p), use_container_width=True)
    else:
        st.info(f"Falta el archivo: {path}")

def hero(title: str, subtitle: str):
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown(f"""
        <div class="card">
          <div class="pill">Hy-Line Brown</div>
          <h1 style="margin:0.6rem 0 0.2rem 0;">{title}</h1>
          <div class="muted" style="font-size:1.05rem;">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        svg_image("assets/hero.svg")

def goto(page: str):
    st.session_state["page"] = page
    st.rerun()

st.set_page_config(page_title="Panel de Gallinas (Consumo)", layout="wide")
init_db()
inject_css()

if "page" not in st.session_state:
    st.session_state["page"] = "Inicio"

st.sidebar.markdown("## 🐔 Menú")
pages = ["Inicio", "Lotes", "Orientación (Estándar)", "Registro real (opcional)", "Gráficas"]
page = st.sidebar.radio("Ir a", pages, index=pages.index(st.session_state["page"]))
st.session_state["page"] = page

lotes = fetch_lotes()
page = st.session_state["page"]

if page == "Inicio":
    hero("Panel de Gallinas", "Una app sencilla para orientar consumo de alimento y agua (por semana).")
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        svg_image("assets/card_orientacion.svg")
        st.markdown("### 🧭 Orientación")
        st.write("Calcula recomendado del manual por semana (automático).")
        if st.button("➡️ Ir a Orientación", use_container_width=True):
            goto("Orientación (Estándar)")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        svg_image("assets/card_registro.svg")
        st.markdown("### 📝 Registro real")
        st.write("Opcional: captura real y compara (Bajo/OK/Alto).")
        if st.button("➡️ Ir a Registro", use_container_width=True):
            goto("Registro real (opcional)")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        svg_image("assets/card_graficas.svg")
        st.markdown("### 📊 Gráficas")
        st.write("Recomendado vs real (si existe).")
        if st.button("➡️ Ver Gráficas", use_container_width=True):
            goto("Gráficas")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Lotes":
    hero("Lotes", "Crea un lote y selecciona la raza disponible (por ahora: Hy-Line Brown).")
    st.markdown("### 📦 Crear / Ver Lotes")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        nombre = st.text_input("Nombre del lote", placeholder="Ej: Lote A-2026")
        raza = st.selectbox("Raza (disponible)", list(RAZAS.keys()))
        fecha_inicio = st.date_input("Fecha de inicio del lote", value=date.today())
        aves_iniciales = st.number_input("Aves iniciales", min_value=1, step=1, value=1000)
        if st.button("✅ Guardar lote", use_container_width=True):
            try:
                add_lote(nombre.strip(), raza, fecha_inicio.strftime("%Y-%m-%d"), int(aves_iniciales))
                st.success("Lote creado.")
                st.rerun()
            except Exception as e:
                st.error(f"No se pudo guardar el lote: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("### Lotes existentes")
        if lotes.empty:
            st.info("Aún no hay lotes.")
        else:
            st.dataframe(lotes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Orientación (Estándar)":
    hero("Orientación (Estándar)", "La app calcula automáticamente el alimento (kg/día) y agua (L/día).")
    if lotes.empty:
        st.warning("Primero crea un lote en 'Lotes'.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lote_nombre = st.selectbox("Selecciona lote", lotes["nombre"].tolist(), key="ori_lote")
        lote_row = lotes[lotes["nombre"] == lote_nombre].iloc[0]
        raza = lote_row["raza"]
        std_df = RAZAS[raza]["estandares"]
        inicio_postura = int(RAZAS[raza]["inicio_postura_semana"])
        col1, col2, col3 = st.columns(3)
        with col1:
            semana = st.number_input("Semana del lote", min_value=1, max_value=200, step=1, value=1)
        with col2:
            aves_vivas = st.number_input("Aves vivas (para calcular totales)", min_value=1, step=1, value=int(lote_row["aves_iniciales"]))
        with col3:
            modo = st.selectbox("Tomar estándar como", ["Promedio", "Mínimo", "Máximo"])
        std = get_std_for_week(std_df, int(semana))
        if std is None:
            st.error("No hay estándar para esa semana.")
        else:
            g_obj, ml_obj = pick_targets(std, modo)
            al_kg, ag_l = calc_std_totals(int(aves_vivas), g_obj, ml_obj)
            faltan = max(0, inicio_postura - int(semana))
            if faltan > 0:
                st.info(f"⏳ Faltan **{faltan} semana(s)** para iniciar postura (referencia: semana {inicio_postura}).")
            else:
                st.success("✅ Tu lote ya está en edad de postura (semana 18 o más).")
            st.write("#### Estándar del manual (por ave)")
            cA, cB = st.columns(2)
            cA.metric("Alimento (g/ave/día)", f"{g_obj:.1f}")
            cB.metric("Agua (ml/ave/día)", f"{ml_obj:.1f}")
            st.write("#### Recomendación (totales del día para tu lote)")
            cC, cD = st.columns(2)
            cC.metric("Alimento recomendado (kg/día)", f"{al_kg:.2f}")
            cD.metric("Agua recomendada (L/día)", f"{ag_l:.2f}")
            st.caption(
                f"Rango semana {std['semana']}: "
                f"Alimento {std['al_min']:.0f}–{std['al_max']:.0f} g/ave/d; "
                f"Agua {std['ag_min']:.0f}–{std['ag_max']:.0f} ml/ave/d."
            )
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Registro real (opcional)":
    hero("Registro real (opcional)", "Si deseas, captura el consumo real para compararlo contra el rango del manual.")
    if lotes.empty:
        st.warning("Primero crea un lote en 'Lotes'.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lote_nombre = st.selectbox("Selecciona lote", lotes["nombre"].tolist(), key="reg_lote")
        lote_row = lotes[lotes["nombre"] == lote_nombre].iloc[0]
        lote_id = int(lote_row["id"])
        raza = lote_row["raza"]
        std_df = RAZAS[raza]["estandares"]
        inicio_postura = int(RAZAS[raza]["inicio_postura_semana"])
        col1, col2, col3 = st.columns(3)
        with col1:
            f = st.date_input("Fecha (para guardar)", value=date.today())
            semana = st.number_input("Semana del lote", min_value=1, max_value=200, step=1, value=1)
        with col2:
            aves_vivas = st.number_input("Aves vivas HOY", min_value=1, step=1, value=int(lote_row["aves_iniciales"]))
        with col3:
            modo = st.selectbox("Estándar como", ["Promedio", "Mínimo", "Máximo"], key="modo_reg")
        std = get_std_for_week(std_df, int(semana))
        if std is None:
            st.error("No hay estándar para esa semana.")
        else:
            g_obj, ml_obj = pick_targets(std, modo)
            al_std_kg, ag_std_l = calc_std_totals(int(aves_vivas), g_obj, ml_obj)
            faltan = max(0, inicio_postura - int(semana))
            if faltan > 0:
                st.info(f"⏳ Faltan **{faltan} semana(s)** para iniciar postura (referencia: semana {inicio_postura}).")
            else:
                st.success("✅ Tu lote ya está en edad de postura (semana 18 o más).")
            st.write("#### Recomendación (automática) según manual")
            cA, cB = st.columns(2)
            cA.metric("Alimento recomendado (kg/día)", f"{al_std_kg:.2f}")
            cB.metric("Agua recomendada (L/día)", f"{ag_std_l:.2f}")
            st.write("#### Captura REAL (solo si deseas comparar)")
            cC, cD = st.columns(2)
            with cC:
                alimento_real = st.number_input("Alimento REAL (kg/día) — opcional", min_value=0.0, step=0.5, value=0.0)
            with cD:
                agua_real = st.number_input("Agua REAL (L/día) — opcional", min_value=0.0, step=1.0, value=0.0)
            if alimento_real > 0:
                g_real = (alimento_real * 1000.0) / int(aves_vivas)
                st.write("Estado alimento (real vs rango):", status_vs_range(g_real, std["al_min"], std["al_max"]))
            if agua_real > 0:
                ml_real = (agua_real * 1000.0) / int(aves_vivas)
                st.write("Estado agua (real vs rango):", status_vs_range(ml_real, std["ag_min"], std["ag_max"]))
            if st.button("💾 Guardar registro (recomendado + real opcional)", use_container_width=True):
                upsert_registro(
                    lote_id=lote_id,
                    fecha=f.strftime("%Y-%m-%d"),
                    semana=int(semana),
                    aves_vivas=int(aves_vivas),
                    modo=modo,
                    al_std_kg=float(al_std_kg),
                    ag_std_l=float(ag_std_l),
                    al_real_kg=(None if alimento_real <= 0 else float(alimento_real)),
                    ag_real_l=(None if agua_real <= 0 else float(agua_real)),
                )
                st.success("Guardado.")
            reg = fetch_registros(lote_id)
            if not reg.empty:
                st.write("#### Historial")
                reg_show = reg.copy()
                reg_show["fecha"] = pd.to_datetime(reg_show["fecha"]).dt.date
                st.dataframe(reg_show.tail(30), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Gráficas":
    hero("Gráficas", "Visualiza el recomendado vs real (si existe) en tu historial.")
    if lotes.empty:
        st.warning("Primero crea un lote en 'Lotes'.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        lote_nombre = st.selectbox("Selecciona lote", lotes["nombre"].tolist(), key="graf_lote")
        lote_row = lotes[lotes["nombre"] == lote_nombre].iloc[0]
        lote_id = int(lote_row["id"])
        reg = fetch_registros(lote_id)
        if reg.empty:
            st.info("Aún no hay registros.")
        else:
            df = reg.copy()
            df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
            st.write("#### Alimento (kg/día)")
            cols = ["alimento_std_kg"]
            if df["alimento_real_kg"].notna().any():
                cols.append("alimento_real_kg")
            st.line_chart(df.set_index("fecha")[cols])
            st.write("#### Agua (L/día)")
            cols = ["agua_std_l"]
            if df["agua_real_l"].notna().any():
                cols.append("agua_real_l")
            st.line_chart(df.set_index("fecha")[cols])
            st.write("#### Tabla")
            st.dataframe(df.tail(50), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
