from collections import defaultdict
import tkinter.messagebox as msg


class MapaRotas:
    def __init__(self):
        self.grafo = defaultdict(list)   # cidade -> [vizinhos]
        self.detalhes = {}               # (origem, destino) -> (rodovia, km)

    def adicionar_rota(self, origem, destino, rodovia="", km=0):
        """Adiciona rota bidirecional entre duas cidades."""
        if destino not in self.grafo[origem]:
            self.grafo[origem].append(destino)
        if origem not in self.grafo[destino]:
            self.grafo[destino].append(origem)
        self.detalhes[(origem, destino)] = (rodovia, km)
        self.detalhes[(destino, origem)] = (rodovia, km)

    def _formatar_caminho(self, caminho):
        """Transforma lista de cidades em texto legível com rodovias e km."""
        partes = []
        total_km = 0
        for i in range(len(caminho) - 1):
            a, b = caminho[i], caminho[i + 1]
            rod, km = self.detalhes.get((a, b), ("", 0))
            trecho = f"{a} --[{rod} | {km}km]--> {b}" if rod else f"{a} --> {b}"
            partes.append(trecho)
            total_km += km
        return "\n".join(partes), total_km

    def bfs(self, inicio, fim):
        """
        Busca em Largura (BFS).
        Garante o caminho com o menor número de paradas entre início e fim.
        """
        visitados = set()
        fila = [inicio]
        anterior = {inicio: None}

        while fila:
            atual = fila.pop(0)

            if atual == fim:
                caminho = []
                no = fim
                while no is not None:
                    caminho.append(no)
                    no = anterior[no]
                caminho.reverse()
                texto, km = self._formatar_caminho(caminho)
                mensagem = f"Caminho (BFS — menos paradas):\n\n{texto}"
                if km:
                    mensagem += f"\n\nDistância total estimada: {km} km"
                msg.showinfo("Rota encontrada", mensagem)
                return

            if atual not in visitados:
                visitados.add(atual)
                for vizinho in self.grafo[atual]:
                    if vizinho not in visitados:
                        fila.append(vizinho)
                        anterior[vizinho] = atual

        msg.showinfo("Aviso", f"Nenhuma rota encontrada entre '{inicio}' e '{fim}'.")

    def dfs(self, inicio, fim, visitados=None, anterior=None):
        """
        Busca em Profundidade (DFS).
        Explora o grafo indo o mais fundo possível antes de retroceder.
        Retorna True se encontrou caminho, False caso contrário.
        """
        if visitados is None:
            visitados = set()
        if anterior is None:
            anterior = {inicio: None}

        visitados.add(inicio)

        if inicio == fim:
            caminho = []
            no = fim
            while no is not None:
                caminho.append(no)
                no = anterior[no]
            caminho.reverse()
            texto, km = self._formatar_caminho(caminho)
            mensagem = f"Caminho (DFS — exploração profunda):\n\n{texto}"
            if km:
                mensagem += f"\n\nDistância total estimada: {km} km"
            msg.showinfo("Rota encontrada", mensagem)
            return True

        for vizinho in self.grafo[inicio]:
            if vizinho not in visitados:
                anterior[vizinho] = inicio
                if self.dfs(vizinho, fim, visitados, anterior):
                    return True

        return False

    def carregar_arquivo(self, caminho_arquivo):
        """Carrega rotas salvas de um arquivo .txt."""
        try:
            with open(caminho_arquivo, "r") as f:
                for linha in f:
                    partes = linha.strip().split()
                    if len(partes) >= 2:
                        orig, dest = partes[0], partes[1]
                        rod = partes[2] if len(partes) > 2 else ""
                        km  = int(partes[3]) if len(partes) > 3 else 0
                        self.adicionar_rota(orig, dest, rod, km)
        except FileNotFoundError:
            pass

    def salvar_arquivo(self, caminho_arquivo):
        """Salva todas as rotas em um arquivo .txt."""
        vistos = set()
        with open(caminho_arquivo, "w") as f:
            for cidade, destinos in self.grafo.items():
                for dest in destinos:
                    par = tuple(sorted([cidade, dest]))
                    if par not in vistos:
                        rod, km = self.detalhes.get((cidade, dest), ("", 0))
                        f.write(f"{cidade} {dest} {rod} {km}\n")
                        vistos.add(par)