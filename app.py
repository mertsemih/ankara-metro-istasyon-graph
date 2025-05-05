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

# En kısa yolu bul
def en_kisa_yol(graf, kaynak, hedef):
    try:
        yol = nx.shortest_path(graf, source=kaynak, target=hedef)
        return yol, len(yol) - 1
    except nx.NetworkXNoPath:
        return None, None

# Streamlit Arayüzü
st.title("Ankara Metro Rota ve Harita Uygulaması")

duraklar = sorted(G.nodes())
kaynak = st.selectbox("Başlangıç Durağı", duraklar)
hedef = st.selectbox("Varış Durağı", duraklar)

if st.button("Rota Göster"):
    yol, uzunluk = en_kisa_yol(G, kaynak, hedef)
    if yol:
        st.success(f"{kaynak} → {hedef} arası en kısa yol ({uzunluk} durak / yaklaşık {uzunluk * 2} dk):")
        st.markdown(" → ".join(yol))
        
        # Harita çizimi
        pos = sabit_konumlar_sutun(hatlar)
        fig, ax = plt.subplots(figsize=(15, 10))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=9, ax=ax)
        path_edges = list(zip(yol[:-1], yol[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=yol, node_color='orange', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
        st.pyplot(fig)
    else:
        st.error(f"{kaynak} → {hedef} arasında yol bulunamadı.")
