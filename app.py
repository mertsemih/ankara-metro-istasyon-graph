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

# Graf oluştur
G = nx.Graph()
for hat in hatlar.values():
    for i in range(len(hat) - 1):
        G.add_edge(hat[i], hat[i + 1])

# Sabit konumlar
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

# Başlık
st.set_page_config(layout="wide")
st.title("🚇 Ankara Metro Rota ve Harita Uygulaması")

# Durak seçimi
cols = st.columns(2)
with cols[0]:
    kaynak = st.selectbox("Başlangıç Durağı", sorted(G.nodes()))
with cols[1]:
    hedef = st.selectbox("Varış Durağı", sorted(G.nodes()))

# Rota Göster
if st.button("Rota Göster"):
    yol, uzunluk = en_kisa_yol(G, kaynak, hedef)
    if yol:
        st.success(f"{kaynak} → {hedef} arası {uzunluk} durak ({uzunluk * 2} dakika)")
        st.markdown(" → ".join(yol))
    else:
        st.error("Yol bulunamadı.")
    
    # Harita çizimi
    pos = sabit_konumlar_sutun(hatlar)
    fig, ax = plt.subplots(figsize=(18, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=9, ax=ax)

    if yol:
        path_edges = list(zip(yol[:-1], yol[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=yol, node_color='orange', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)

    st.pyplot(fig)

# Komşuluk analizi
st.header("📊 Durakların Komşu Sayısı")
komsular = {node: len(list(G.neighbors(node))) for node in G.nodes()}
sorted_komsular = dict(sorted(komsular.items(), key=lambda item: item[1], reverse=True))

fig2, ax2 = plt.subplots(figsize=(18, 6))
ax2.bar(sorted_komsular.keys(), sorted_komsular.values(), color='skyblue')
ax2.set_ylabel("Komşu Sayısı")
ax2.set_xlabel("Durak")
ax2.set_title("Her Durağın Komşu Sayısı")
plt.xticks(rotation=90)
st.pyplot(fig2)
