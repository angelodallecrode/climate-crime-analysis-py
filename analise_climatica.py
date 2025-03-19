import matplotlib.pyplot as plt

def ler_arquivo(nome_arquivo):
    dados = []
    with open(nome_arquivo, 'r') as arq:
        cabecalho = arq.readline().strip().split(',')
        print(f"Colunas disponíveis: {cabecalho}")
        for linha in arq:
            valores = linha.strip().split(',')
            registro = dict(zip(cabecalho, valores))
            dados.append(registro)
    return dados

def visualizar_intervalo(dados, mes_inicio, ano_inicio, mes_fim, ano_fim, opcao):
    print(f"Exibindo dados de {mes_inicio}/{ano_inicio} até {mes_fim}/{ano_fim}...")
    for registro in dados:
        data = registro['data']
        dia, mes, ano = map(int, data.split('/'))
        if ano_inicio <= ano <= ano_fim and mes_inicio <= mes <= mes_fim:
            if opcao == 1:
                print(registro)
            elif opcao == 2:
                print(f"Data: {data}, Precipitação: {registro['precip']}")
            elif opcao == 3:
                print(f"Data: {data}, Temp Máx: {registro['maxima']}, Temp Mín: {registro['minima']}")
            elif opcao == 4:
                print(f"Data: {data}, Umidade: {registro['um_relativa']}, Vento: {registro['vel_vento']}")

def mes_mais_chuvoso(dados):
    precip_total_por_mes = {}
    for registro in dados:
        data = registro['data']
        dia, mes, ano = data.split('/')
        try:
            precipitacao = float(registro['precip'])
        except ValueError:
            continue
        
        chave = f'{mes}/{ano}'
        precip_total_por_mes[chave] = precip_total_por_mes.get(chave, 0) + precipitacao

    mes_mais_chuvoso = max(precip_total_por_mes, key=precip_total_por_mes.get)
    print(f"Mês mais chuvoso: {mes_mais_chuvoso}, Precipitação: {precip_total_por_mes[mes_mais_chuvoso]}")
    return mes_mais_chuvoso, precip_total_por_mes[mes_mais_chuvoso]

def media_temp_minima_por_mes(dados, mes):
    temp_minima_por_ano = {}
    for registro in dados:
        data = registro['data']
        dia, mes_dado, ano = data.split('/')
        if '2006' <= ano <= '2016' and mes_dado.zfill(2) == mes.zfill(2):
            chave = f"{mes_dado}/{ano}"
            try:
                temp_minima = float(registro['minima'])
            except ValueError:
                continue
            if chave in temp_minima_por_ano:
                temp_minima_por_ano[chave].append(temp_minima)
            else:
                temp_minima_por_ano[chave] = [temp_minima]

    medias = {chave: sum(valores) / len(valores) for chave, valores in temp_minima_por_ano.items()}
    return medias

def media_geral_temp_minima(medias):
    print(medias)
    if len(medias) == 0:
        print("Não há dados suficientes para calcular a média.")
        return
    
    total = sum(medias.values())
    media_geral = total / len(medias)
    print(f"A média geral da temperatura mínima é: {media_geral:.2f}")

def gerar_grafico(medias, mes):
    if len(medias) == 0:
        print("Não há dados suficientes para gerar o gráfico.")
        return
    
    meses = {
        '01': 'janeiro', '02': 'fevereiro', '03': 'março', '04': 'abril',
        '05': 'maio', '06': 'junho', '07': 'julho', '08': 'agosto',
        '09': 'setembro', '10': 'outubro', '11': 'novembro', '12': 'dezembro'
    }
    
    anos = [chave[-4:] for chave in medias.keys()]
    temp_minimas = list(medias.values())
    
    plt.bar(anos, temp_minimas, color='blue')
    plt.xlabel('Ano')
    plt.ylabel('Média de Temperatura Mínima (°C)')
    plt.title(f'Média de Temperatura Mínima em {meses[mes]} (2006-2016)')
    plt.show()

def media_temp_minima_ano_a_ano(dados, mes):
    meses_validos = {'01': 'janeiro', '02': 'fevereiro', '03': 'março', '04': 'abril', '05': 'maio', '06': 'junho', 
                     '07': 'julho', '08': 'agosto', '09': 'setembro', '10': 'outubro', '11': 'novembro', '12': 'dezembro'}

    if mes not in meses_validos:
        print("Mês inválido. Por favor, informe um mês válido (MM).")
        return

    temp_minima_por_ano = {}
    for registro in dados:
        data = registro['data']
        dia, mes_dado, ano = data.split('/')
        if '2006' <= ano <= '2016' and mes_dado.zfill(2) == mes.zfill(2):
            chave = f"{meses_validos[mes]}{ano}"
            try:
                temp_minima = float(registro['minima'])
            except ValueError:
                continue
            if chave in temp_minima_por_ano:
                temp_minima_por_ano[chave].append(temp_minima)
            else:
                temp_minima_por_ano[chave] = [temp_minima]

    medias = {chave: sum(valores) / len(valores) for chave, valores in temp_minima_por_ano.items()}
    return medias

def main():
    nome_arquivo = 'dados.csv'  
    dados = ler_arquivo(nome_arquivo)
    
    mes_inicio = int(input("Informe o mês de início (MM): "))
    ano_inicio = int(input("Informe o ano de início (YYYY): "))
    mes_fim = int(input("Informe o mês de fim (MM): "))
    ano_fim = int(input("Informe o ano de fim (YYYY): "))
    opcao = int(input("Escolha o que deseja visualizar (1: Todos, 2: Precipitação, 3: Temperatura, 4: Umidade e Vento): "))
    visualizar_intervalo(dados, mes_inicio, ano_inicio, mes_fim, ano_fim, opcao)
    
    mes_mais_chuvoso(dados)
    
    mes = input("Informe o mês para calcular a média de temperatura mínima (MM): ")
    medias = media_temp_minima_por_mes(dados, mes)
    
    gerar_grafico(medias, mes)
    
    media_geral_temp_minima(medias)

    
    mes = input("Informe o mês para calcular a média anual da temperatura mínima (MM): ")
    medias_anuais = media_temp_minima_ano_a_ano(dados, mes)
    
    if medias_anuais:
        print("Média anual da temperatura mínima:")
        for ano, media in medias_anuais.items():
            print(f"{ano}: {media:.2f}")

if __name__ == "__main__":
    main()