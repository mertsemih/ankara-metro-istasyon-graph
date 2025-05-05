import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Metro hatları
hatlar = {
    "A1": ["AŞTİ", "Emek", "Bahçelievler", "Beşevler", "Maltepe", "Demirtepe", "Kızılay", "Kolej", "Kurtuluş", "Dikimevi"],
    "M1": ["Kızılay", "Sıhhiye", "Ulus", "Atatürk Kültür Merkezi", "Akköprü", "İvedik", "Yenimahalle", "Demetevler", "Hastane", "Macunköy", "OSTİM", "Batıkent"],
    "M2": ["Kızılay", "Necatibey", "Milli Kütüphane", "Söğütözü", "MTA", "ODTÜ", "Bilkent", "Tarım Bakanlığı", "Beytepe", "Ümitköy", "Çayyolu", "Koru"],
    "M3": ["Batıkent", "Batı Merkez", "Mesa", "Botanik", "İstanbul Yolu", "Eryaman 1-2", "Eryaman 5", "Devlet Mah.", "Harikalar Diyarı", "Fatih", "GOP", "OSB-Törekent"],
    "M4": ["Atatürk Kültür Merkezi", "ASKİ", "Dışkapı", "Meteoroloji", "Belediye", "Mecidiye", "Kuyubaşı", "Dutluk", "Şehitler"],
    "BAŞKENTRAY": ["Sincan", "Lale", "Elvankent", "Eryaman YHT", "Özgüneş", "Etimesgut", "Havadurağı", "Yıldırım", "Behiçbey", "Motor", "Gazi", "Gazi Mahallesi", "Hipodrom", "Ankara Gar", "Yenişehir", "Kurtuluş", "Cebeci", "Demirlibahçe", "Saimekadın", "Mamak", "Bağderesi", "Üreğil", "Köstence", "Kayas"],
    "T1": ["Yenimahalle", "Yunus Emre", "TRT Seyir", "Şentepe"]
}

renkler = {
    "A1": "green",
    "M1": "blue",
    "M2": "orange",
    "M3": "purple",
    "M4": "red",
    "BAŞKENTRAY": "gray",
    "T1": "gold"
}

# Graph yapısı
G = nx.Graph()
for hat in hatlar.values():
    for i in range(len(hat) - 1):
        G.add_edge(hat[i], hat[i + 1])

# Sabit konum
def sabit_konumlar_sutun(hatlar_dict):
    pos = {}
    x_step = 5
    y_step = -1
    x = 0
    for hat in hatlar_dict.values():
        for i, durak in enumerate(hat):
            if durak not in pos:
                pos[durak] = (x, i * y_step)
        x += x_step
    return pos

# En kısa yol
def en_kisa_yol(graf, kaynak, hedef):
    try:
        yol = nx.shortest_path(graf, source=kaynak, target=hedef)
        return yol, len(yol) - 1
    except nx.NetworkXNoPath:
        return None, None

# Kullanılan hatları bul
def kullanilan_hatlari_bul(yol):
    kullanilan_hatlar = set()
    for i in range(len(yol) - 1):
        d1, d2 = yol[i], yol[i+1]
        for hat_adi, duraklar in hatlar.items():
            if d1 in duraklar and d2 in duraklar:
                idx1 = duraklar.index(d1)
                idx2 = duraklar.index(d2)
                if abs(idx1 - idx2) == 1:
                    kullanilan_hatlar.add(hat_adi)
    return kullanilan_hatlar

# Uygulama başlığı
st.title("Ankara Metro Rota ve Harita Uygulaması")

duraklar = sorted(G.nodes())
kaynak = st.selectbox("Başlangıç Durağı", duraklar)
hedef = st.selectbox("Varış Durağı", duraklar)

if st.button("Rota Göster"):
    yol, uzunluk = en_kisa_yol(G, kaynak, hedef)
    if yol:
        st.success(f"{kaynak} → {hedef} arası en kısa yol ({uzunluk} durak / yaklaşık {uzunluk * 2.5} dk):")
        st.markdown(" → ".join(yol))

        # 🔁 Kullanılan hatları bul ve yaz
        kullanilan = kullanilan_hatlari_bul(yol)
        if kullanilan:
            renkli = [f"<span style='color:{renkler[h]}; font-weight:bold'>{h}</span>" for h in kullanilan]
            st.markdown("🛤 Kullanılan Hatlar: " + ", ".join(renkli), unsafe_allow_html=True)

        # Harita çizimi
        pos = sabit_konumlar_sutun(hatlar)
        fig, ax = plt.subplots(figsize=(15, 10))

        # 🎨 Tüm hatları renkli çiz
        for hat_adi, duraklar in hatlar.items():
            edges = [(duraklar[i], duraklar[i + 1]) for i in range(len(duraklar) - 1)]
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=renkler[hat_adi], width=2, ax=ax)

        # 🟠 Yol çizimi
        path_edges = list(zip(yol[:-1], yol[1:]))
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=yol, node_color='orange', ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)

        st.pyplot(fig)
    else:
        st.error(f"{kaynak} → {hedef} arasında yol bulunamadı.")
