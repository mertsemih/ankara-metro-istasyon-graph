from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Metro hatları
hatlar = {
    "A1": ["AŞTİ", "Emek", "Bahçelievler", "Beşevler", "Maltepe", "Demirtepe", "Kızılay", "Kolej", "Kurtuluş", "Cebeci", "Dikimevi"],
    "M1": ["Kızılay", "Sıhhiye", "Adliye", "Ulus", "Atatürk Kültür Merkezi", "Akköprü", "İvedik", "Yenimahalle", "Demetevler", "Hastane", "Macunköy", "OSTİM", "Batıkent"],
    "M2": ["Kızılay", "Necatibey", "Milli Kütüphane", "Söğütözü", "MTA", "Emek", "Bilkent", "Beytepe", "Ümitköy", "Çayyolu", "Koru"],
    "M3": ["Batıkent", "Batı Merkez", "Mesa", "Botanik", "İstanbul Yolu", "Eryaman 5", "Eryaman 1-2", "Devlet Mah.", "Harikalar Diyarı", "GOP", "OSB-Törekent"],
    "M4": ["Atatürk Kültür Merkezi", "ASKİ", "Dışkapı", "Meteoroloji", "Belediye", "Mecidiye", "Kuyubaşı", "Dutluk", "Şehitler"],
    "BAŞKENTRAY": ["Sincan", "Lale", "Elvankent", "Eryaman YHT", "Özgüneş", "Etimesgut", "Havadurağı", "Yıldırım", "Behiçbey", "Motor", "Gazi", "Gazi Mahallesi", "Hipodrom", "Ankara Gar", "Kurtuluş", "Cebeci", "Demirlibahçe", "Saimekadın", "Mamak", "Bağderesi", "Üreğil", "Köstence", "Kayas"],
    "T1": ["Yenimahalle", "İvedik", "Yunus Emre", "TRT Seyir", "Şentepe"]
}

# Graf yapısı
G = nx.Graph()
for hat in hatlar.values():
    for i in range(len(hat) - 1):
        G.add_edge(hat[i], hat[i + 1])

# Sabit pozisyonlar
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

# En kısa yolu bul
def en_kisa_yol(graf, kaynak, hedef):
    try:
        yol = nx.shortest_path(graf, source=kaynak, target=hedef)
        return yol, len(yol) - 1
    except nx.NetworkXNoPath:
        return None, None

# Streamlit arayüzü
st.title("🚇 Ankara Metro Haritası ve Rota Hesaplayıcı")

duraklar = sorted(G.nodes())
kaynak = st.selectbox("Başlangıç Durağı", duraklar)
hedef = st.selectbox("Varış Durağı", duraklar)

if st.button("En Kısa Rota Hesapla"):
    yol, uzunluk = en_kisa_yol(G, kaynak, hedef)
    if yol:
        st.success(f"➡️ {kaynak} → {hedef} ({uzunluk} durak / yaklaşık {uzunluk*2} dakika)")
        st.write(" → ".join(yol))

        fig, ax = plt.subplots(figsize=(16, 10))
        pos = sabit_konumlar_sutun(hatlar)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, edge_color='gray', font_size=8, ax=ax)

        # Yol vurgulama
        path_edges = list(zip(yol[:-1], yol[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=yol, node_color='orange', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)

        st.pyplot(fig)
    else:
        st.error("🚫 İki durak arasında yol bulunamadı.")

