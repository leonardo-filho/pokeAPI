def extrair_evolucoes(chain):
    resultado = []

    def percorrer_evolucao(node):
        nome = node['species']['name']
        resultado.append(nome)
        for evolucao in node.get('evolves_to', []):
            percorrer_evolucao(evolucao)

    percorrer_evolucao(chain['chain'])
    return resultado
