# Ivan Germano: Função para formatar a resposta JSON em um novo JSON que facilite a construção do gráfico no FrontEnd
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
        # Extrai os parâmetros de interesse (como temperatura) da resposta da API.
        parameters = api_response.get("properties", {}).get("parameter", {})
        
        # Obtém os dados de temperatura (T2M = temperatura a 2 metros).
        temperatures = parameters.get("T2M", {})
        
        # Inicializa uma lista que armazenará os dados formatados para cada dia.
        formatted_data = []

        # Itera sobre os dados de temperatura, organizando-os no novo formato.
        for day, temp in temperatures.items():
            formatted_data.append({
                "day": day,             # A data do registro (formato YYYYMMDD).
                "temperature": temp,    # A temperatura registrada no dia.
                "precipitation": 0      # Valor fixo 0, pois não foi definido ainda qual vai ser o parametro da precipitação.
            })

        # Cria a estrutura final do JSON que será retornado ao FrontEnd.
        formatted_response = {
            "message": "Resposta API - Clima",
            "status": "sucesso",
            "data": formatted_data
        }

        return formatted_response

    except KeyError as e:
        # Captura exceções relacionadas à ausência de chaves esperadas no JSON e retorna um erro formatado.
        return {
            "message": "Erro ao processar os dados da API",
            "status": "falha",
            "error": str(e)  # Inclui a descrição do erro ocorrido.
        }