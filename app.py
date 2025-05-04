import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.title('Ankara Metro İstasyon Grafiği')

def create_metro_graph():
    # Metro istasyonlarını ve bağlantılarını içeren veri yapısı
    G = nx.Graph()
    
    # İstasyonları ve bağlantıları ekle
    stations = {
        'Kızılay': {'line': 'Ankaray', 'pos': (0, 0)},
        'Batıkent': {'line': 'M1', 'pos': (-2, 2)},
        'Koru': {'line': 'M2', 'pos': (-3, -1)},
        'Keçiören': {'line': 'M4', 'pos': (2, 2)}
    }
    
    # İstasyonları grafa ekle
    for station, data in stations.items():
        G.add_node(station, **data)
    
    # Bağlantıları ekle
    connections = [
        ('Kızılay', 'Batıkent'),
        ('Kızılay', 'Koru'),
        ('Kızılay', 'Keçiören')
    ]
    G.add_edges_from(connections)
    
    return G

def plot_metro_graph():
    G = create_metro_graph()
    
    # Grafik ayarları
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # İstasyonları çiz
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=1000, alpha=0.6)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    nx.draw_networkx_labels(G, pos)
    
    plt.title("Ankara Metro Ağı")
    st.pyplot(plt)

if __name__ == "__main__":
    st.write("Bu uygulama, Ankara'daki metro istasyonlarını ve hatlarını görselleştirmektedir.")
    plot_metro_graph()
    
    st.sidebar.header("Bilgi")
    st.sidebar.write("""
    Bu görselleştirme, Ankara'daki metro hatlarının basitleştirilmiş bir temsilini göstermektedir.
    
    Metro Hatları:
    - Ankaray
    - M1 (Batıkent Hattı)
    - M2 (Çayyolu Hattı)
    - M4 (Keçiören Hattı)
    """) 