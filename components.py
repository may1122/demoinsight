def prepare_data(df):
    """
    Şimdilik veriyi paketler.
    İleride stok, miad, skor, görev ve kaçırılan kâr hesapları burada yapılacak.
    """
    return {
        "df": df,
        "score": 82,
        "critical_stock_count": 0,
        "miad_count": 0,
        "dead_stock_value": 0,
        "order_count": 0,
        "lost_profit": 0,
    }
