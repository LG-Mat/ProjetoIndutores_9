import numpy as np
from scipy import signal

def PerdasCuCA(N_espiras, N_paralelo, f, corrente_cc, var_corrente, J, D, RF, PFT, d_cond, comprimento_medio_da_espira, ID):
    Fs = f * 10
    T = 1.0 / Fs
    N = 1024
    tempo_total = N * T

    freq_fundamental = f
    amplitude = var_corrente / 2
    t = np.linspace(0.0, tempo_total, N, endpoint=False)
    # Geração e FFT
    onda_base = amplitude * signal.sawtooth(2 * np.pi * freq_fundamental * t, width=D)
    onda_triangular_com_offset = onda_base + corrente_cc

    Y = np.fft.fft(onda_triangular_com_offset)
    amplitude_espectro = 2.0 / N * np.abs(Y)

    delta_f = Fs / N

    max_harmonics = int((Fs / 2) / f)
    # Inicializa a soma
    soma_P_CA = 0.0

    for n in range(0, max_harmonics + 1, 1):
        # Calcula a frequência do harmônico
        freq_harmonico = n * freq_fundamental

        indice_bin = int(round(freq_harmonico / delta_f))

        # Verifica se o índice está dentro dos limites da metade do espectro (N/2)
        if indice_bin < N // 2:
            magnitude = amplitude_espectro[indice_bin]
            large_circle_radius = PFT / float(RF)
            diam_cond_paralelo = large_circle_radius * d_cond
            PF = diam_cond_paralelo / (N_paralelo ** (1 / 2) * d_cond)
            porosidade = 1 / PF

            # Perdas CA
            N_camadas = 1
            circ_int = 2 * np.pi * ID / 2
            comp_diam_cond = diam_cond_paralelo * N_espiras

            while comp_diam_cond > circ_int:
                circ_int = 2 * np.pi * (ID - diam_cond_paralelo * N_camadas / 2) / 2
                if diam_cond_paralelo < circ_int:
                    N_camadas = N_camadas + 1
                comp_diam_cond = comp_diam_cond - circ_int

            if freq_harmonico != 0:
                # ρ: [Ωm] | μo = 1.256637 μH/m | f: Hz
                profund_pelicular = ((1.72 * 1e-8) / (np.pi * (4 * np.pi * 1e-7) * freq_harmonico)) ** (1 / 2) #[m]

                A_dow = (((np.pi / 4) ** 0.75) * (d_cond * 0.01 / profund_pelicular) * porosidade ** (1 / 2))

                R_CA = (A_dow * (((np.sinh(2 * A_dow) + np.sin(A_dow)) / (np.cosh(2 * A_dow) - np.cos(A_dow))) +
                        (2 * (N_camadas ** 2 - 1) / 3) * ((np.sinh(A_dow) - np.sin(A_dow)) / (np.cosh(A_dow) + np.cos(A_dow)))) *
                        1.72 * 0.00000001 * comprimento_medio_da_espira * N_espiras / (corrente_cc / J))

                P_CA = R_CA * (magnitude ** 2) / 2
                print('fh: ',freq_harmonico,'A_dow: ', A_dow,'prof_pelicular: ', profund_pelicular, 'R_CA: ', R_CA, 'P_CA', P_CA)
                #print(N_espiras, N_paralelo, f, corrente_cc, var_corrente, J, D, RF, PFT, d_cond, comprimento_medio_da_espira, ID)
                soma_P_CA += P_CA
    return soma_P_CA

if __name__ == '__main__':
    PerdasCuCA(92, 40, 90000, 5, 1.5, 450, 0.2, 1.29, 0.1403736042, 0.0267, 6.436, 22.56)