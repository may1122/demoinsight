import streamlit as st
import pandas as pd

from components import (
    render_kpi_cards,
    render_executive_panel,
    render_risk_center,
    render_navigation,
    money_fmt,
)


def get_df(data):
    df = data.get("df")
    if df is None:
        return pd.DataFrame()
    return df


def render_general_page(data):
    render_kpi_cards(data)
    st.markdown("<br>", unsafe_allow_html=True)
    render_executive_panel(data)
    render_risk_center(data)


def render_stock_page(data):
    st.markdown("## 📦 Stok Bitiş Tahmini")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    preview_cols = [
        col for col in [
            "Ürün Adı",
            "Kategori",
            "Mevcut Stok",
            "Son 60 Gün Çıkış",
            "Stok Ay Karşılığı",
            "Sipariş Önerisi",
        ]
        if col in df.columns
    ]

    if preview_cols:
        st.dataframe(df[preview_cols].head(50), use_container_width=True)
    else:
        st.dataframe(df.head(50), use_container_width=True)


def render_order_page(data):
    st.markdown("## 🛒 Sipariş Asistanı")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    if "Sipariş Önerisi" in df.columns:
        order_df = df[df["Sipariş Önerisi"].astype(str).str.strip() != ""]
    else:
        order_df = df.head(0)

    st.metric("Sipariş Önerisi Olan Ürün", len(order_df))

    if order_df.empty:
        st.success("Sipariş önerisi görünen ürün bulunamadı.")
    else:
        st.dataframe(order_df.head(50), use_container_width=True)


def render_miad_page(data):
    st.markdown("## ⏳ Miad Takibi")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    if "Miad Tarihi" not in df.columns:
        st.warning("Miad Tarihi kolonu bulunamadı.")
        st.dataframe(df.head(20), use_container_width=True)
        return

    temp = df.copy()
    temp["Miad Tarihi"] = pd.to_datetime(temp["Miad Tarihi"], errors="coerce", dayfirst=True)
    today = pd.Timestamp.today().normalize()
    temp["Kalan Gün"] = (temp["Miad Tarihi"] - today).dt.days

    miad_df = temp[temp["Kalan Gün"].notna()].sort_values("Kalan Gün")

    st.metric("Miad Bilgisi Olan Ürün", len(miad_df))

    st.dataframe(
        miad_df.head(50),
        use_container_width=True,
    )


def render_dead_stock_page(data):
    st.markdown("## 💀 Ölü Stok Analizi")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    if "Son 60 Gün Çıkış" in df.columns and "Mevcut Stok" in df.columns:
        dead_df = df[
            (pd.to_numeric(df["Mevcut Stok"], errors="coerce").fillna(0) > 0)
            & (pd.to_numeric(df["Son 60 Gün Çıkış"], errors="coerce").fillna(0) <= 0)
        ]
    else:
        dead_df = df.head(0)

    st.metric("Ölü Stok Adayı", len(dead_df))

    if dead_df.empty:
        st.success("Ölü stok adayı bulunamadı.")
    else:
        st.dataframe(dead_df.head(50), use_container_width=True)


def render_profitability_page(data):
    st.markdown("## 💰 Kârlılık")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    ciro = df["Ciro TL"].sum() if "Ciro TL" in df.columns else 0
    kar = df["Brüt Kar TL"].sum() if "Brüt Kar TL" in df.columns else 0
    margin = kar / ciro if ciro else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Toplam Ciro", money_fmt(ciro))

    with col2:
        st.metric("Brüt Kâr", money_fmt(kar))

    with col3:
        st.metric("Kâr Marjı", f"%{margin * 100:.1f}")

    st.dataframe(df.head(50), use_container_width=True)


def render_category_page(data):
    st.markdown("## 📊 Kategori Analizi")

    df = get_df(data)

    if df.empty:
        st.info("Veri bulunamadı.")
        return

    if "Kategori" not in df.columns:
        st.warning("Kategori kolonu bulunamadı.")
        st.dataframe(df.head(20), use_container_width=True)
        return

    agg_dict = {}

    if "Ciro TL" in df.columns:
        agg_dict["Ciro TL"] = "sum"

    if "Brüt Kar TL" in df.columns:
        agg_dict["Brüt Kar TL"] = "sum"

    if "Adet" in df.columns:
        agg_dict["Adet"] = "sum"

    if not agg_dict:
        st.dataframe(df[["Kategori"]].head(50), use_container_width=True)
        return

    category_df = df.groupby("Kategori").agg(agg_dict).reset_index()

    st.dataframe(category_df, use_container_width=True)


def render_report_page(data):
    st.markdown("## 📥 Rapor")

    st.info("Bu sade mimaride rapor modülü sonra `report_utils.py` içine taşınacak.")

    df = get_df(data)

    if df.empty:
        return

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "CSV Rapor İndir",
        data=csv,
        file_name="ayca_insight_rapor.csv",
        mime="text/csv",
    )


def render_page(data):
    page = render_navigation()

    st.markdown("---")

    if page == "general":
        render_general_page(data)

    elif page == "stock":
        render_stock_page(data)

    elif page == "order":
        render_order_page(data)

    elif page == "miad":
        render_miad_page(data)

    elif page == "dead_stock":
        render_dead_stock_page(data)

    elif page == "profitability":
        render_profitability_page(data)

    elif page == "category":
        render_category_page(data)

    elif page == "report":
        render_report_page(data)
