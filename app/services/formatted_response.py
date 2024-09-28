# Ivan Germano: Função para formatar a resposta JSON em um Novo JSON que facilite a construção do Gráfico no FrontEnd
def format_climate_response(api_response):
    """
    Esta função recebe a resposta JSON da API da NASA e a formata em um novo JSON para facilitar o uso no FrontEnd.
    
    Parâmetros:
        api_response (dict): O JSON retornado pela API da NASA contendo os dados climáticos (temperatura, precipitação, etc.).

    Retorna:
        dict: Um JSON formatado contendo os dados no seguinte formato:
              {
                  "message": "Resposta API - Clima",
                  "status": "sucesso",
                  "data": [
                      {
                          "day": "YYYYMMDD",
                          "temperature": valor_da_temperatura,
                          "precipitation": valor_da_precipitação
                      }
                  ]
              }
    """
    try:
        # Extraindo os parâmetros de interesse da resposta da API da NASA
        parameters = api_response.get("properties", {}).get("parameter", {})

        # Obtendo os dados de temperatura (T2M) e precipitação (PRECTOTCORR)
        temperatures = parameters.get("T2M", {})
        precipitations = parameters.get("PRECTOTCORR", {})

        # Inicializando uma lista para armazenar os dados formatados para cada dia
        formatted_data = []

        # Iterando sobre as temperaturas para organizar o formato
        for day, temp in temperatures.items():
            # Obtendo o valor de precipitação para o mesmo dia (se disponível)
            precipitation = precipitations.get(day, 0)

            # Adicionando os dados formatados à lista
            formatted_data.append({
                "day": day,               # A data do registro (formato YYYYMMDD)
                "temperature": temp,      # A temperatura registrada no dia
                "precipitation": precipitation  # O valor de precipitação registrado no dia
            })

        # Criando a estrutura final do JSON que será retornado ao FrontEnd
        formatted_response = {
            "message": "Resposta API - Clima",
            "status": "sucesso",
            "data": formatted_data
        }

        return formatted_response

    except KeyError as e:
        # Capturando exceções relacionadas à ausência de chaves esperadas no JSON e retornando um erro formatado
        return {
            "message": "Erro ao processar os dados da API",
            "status": "falha",
            "error": str(e)  # Inclui a descrição do erro ocorrido
        }