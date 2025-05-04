{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "62729027-51a3-4677-aead-07eafe07f431",
   "metadata": {},
   "source": [
    "# 🚇 Ankara Metro Rota ve Grafik Uygulaması\n",
    "\n",
    "Bu proje, Ankara Metro sistemini bir **graf veri yapısı** olarak modelleyen ve duraklar arası **en kısa rotayı bulan** görsel bir Python uygulamasıdır. Kullanıcı arayüzü (GUI) **Tkinter** ile geliştirilmiştir ve metro hatları **NetworkX** kütüphanesi ile analiz edilmiştir.\n",
    "\n",
    "## 🧩 Özellikler\n",
    "\n",
    "- Tüm Ankara metro hatları graf olarak tanımlandı (A1, M1, M2, M3, M4, BAŞKENTRAY, T1).\n",
    "- Başlangıç ve varış duraklarını seçerek:\n",
    "  - En kısa rotayı bulma\n",
    "  - Harita üzerinden görsel rota çizimi\n",
    "  - Yaklaşık süre tahmini (2 dk/durak)\n",
    "- Metro haritası otomatik olarak tam ekran ve okunabilir şekilde çizilir.\n",
    "- Her durağın kaç komşusu olduğunu analiz eden çubuk grafik.\n",
    "- Grafın komşuluk matrisi çıkarıldı ve analiz için kullanıldı.\n",
    "\n",
    "## 🖥️ Kullanılan Teknolojiler\n",
    "\n",
    "- Python 3\n",
    "- Tkinter (GUI için)\n",
    "- NetworkX (graf modelleme için)\n",
    "- Matplotlib (grafik çizimi için)\n",
    "\n",
    "## 📊 Matematiksel Arka Plan\n",
    "\n",
    "- Metro sistemi **ağırlıksız, yönsüz bir graf** olarak modellenmiştir.\n",
    "- En kısa yol hesaplamalarında **Breadth-First Search (BFS)** tabanlı `nx.shortest_path` yöntemi kullanılmıştır.\n",
    "- **Komşuluk matrisi**, grafın yapısal analizleri için oluşturulmuştur.\n",
    "- Her durağın **komşu sayısı (degree)** istatistik olarak gösterilmiştir.\n",
    "\n",
    "## 📁 Nasıl Kullanılır?\n",
    "\n",
    "```bash\n",
    "# Gerekli kütüphaneler\n",
    "pip install networkx matplotlib\n",
    "\n",
    "# Uygulamayı başlat\n",
    "python metro_gui.py\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
