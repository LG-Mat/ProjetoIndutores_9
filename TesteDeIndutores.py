import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm

# Parametros de entrada =============================================
f_min = 10000
f_max = 210000
f_step = 10000
# TODO: adicionar caso em que nivel CC de corrente for zero
ripple_i_min = 5
ripple_i_max = 105  # 100% de ripple: ripple_i_max = 105
ripple_step = 5

corrente_cc = 5

temp_amb = 20
# ID 55164.0 | AWG:  21.0 | N de espiras:  156 | N em paralelo:  4 | Empilhamento:  1
# Parametros do indutor
ID_indutor = 58204
AWG_cond = 21
N_espiras = 156
N_paralelo = 4
n_empilhamento = 1

Vin = 100
D = 0.5

# ===================================================================
df = pd.read_csv(
    r'C:\Users\User\PycharmProjects\Projeto_Indutores\csv\DadosIndutor - Toroids - Copia (alterado) 01-04.csv')
df_awg = pd.read_csv(r'C:\Users\User\PycharmProjects\Projeto_Indutores\csv\Dados AWG.csv')

dados_plot = np.array([[0, 0, 0, 0, 0]])
dados_plot = np.delete(dados_plot, 0, 0)

ID_indice = 1
awg_indice = 1

for i in range(df.shape[0]):
    if df.values[i][0] == ID_indutor:
        ID_indice = i
        break

for i in range(df.shape[0]):
    if df_awg.values[i][0] == AWG_cond:
        awg_indice = i
        break

for f in range(f_min, f_max, f_step):  # Varredura na frequência
    print('Valor da frequência atual: ', f)
    for r in range(ripple_i_min, ripple_i_max, ripple_step):  # Varredura no ripple de corrente




        var_corrente = r * 0.01 * corrente_cc
        L = Vin * D / (var_corrente * f)  # [H]
        E = L * 1000 * (var_corrente + corrente_cc) ** 2  # [mHI²]

        executabilidade = 0
        n_empilhamento = 1

        while executabilidade != 1:
            # Cálculo do número de espiras
            N_espiras = np.sqrt((L * 1000000 * df.values[i][4] * 1000) / (
                    0.4 * np.pi * df.values[i][1] * df.values[i][10] * n_empilhamento))
            N_espiras = math.ceil(N_espiras)

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

            J = 450  # Densidade de corrente no condutor ()
            AWG = df_awg.values[awg_indice][1]
            A_necessaria = corrente_cc * (2 ** (1 / 2)) / J
            N_paralelo = A_necessaria / (df_awg.values[awg_indice][1] / 1000)
            N_paralelo = math.ceil(N_paralelo)

            # Fator de enrolamento =======================================================
            WindFactor = (df_awg.values[awg_indice][1] * 0.001 * N_espiras * N_paralelo) / (
                    df.values[i][23] / 100)
            print(WindFactor)

            if WindFactor <= 0.4:
                executabilidade = 1

            if WindFactor > 0.4:
                executabilidade = 0
                n_empilhamento = n_empilhamento + 1

            if n_empilhamento >= 5:
                break


            print(n_empilhamento, WindFactor, executabilidade)



            # Calculo das perdas no núcleo ==============================================
            var_corrente = r * 0.01 * corrente_cc
            H_max = 4 * np.pi * ((N_espiras / df.values[ID_indice][4]) * (corrente_cc + var_corrente / 2))
            H_min = 4 * np.pi * ((N_espiras / df.values[ID_indice][4]) * (corrente_cc - var_corrente / 2))

            B_max = ((df.values[ID_indice][14] + df.values[ID_indice][15] * H_max + df.values[ID_indice][
                16] * H_max ** 2) / (
                             1 + df.values[ID_indice][17] * H_max + df.values[ID_indice][18] * H_max ** 2)) ** \
                    df.values[ID_indice][19]
            B_min = ((df.values[ID_indice][14] + df.values[ID_indice][15] * H_min + df.values[ID_indice][
                16] * H_min ** 2) / (
                             1 + df.values[ID_indice][17] * H_min + df.values[ID_indice][18] * H_min ** 2)) ** \
                    df.values[ID_indice][19]

            Bpk = (B_max - B_min) / 2

            PL = df.values[ID_indice][11] * (Bpk ** df.values[ID_indice][12]) * (
                    (f * 0.001) ** df.values[ID_indice][13])  # mW/cm³

            perdas_nucleo = PL * df.values[ID_indice][4] * 0.001 * float(df.values[ID_indice][10] * n_empilhamento)
            perdas_nucleo = perdas_nucleo * 0.001

            # Perdas no condutor ====================================================
            comprimento_medio_da_espira = (2 * df.values[ID_indice][22] * n_empilhamento + 2 * (
                    df.values[ID_indice][20] - df.values[ID_indice][21])) / 10
            R_CC_condutor = comprimento_medio_da_espira * (df_awg.values[awg_indice][2] * 0.000001)
            R_CC_condutor_paralelo = 1 / (N_paralelo * (1 / R_CC_condutor))
            perdas_cobre = (corrente_cc ** 2) * R_CC_condutor_paralelo * N_espiras

            # Temperatura no núcleo =================================================
            temp_nuc = temp_amb + ((perdas_cobre + perdas_nucleo) / (df.values[ID_indice][10] * n_empilhamento * 0.0001))

            data = np.array([r, f / 1000, perdas_nucleo, perdas_cobre, temp_nuc])
            dados_plot = np.r_[dados_plot, [data]]

if dados_plot.shape[0] > 3:
    for p in range(2, 5, 1):
        X = dados_plot[:, 0]
        Y = dados_plot[:, 1]
        Z = dados_plot[:, p]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0)
        fig.colorbar(surf)

        if p == 2: ax.view_init(elev=20, azim=-135)  # perdas no nucleo
        if p == 3: ax.view_init(elev=20, azim=45)  # perdas no cobre
        if p == 4: ax.view_init(elev=20, azim=-115)  # Temperatura

        if p == 2: plt.title('Perdas no Núcleo')
        if p == 3: plt.title('Perdas no Cobre')
        if p == 4: plt.title('Temperatura')

        ax.set_xlabel(u'Δi(%)')
        ax.set_ylabel('Frequência (kHz)')

        if p == 2 or p == 3: ax.set_zlabel('Perdas (W)')
        if p == 4: ax.set_zlabel('Temperatura (°C)')

        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(6))
        ax.zaxis.set_major_locator(MaxNLocator(5))

        fig.tight_layout()

        if p == 2:
            plt.savefig(r'C:\Users\User\PycharmProjects\Projeto_Indutores\Figuras\TesteDeIndutor\PerdasNucleo.png', dpi=600)

        if p == 3:
            plt.savefig(r'C:\Users\User\PycharmProjects\Projeto_Indutores\Figuras\TesteDeIndutor\PerdasCobre.png', dpi=600)

        if p == 4:
            plt.savefig(r'C:\Users\User\PycharmProjects\Projeto_Indutores\Figuras\TesteDeIndutor\Temperatura.png', dpi=600)