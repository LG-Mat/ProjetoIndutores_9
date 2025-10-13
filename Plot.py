import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm

m = 0 # Determina os dados de quais materiais serão plotados

arquivos = {
    0: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMu.csv', # 0: Kool Mu
    1: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMM.csv', # 1: Kool Mu Max
    2: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMH.csv', # 2: Kool Mu Hf
    3: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\Xf.csv',  # 3: Xflux
    4: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\HF.csv',  # 4: High Flux
    5: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\EDG.csv', # 5: Edge
    6: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\MPP.csv'  # 6: Molypermalloy
}

caminho_arquivo = arquivos.get(m)
plot_df = pd.read_csv(caminho_arquivo)
plot_atual = plot_df.values

for p in range(2, 7, 1):
    X = plot_atual[:, 0]
    Y = plot_atual[:, 1]
    Z = plot_atual[:, p]
    C = plot_atual[:, 8]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if p != 2:
        surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0)

    if p == 2:
        scatter = ax.scatter(X, Y, Z, c=C, cmap='jet', marker='o', s=50)
        cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
        cbar.set_label('Temperatura (°C)')

    if p == 2: ax.view_init(elev=18, azim=60)
    if p == 3: ax.view_init(elev=20, azim=-135)  # perdas no nucleo
    if p == 4: ax.view_init(elev=20, azim=45)  # perdas no cobre e volume do núcleo
    if p == 5 or p == 6: ax.view_init(elev=20, azim=135)  # Temperatura e perdas totais

    if m == 0: plt.title('Kool Mu')
    if m == 1: plt.title('Kool Mu Max')
    if m == 2: plt.title('Kool Mu Hf')
    if m == 3: plt.title('Xflux')
    if m == 4: plt.title('High Flux')
    if m == 5: plt.title('Edge')
    if m == 6: plt.title('Molypermaloy')

    ax.set_xlabel(u'Δi(%)')
    ax.set_ylabel('Frequência (kHz)')

    if p == 2: ax.set_zlabel('Volume (cm³)')
    if p == 3 or p == 4 or p == 6: ax.set_zlabel('Perdas (W)')
    if p == 5: ax.set_zlabel('Temperatura (°C)')

    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(6))
    ax.zaxis.set_major_locator(MaxNLocator(5))

    fig.tight_layout()

    if p == 2:
        if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMu.jpg', dpi=600)
        if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMM.jpg', dpi=600)
        if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMH.jpg', dpi=600)
        if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\Xf.jpg', dpi=600)
        if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\HF.jpg', dpi=600)
        if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\EDG.jpg', dpi=600)
        if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\MPP.jpg', dpi=600)

    if p == 3:
        if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMu.png', dpi=600)
        if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMM.png', dpi=600)
        if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMH.png', dpi=600)
        if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\Xf.png', dpi=600)
        if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\HF.png', dpi=600)
        if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\EDG.png', dpi=600)
        if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\MPP.png', dpi=600)

    if p == 4:
        if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMu.png', dpi=600)
        if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMM.png', dpi=600)
        if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMH.png', dpi=600)
        if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\Xf.png', dpi=600)
        if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\HF.png', dpi=600)
        if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\EDG.png', dpi=600)
        if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\MPP.png', dpi=600)

    if p == 5:
        if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMu.png', dpi=600)
        if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMM.png', dpi=600)
        if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMH.png', dpi=600)
        if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\Xf.png', dpi=600)
        if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\HF.png', dpi=600)
        if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\EDG.png', dpi=600)
        if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\MPP.png', dpi=600)

    if p == 6:
        if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMu.png', dpi=600)
        if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMM.png', dpi=600)
        if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMH.png', dpi=600)
        if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\Xf.png', dpi=600)
        if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\HF.png', dpi=600)
        if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\EDG.png', dpi=600)
        if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\MPP.png', dpi=600)
