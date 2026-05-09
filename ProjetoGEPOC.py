import pandas as pd
import numpy as np
import math

Vin = 50
D = 0.5
iL = 2
f = 50000
DiL = 40  # 100% de ripple: ripple_i_max = 105

temp_amb = 20

df = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\DadosIndutor - Toroids - Copia (alterado) 01-04.csv')
df_awg = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\Dados AWG.csv')
df_gepoc = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\Nucleos GEPOC.csv')
df_awg_gepoc = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\AWG GEPOC.csv')

awg_indice = 0

df_filtrado = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
df_filtrado = np.delete(df_filtrado, 0, 0)
df_awg_filtrado = np.array([[0, 0, 0, 0]])
df_awg_filtrado = np.delete(df_awg_filtrado, 0, 0)
projetos = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0]])
projetos = np.delete(projetos, 0, 0)

for m in range(df.shape[0]):
    for k in range(df_gepoc.shape[0]):
        if df.values[m][0] == df_gepoc.values[k][0]:
            df_filtrado = np.r_[df_filtrado, [df.values[m][:]]]
print(df_awg.shape)
for m in range(df_awg.shape[0]):
    for k in range(df_awg_gepoc.shape[0]):
        if df_awg.values[m][0] == df_awg_gepoc.values[k][0]:
            df_awg_filtrado = np.r_[df_awg_filtrado, [df_awg.values[m][:]]]

#print('Quantidade de núcleos disponíveis no GEPOC: ', df_filtrado.shape[0])

print('Quantidade de AWGs disponíveis no GEPOC: ', df_awg_filtrado.shape[0])

