import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm

# Parametros de entrada =============================================
f_min = 20000
f_max = 210000
f_step = 10000
# TODO: adicionar caso em que nivel CC de corrente for zero
ripple_i_min = 20
ripple_i_max = 105  # 100% de ripple: ripple_i_max = 105
ripple_step = 5

corrente_cc = 5
Vin = 100
D = 0.5

temp_amb = 20
# ===================================================================

dados_plot_KMu = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_KMu = np.delete(dados_plot_KMu, 0, 0)
dados_plot_KMM = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_KMM = np.delete(dados_plot_KMM, 0, 0)
dados_plot_KMH = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_KMH = np.delete(dados_plot_KMH, 0, 0)
dados_plot_Xf = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_Xf = np.delete(dados_plot_Xf, 0, 0)
dados_plot_HF = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_HF = np.delete(dados_plot_HF, 0, 0)
dados_plot_EDG = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_EDG = np.delete(dados_plot_EDG, 0, 0)
dados_plot_MPP = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
dados_plot_MPP = np.delete(dados_plot_MPP, 0, 0)

awg_indice = 0

#df = pd.read_csv(
#    r'C:\Users\User\PycharmProjects\Projeto_Indutores\csv\DadosIndutor - Toroids - Copia (alterado) 01-04.csv')
#df_awg = pd.read_csv(r'C:\Users\User\PycharmProjects\Projeto_Indutores\csv\Dados AWG.csv')
df = pd.read_csv(
    r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\DadosIndutor - Toroids - Copia (alterado) 01-04.csv')
df_awg = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\Dados AWG.csv')

for f in range(f_min, f_max, f_step):  # Varredura na frequência
    print('Valor da frequência atual: ', f)
    for r in range(ripple_i_min, ripple_i_max, ripple_step):  # Varredura no ripple de corrente
        matriz_selecao = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_selecao = np.delete(matriz_selecao, 0, 0)
        matriz_KMu = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_KMu = np.delete(matriz_KMu, 0, 0)
        matriz_KMM = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_KMM = np.delete(matriz_KMM, 0, 0)
        matriz_KMH = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_KMH = np.delete(matriz_KMH, 0, 0)
        matriz_Xf = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_Xf = np.delete(matriz_Xf, 0, 0)
        matriz_HF = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_HF = np.delete(matriz_HF, 0, 0)
        matriz_EDG = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_EDG = np.delete(matriz_EDG, 0, 0)
        matriz_MPP = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        matriz_MPP = np.delete(matriz_MPP, 0, 0)

        var_corrente = r * 0.01 * corrente_cc
        L = Vin * D / (var_corrente * f)  # [H]
        E = L * 1000 * (var_corrente + corrente_cc) ** 2  # [mHI²]

        executabilidade = 0
        n_empilhamento = 1

        while executabilidade != 1:
            nucleos_elegiveis = np.array([0])
            for i in range(df.shape[0]):
                if (df.values[i][8] * n_empilhamento) > E:
                    # Cálculo do número de espiras
                    N_espiras = np.sqrt((L * 1000000 * df.values[i][4] * 1000) / (
                            0.4 * np.pi * df.values[i][1] * df.values[i][10] * n_empilhamento))
                    N_espiras = math.ceil(N_espiras)

                    N_espiras_i = N_espiras

                    # Indução magnética
                    IM = (np.pi * 4 * N_espiras + (var_corrente + corrente_cc)) / df.values[i][4]  # [Oe]
                    permeabilidade = (1 / (df.values[i][5] + df.values[i][6] * IM ** df.values[i][7])) * 0.01

                    # Ajuste do número de espiras
                    N_espiras = N_espiras / permeabilidade
                    N_espiras = math.ceil(N_espiras)

                    IM = (np.pi * 4 * N_espiras + (var_corrente + corrente_cc)) / df.values[i][4]
                    perm_final = (1 / (df.values[i][5] + df.values[i][6] * IM ** df.values[i][7])) * 0.01
                    L_final = (N_espiras ** 2 * 0.4 * np.pi * df.values[i][1] * df.values[i][10] * n_empilhamento) / (
                            1000000 * df.values[i][4] * 1000)

                    # Seleção do condutor ====================================================
                    d_util = 7.5 / (f ** (1 / 2))
                    for n in range(df_awg.shape[0]):
                        if d_util > df_awg.values[n][3]:  # df_awg[][3] diâmetro do condutor em cm
                            awg_indice = n - 1
                            break

                    # TODO: verificar se valor de condutores em paralelo está correto
                    J = 450  # Densidade de corrente no condutor ()
                    AWG = df_awg.values[awg_indice][1]
                    A_necessaria = corrente_cc * (2 ** (1 / 2)) / J
                    N_paralelo = A_necessaria / (df_awg.values[awg_indice][1] / 1000)
                    N_paralelo = math.ceil(N_paralelo)

                    # Fator de enrolamento =======================================================
                    WindFactor = (df_awg.values[awg_indice][1] * 0.001 * N_espiras * N_paralelo) / (
                            df.values[i][23] / 100)

                    if WindFactor <= 0.4:
                        executabilidade = 1
                        nucleos_elegiveis = np.r_[nucleos_elegiveis, [df.values[i][0]]]

                    if nucleos_elegiveis.shape[0] == 1:
                        executabilidade = 0
                        n_empilhamento = n_empilhamento + 1

                    # Calculo das perdas no núcleo ==============================================
                    H_max = 4 * np.pi * ((N_espiras / df.values[i][4]) * (corrente_cc + var_corrente / 2))
                    H_min = 4 * np.pi * ((N_espiras / df.values[i][4]) * (corrente_cc - var_corrente / 2))

                    B_max = ((df.values[i][14] + df.values[i][15] * H_max + df.values[i][16] * H_max ** 2) / (
                        1 + df.values[i][17] * H_max + df.values[i][18] * H_max ** 2)) ** df.values[i][19]
                    B_min = ((df.values[i][14] + df.values[i][15] * H_min + df.values[i][16] * H_min ** 2) / (
                        1 + df.values[i][17] * H_min + df.values[i][18] * H_min ** 2)) ** df.values[i][19]

                    Bpk = (B_max - B_min) / 2

                    PL = df.values[i][11] * (Bpk ** df.values[i][12]) * (
                            (f * 0.001) ** df.values[i][13])  # mW/cm³

                    perdas_nucleo = PL * df.values[i][4] * 0.001 * float(df.values[i][10] * n_empilhamento)
                    perdas_nucleo = perdas_nucleo * 0.001

                    # Perdas no condutor ====================================================
                    comprimento_medio_da_espira = (2 * df.values[i][22] * n_empilhamento + 2 * (
                            df.values[i][20] - df.values[i][21])) / 10
                    R_CC_condutor = comprimento_medio_da_espira * (df_awg.values[awg_indice][2] * 0.000001)
                    R_CC_condutor_paralelo = 1 / (N_paralelo * (1 / R_CC_condutor))
                    perdas_cobre = (corrente_cc ** 2) * R_CC_condutor_paralelo * N_espiras

                    # Temperatura no núcleo =================================================
                    area_externa = 2*np.pi*((df.values[i][20]**2 - df.values[i][21]**2)/4 + df.values[i][22]*n_empilhamento*(df.values[i][21]+df.values[i][22]))
                    area_externa = area_externa*0.0001
                    temp_nuc = temp_amb + ((perdas_cobre + perdas_nucleo)*1000 / (area_externa))**0.833

                    perdas_totais = perdas_cobre + perdas_nucleo

                    #if df.values[i][0] == 77073:
                        #print('frequência: ', f, '| ripple: ', r, '| AWG: ', df_awg.values[awg_indice][0], 'N inicial', N_espiras_i, '| N de espiras: ', N_espiras,
                        #      '| N em paralelo: ', N_paralelo, '| Empilhamento: ', n_empilhamento, 'WindFactor: ', WindFactor, 'Indutância: ', L,
                        #      'Energia ', E)

                    if executabilidade != 0:
                        dados = np.array(
                            [1, df.values[i][0], L_final, N_espiras, 1, float(df.values[i][9]) * 0.001 * n_empilhamento,
                             f * 0.001, var_corrente * 100 / 5, perdas_nucleo, perdas_cobre, AWG, N_paralelo,
                             temp_nuc, n_empilhamento, perdas_totais])

                        matriz_selecao = np.r_[matriz_selecao, [dados]]

                        #print('frequência: ', f, '| ripple: ', r, '| ID', dados[1], '| AWG: ', df_awg.values[awg_indice][0], '| N de espiras: ', N_espiras,
                        #      '| N em paralelo: ', N_paralelo, '| Empilhamento: ', n_empilhamento, 'WindFactor: ', WindFactor)

                        if 77000 <= df.values[i][0] < 78000: matriz_KMu = np.r_[matriz_KMu, [dados]]
                        if 79000 <= df.values[i][0] < 80000: matriz_KMM = np.r_[matriz_KMM, [dados]]
                        if 76000 <= df.values[i][0] < 77000: matriz_KMH = np.r_[matriz_KMH, [dados]]
                        if 78000 <= df.values[i][0] < 79000: matriz_Xf = np.r_[matriz_Xf, [dados]]
                        if 58000 <= df.values[i][0] < 59000: matriz_HF = np.r_[matriz_HF, [dados]]
                        if 59000 <= df.values[i][0] < 60000: matriz_EDG = np.r_[matriz_EDG, [dados]]
                        if 55000 <= df.values[i][0] < 56000: matriz_MPP = np.r_[matriz_MPP, [dados]]

        if matriz_selecao.shape[0] > 0:
            matrizes = np.array([matriz_KMu, matriz_KMM, matriz_KMH, matriz_Xf,
                                 matriz_HF, matriz_EDG, matriz_MPP], dtype=object)

            for m in range(matrizes.shape[0]):
                matriz_atual = matrizes[m]
                if matriz_atual.shape[0] > 0:
                    menor_vol = matriz_atual[0][5]
                    menor_n_esp = matriz_atual[0][3]
                    id_n_espiras = 0
                    menor_perdas_nucleo = matriz_atual[0][8]
                    menor_perdas_cobre = matriz_atual[0][9]
                    menor_temp_nuc = matriz_atual[0][12]
                    menor_perdas_totais = matriz_atual[0][14]

                    for i in range(matriz_atual.shape[0]):
                        if matriz_atual[i][8] < menor_perdas_nucleo:
                            menor_perdas_nucleo = matriz_atual[i][8]

                        if matriz_atual[i][9] < menor_perdas_cobre:
                            menor_perdas_cobre = matriz_atual[i][9]

                        if matriz_atual[i][12] < menor_temp_nuc:
                            menor_temp_nuc = matriz_atual[i][12]

                        if matriz_atual[i][14] < menor_perdas_totais:
                            menor_perdas_totais = matriz_atual[i][14]

                        if matriz_atual[i][5] < menor_vol:
                            menor_vol = matriz_atual[i][5]

                    for i in range(matriz_atual.shape[0]):
                        if matriz_atual[i][5] == menor_vol:
                            if matriz_atual[i][3] < menor_n_esp:
                                if matriz_atual[i][3] < menor_n_esp:
                                    menor_n_esp = matriz_atual[i][3]
                                    id_n_espiras = i

                    data = np.array([r, f/1000, matriz_atual[id_n_espiras][5], menor_perdas_nucleo,
                                     menor_perdas_cobre, menor_temp_nuc, menor_perdas_totais, matriz_atual[1][1]])

                    if 77000 <= data[7] < 78000: dados_plot_KMu = np.r_[dados_plot_KMu, [data]]
                    if 79000 <= data[7] < 80000: dados_plot_KMM = np.r_[dados_plot_KMM, [data]]
                    if 76000 <= data[7] < 77000: dados_plot_KMH = np.r_[dados_plot_KMH, [data]]
                    if 78000 <= data[7] < 79000: dados_plot_Xf = np.r_[dados_plot_Xf, [data]]
                    if 58000 <= data[7] < 59000: dados_plot_HF = np.r_[dados_plot_HF, [data]]
                    if 59000 <= data[7] < 60000: dados_plot_EDG = np.r_[dados_plot_EDG, [data]]
                    if 55000 <= data[7] < 56000: dados_plot_MPP = np.r_[dados_plot_MPP, [data]]

matrizes_plot = np.array([dados_plot_KMu, dados_plot_KMM, dados_plot_KMH, dados_plot_Xf,
                                 dados_plot_HF, dados_plot_EDG, dados_plot_MPP], dtype=object)

for m in range(matrizes_plot.shape[0]):
    plot_atual = matrizes_plot[m]
    if plot_atual.shape[0] > 3:
        for p in range(2, 7, 1):
            X = plot_atual[:, 0]
            Y = plot_atual[:, 1]
            Z = plot_atual[:, p]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0)
            fig.colorbar(surf)

            if p == 3: ax.view_init(elev=20, azim=-135)  # perdas no nucleo
            if p == 4 or p == 5 or p == 2: ax.view_init(elev=20, azim=45)  # perdas no cobre, temperatura, volume do núcleo
            if p == 6: ax.view_init(elev=20, azim=135)

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
                if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMu.pdf', dpi=600)
                if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMM.pdf', dpi=600)
                if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\KMH.pdf', dpi=600)
                if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\Xf.pdf', dpi=600)
                if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\HF.pdf', dpi=600)
                if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\EDG.pdf', dpi=600)
                if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Volume\MPP.pdf', dpi=600)

            if p == 3:
                if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMu.pdf', dpi=600)
                if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMM.pdf', dpi=600)
                if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\KMH.pdf', dpi=600)
                if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\Xf.pdf', dpi=600)
                if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\HF.pdf', dpi=600)
                if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\EDG.pdf', dpi=600)
                if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasNucleo\MPP.pdf', dpi=600)

            if p == 4:
                if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMu.pdf', dpi=600)
                if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMM.pdf', dpi=600)
                if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\KMH.pdf', dpi=600)
                if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\Xf.pdf', dpi=600)
                if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\HF.pdf', dpi=600)
                if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\EDG.pdf', dpi=600)
                if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\PerdasCobre\MPP.pdf', dpi=600)

            if p == 5:
                if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMu.pdf', dpi=600)
                if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMM.pdf', dpi=600)
                if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\KMH.pdf', dpi=600)
                if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\Xf.pdf', dpi=600)
                if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\HF.pdf', dpi=600)
                if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\EDG.pdf', dpi=600)
                if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Temperatura\MPP.pdf', dpi=600)

            if p == 6:
                if m == 0: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMu.pdf', dpi=600)
                if m == 1: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMM.pdf', dpi=600)
                if m == 2: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\KMH.pdf', dpi=600)
                if m == 3: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\Xf.pdf', dpi=600)
                if m == 4: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\HF.pdf', dpi=600)
                if m == 5: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\EDG.pdf', dpi=600)
                if m == 6: plt.savefig(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\Figuras\Perdas\MPP.pdf', dpi=600)
