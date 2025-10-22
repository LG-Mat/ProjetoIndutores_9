import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd


N_paralelo = 12

df_radius = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\RelacaoDeRaios.csv')
df_awg = pd.read_csv(r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\Dados AWG.csv')

awg_indice = 8

comprimento_medio_da_espira = 8
N_espiras = 80
J = 450

f = 20000
corrente_cc = 5
r = 20
D = 0.2
var_corrente = r * 0.01 * corrente_cc

Fs = f*10
T = 1.0 / Fs
N = 1024
tempo_total = N * T

freq_fundamental = f
amplitude = var_corrente/2

t = np.linspace(0.0, tempo_total, N, endpoint=False)

# Geração e FFT
onda_base = amplitude * signal.sawtooth(2 * np.pi * freq_fundamental * t, width=D)
onda_triangular_com_offset = onda_base + corrente_cc

Y = np.fft.fft(onda_triangular_com_offset)
xf = np.fft.fftfreq(N, T)
amplitude_espectro = 2.0/N * np.abs(Y)

delta_f = Fs / N

indice_fundamental = int(freq_fundamental / delta_f)

max_harmonics = int((Fs / 2) / f)

# Inicializa a soma
soma_magnitudes_harmonicos = 0.0
soma_P_CA = 0.0
indices_encontrados = []
magnitudes_encontradas = []

for indice_paralelo in range(0, df_radius.shape[0], 1):
    if df_radius.values[indice_paralelo][0] == N_paralelo:
        break

print(f"Frequência Fundamental (f): {freq_fundamental / 1000} kHz")
print(f"Resolução da Frequência (delta_f): {delta_f:.2f} Hz\n")

for n in range(0, max_harmonics + 1, 1):
    # Calcula a frequência do harmônico
    freq_harmonico = n * freq_fundamental

    # Calcula o índice do bin correspondente
    # Arredo
    #damos para o inteiro mais próximo
    indice_bin = int(round(freq_harmonico / delta_f))

    # Verifica se o índice está dentro dos limites da metade do espectro (N/2)
    if indice_bin < N // 2:
        magnitude = amplitude_espectro[indice_bin]

        print(f"Harmônico {n} ({freq_harmonico / 1000:.1f} kHz): Magnitude = {magnitude:.4f}")

        # calculo da resistência CA
        #large_circle_radius = float(df_radius.values[indice_paralelo][1]) / float(df_radius.values[indice_paralelo][2])
        large_circle_radius = 1.3 / float(df_radius.values[indice_paralelo][2])
        diam_cond_paralelo = large_circle_radius * (df_awg.values[awg_indice][3]/2)
        PF = diam_cond_paralelo*2/(N_paralelo**(1/2)*df_awg.values[awg_indice][3])
        porosidade = 1/PF

        # Perdas CA
        N_camadas = 1
        circ_int = 2*np.pi*34.75/2
        comp_diam_cond = diam_cond_paralelo * N_espiras

        while comp_diam_cond > circ_int:
            circ_int = 2*np.pi*(34.75-diam_cond_paralelo*N_camadas/2)/2
            if diam_cond_paralelo < circ_int:
                N_camadas = N_camadas + 1
            comp_diam_cond = comp_diam_cond - circ_int
        # TODO: PASSAR TUDO PARA METRO
        if freq_harmonico != 0:
            # ρ: [Ωm] | μo = 1.256637 μH/m | f: Hz
            profund_pelicular = ((1.72 * 0.00000001) / (np.pi * 4*np.pi*0.0000001 * freq_harmonico)) ** (1/2)
            print('freq_harmonico: ', freq_harmonico)
            print('N_paralelo:', N_paralelo, 'df_radius.values[indice_paralelo][3] ', df_radius.values[indice_paralelo][2])
            print('diam_cond_paralelo ', diam_cond_paralelo)
            print('Radius factor ', df_radius.values[indice_paralelo][2])
            print('d ', df_awg.values[awg_indice][3])
            print('profund_pelicular ', profund_pelicular)
            print('porosidade ', porosidade)
            print('diametro ', df_awg.values[awg_indice][3])
            A_dow = (((np.pi / 4) ** 0.75) * (df_awg.values[awg_indice][3]*0.01 / profund_pelicular) * porosidade**(1/2))
            print('A_dow ', A_dow)
            print(print(np.sinh(A_dow)))
            R_CA = (A_dow * (((np.sinh(2 * A_dow) + np.sin(A_dow)) / (np.cosh(2 * A_dow) - np.cos(A_dow))) +
                    (2 * (N_camadas ** 2 - 1) / 3) * ((np.sinh(A_dow) - np.sin(A_dow)) / (np.cosh(A_dow) + np.cos(A_dow)))) *
                    1.72 * 0.00000001 * comprimento_medio_da_espira * N_espiras / (corrente_cc / J))

            P_CA = R_CA*(magnitude**2)/2
            print(freq_harmonico, magnitude, R_CA, P_CA, '\n')

            soma_P_CA += P_CA
            soma_magnitudes_harmonicos += magnitude
            indices_encontrados.append(indice_bin)
            magnitudes_encontradas.append(magnitude)

# --- 4. Exibição do Resultado ---

print("\n" + "=" * 50)
print(f"Soma Total das Magnitudes dos Harmônicos (Componente AC): {soma_magnitudes_harmonicos:.4f}")
print(soma_P_CA)
print("=" * 50)

# --- 4. Plotagem dos Resultados ---

plt.figure(figsize=(12, 6))

# Plotagem no Domínio do Tempo
plt.subplot(2, 1, 1)
plt.plot(t, onda_triangular_com_offset, label='Onda Triangular')
plt.title('Sinal de Onda Triangular no Domínio do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, 1/freq_fundamental * 2) # Mostra apenas 2 períodos para clareza

# Plotagem no Domínio da Frequência
plt.subplot(2, 1, 2)
# Focamos apenas na primeira metade do espectro (frequências positivas)
# O índice N//2 marca o limite da frequência de Nyquist (Fs/2)
plt.plot(xf[:N//2], amplitude_espectro[:N//2])
plt.title('Espectro de Frequência (FFT) da Onda Triangular')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude Normalizada')
plt.grid(True)
plt.xlim(0, Fs/2) # Limite máximo na Frequência de Nyquist

# Para garantir que os gráficos não se sobreponham
plt.tight_layout()
plt.show()