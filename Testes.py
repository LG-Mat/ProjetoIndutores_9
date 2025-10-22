import pandas as pd

arquivos = {
    0: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMu.csv',
    1: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMM.csv',
    2: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\KMH.csv',
    3: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\Xf.csv',
    4: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\HF.csv',
    5: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\EDG.csv',
    6: r'C:\Users\lgmat\PycharmProjects\Projeto_Indutores\Projeto_Indutores\CSV\CSV_plot\MPP.csv'
}

for m in range(0, 7, 1):
    caminho_arquivo = arquivos.get(m)
    df = pd.read_csv(caminho_arquivo)

    todos_numericos = (df.dtypes.apply(pd.api.types.is_numeric_dtype)).all()
    print(f"O DataFrame inteiro é composto apenas por tipos numéricos? {todos_numericos}", m)
