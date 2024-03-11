import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class LeitorDataFrame:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df = pd.read_csv(caminho_arquivo)

    def open_files(self):
        dados_arquivo = []

        if self.caminho_arquivo.endswith('.txt'):
            with open(self.caminho_arquivo, 'r') as file:
                for linha in file:
                    try:
                        dados = json.loads(linha)
                        dados_arquivo.append(dados)
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON no arquivo {self.caminho_arquivo}: {e}")

        elif self.caminho_arquivo.endswith('.csv'):
            dados_arquivo = pd.read_csv(self.caminho_arquivo)

        else:
            raise ValueError("Formato de arquivo não suportado. Use .json ou .csv.")

        df = pd.DataFrame(dados_arquivo)
        self.df=df
        return df
    

    def merge_files(self, df_1, df_2):
        df = pd.concat([df_1, df_2], ignore_index=True)
        df["origem"] = ["df_1" for _ in range(len(df_1))] + ["df_2" for _ in range(len(df_2))]
        data_frame=LeitorDataFrame()
        data_frame.df=df
        return data_frame


class Graficos:
    def __init__(self, df):
        self.df = df
        self.methods = {
            "linearplot": self.linearplot,
            "linearplot_hue": self.linearplot_hue,
            "displot": self.displot,
            "jointplot": self.jointplot,
            "jointplot_with_reg": self.jointplot_with_reg,
            "lmplot": self.lmplot,
            "barplot": self.barplot,
            "map_FacetGrid": self.map_FacetGrid,
            "relplot": self.relplot,
            "dispersão 3D":self.dispersao_3d,
        }
    def get_method_names(self):
       return list(self.methods.keys())

    def plot(self, method_name, *args, **kwargs):
        if method_name not in self.methods:
            raise ValueError(f"Método de plotagem '{method_name}' não encontrado.")

        return self.methods[method_name](*args, **kwargs)
    def dispersao_3d(self,x,y,z,name=None):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.df[x], self.df[y], self.df[z], c='blue', marker='o')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)
        self.save(name)
        return fig

    def linearplot(self, x, y, name=None):
        fig, ax = plt.subplots(figsize=(10, 6))  # Define o tamanho da figura
        sns.lineplot(x=self.df[x], y=self.df[y], ax=ax).set(title="Grafico de linha")
        self.save(name)
        return fig

    def linearplot_hue(self, x, y, hue, name=None):
        fig, ax = plt.subplots(figsize=(10, 6))  # Define o tamanho da figura
        sns.lineplot(x=self.df[x], y=self.df[y], hue=self.df[hue], ax=ax).set(title="Grafico de linha")
        self.save(name)
        return fig

    def displot(self, x, name=None):
        plt.figure(figsize=(10, 6))
        fig=sns.displot(self.df[x], kde=True).set(title="Grafico de Barras")
        self.save(name)
        return fig

    def jointplot(self, x, y, hue, name=None):
        plt.figure(figsize=(10, 6))
        fig=sns.jointplot(data=self.df, x=self.df[x], y=self.df[y], hue=self.df[hue])
        self.save(name)
        return fig

    def jointplot_with_reg(self, x, y, name=None):
        plt.figure(figsize=(10, 6))
        fig=sns.jointplot(data=self.df, x=self.df[x], y=self.df[y], kind="reg")
        self.save(name)
        return fig

    def lmplot(self, x, y, hue, name=None):
        plt.figure(figsize=(10, 6))
        fig=sns.lmplot(data=self.df, x=x, y=y, hue=hue)
        self.save(name)
        return fig

    def barplot(self, x, y, name=None):
        plt.figure(figsize=(5, 6))
        fig,ax=plt.subplots()
        sns.barplot(data=self.df, x=x, y=y, palette=sns.color_palette("flare"),ax=ax)
        self.save(name)
        return fig     

    def map_FacetGrid(self, x,col, name=None):
        plt.figure(figsize=(10, 6))
        p = sns.FacetGrid(data=self.df, col=col)
        fig = p.map(sns.histplot, x, kde=True)
        self.save(name)
        return fig

    def relplot(self, x, y, hue, size, name=None):
        plt.figure(figsize=(10, 6))
        
        fig=sns.relplot(data=self.df.head(400), x=x, y=y, hue=hue, size=size, sizes=(1, 100), alpha=0.8, palette=sns.color_palette())
        self.save(name)
        return fig

    def save(self,name=None):
        if name:
            plt.savefig(name, format="png")