for m in range(df_filtrado.shape[0]):

    var_corrente = DiL * 0.01 * iL
    L = (Vin * D) / (var_corrente * f)  # [H]
    E = L * 1000 * (var_corrente + iL) ** 2  # [mHI²]
    executabilidade = 0
    n_empilhamento = 1

    while executabilidade != 1:
        # Cálculo do número de espiras
        N_espiras = np.sqrt((L * 1000000 * df_filtrado[m][4] * 1000) / (
                0.4 * np.pi * df_filtrado[m][1] * df_filtrado[m][10] * n_empilhamento))
        N_espiras = math.ceil(N_espiras)

        # Indução magnética
        IM = (np.pi * 4 * N_espiras + (var_corrente + iL)) / df_filtrado[m][4]  # [Oe]
        permeabilidade = (1 / (df_filtrado[m][5] + df_filtrado[m][6] * IM ** df_filtrado[m][7])) * 0.01

        # Ajuste do número de espiras
        N_espiras = N_espiras / permeabilidade
        N_espiras = math.ceil(N_espiras)

        IM = (np.pi * 4 * N_espiras + (var_corrente + iL)) / df_filtrado[m][4]
        perm_final = (1 / (df_filtrado[m][5] + df_filtrado[m][6] * IM ** df_filtrado[m][7])) * 0.01
        """L_final = (N_espiras ** 2 * 0.4 * np.pi * df_filtrado[m][1]*perm_final * df_filtrado[m][10] * n_empilhamento) / (
                1000000 * df_filtrado[m][4] * 1000)"""
        L_final = L*perm_final

        # Seleção do condutor ====================================================
        d_util = 7.5 / (f ** (1 / 2))
        for n in range(df_awg_filtrado.shape[0]):
            if d_util > df_awg_filtrado[n][3]:  # df_awg[][3] diâmetro do condutor em cm
                awg_indice = n - 1
                break

        J = 450  # Densidade de corrente no condutor ()
        AWG = df_awg_filtrado[awg_indice][0]
        A_necessaria = iL * (2 ** (1 / 2)) / J
        N_paralelo = A_necessaria / (df_awg_filtrado[awg_indice][1] / 1000) # Área em E-10 cm²
        #N_paralelo = A_necessaria / ((2*np.pi*(d_util**(2))/4))
        N_paralelo = math.ceil(N_paralelo)

        # Fator de enrolamento =======================================================
        WindFactor = (df_awg_filtrado[awg_indice][1] * 0.001 * N_espiras * N_paralelo) / (
                df_filtrado[m][23] / 100)
        #print(WindFactor)

        if WindFactor <= 0.4:
            executabilidade = 1

        if WindFactor > 0.4:
            executabilidade = 0
            n_empilhamento = n_empilhamento + 1

        if n_empilhamento >= 5:
            break


        #print(n_empilhamento, WindFactor, executabilidade)

        # Calculo das perdas no núcleo ==============================================
        H_max = 4 * np.pi * ((N_espiras / df_filtrado[m][4]) * (iL + var_corrente / 2))
        H_min = 4 * np.pi * ((N_espiras / df_filtrado[m][4]) * (iL - var_corrente / 2))

        B_max = ((df_filtrado[m][14] + df_filtrado[m][15] * H_max + df_filtrado[m][16] * H_max ** 2) / (
                1 + df_filtrado[m][17] * H_max + df_filtrado[m][18] * H_max ** 2)) ** df_filtrado[m][19]
        B_min = ((df_filtrado[m][14] + df_filtrado[m][15] * H_min + df_filtrado[m][16] * H_min ** 2) / (
                1 + df_filtrado[m][17] * H_min + df_filtrado[m][18] * H_min ** 2)) ** df_filtrado[m][19]

        Bpk = (B_max - B_min) / 2

        PL = df_filtrado[m][11] * (Bpk ** df_filtrado[m][12]) * (
                (f * 0.001) ** df_filtrado[m][13])  # mW/cm³

        perdas_nucleo = PL * df_filtrado[m][4] * 0.001 * float(df_filtrado[m][10] * n_empilhamento)
        perdas_nucleo = perdas_nucleo * 0.001

        # Perdas no condutor ====================================================
        comprimento_medio_da_espira = (2 * df_filtrado[m][22] * n_empilhamento + 2 * (
               df_filtrado[m][20] - df_filtrado[m][21])) / 10
        R_CC_condutor = comprimento_medio_da_espira * (df_awg_filtrado[awg_indice][2] * 0.000001)
        R_CC_condutor_paralelo = 1 / (N_paralelo * (1 / R_CC_condutor))
        perdas_cobre = (iL ** 2) * R_CC_condutor_paralelo * N_espiras

        # Temperatura no núcleo =================================================
        area_externa = 2 * np.pi * (
            (df_filtrado[m][20] ** 2 - df_filtrado[m][21] ** 2)/4 + df_filtrado[m][22] * n_empilhamento * (
                df_filtrado[m][21] + df_filtrado[m][22]))
        area_externa = area_externa * 0.000001
        # Area externa
        temp_nuc = temp_amb + ((perdas_cobre + perdas_nucleo) / (area_externa)) ** 0.833

        comp_cond = 1.1*(N_espiras*(2*(df_filtrado[m][20]-df_filtrado[m][21]+df_filtrado[m][22]*n_empilhamento)))

    if WindFactor <= 0.4:
        data = np.array([df_filtrado[m][0], N_espiras, N_paralelo, n_empilhamento, perdas_nucleo, perdas_cobre, temp_nuc,
                             L_final, AWG, area_externa, comp_cond,H_max,B_max])
        projetos = np.r_[projetos, [data]]

for i in range(projetos.shape[0]):
    print('ID: ', projetos[i][0], '| N espiras: ', projetos[i][1], '| N paralelo: ', projetos[i][2], '| N empilhamento: ',
          projetos[i][3], '| AWG: ', projetos[i][8],'| Comprimento do condutor: ', math.trunc(projetos[i][10]), 'mm ', '| Perdas no núcleo: ', projetos[i][4], '| Perdas no cobre: ', projetos[i][5],
          '| Area externa: ', projetos[i][9],'| Temperartura: ', projetos[i][6], '| Indutância: ', projetos[i][7],
          projetos[i][11],projetos[i][12])

