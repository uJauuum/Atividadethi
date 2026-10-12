import datetime
import requests


def cotar():
    hoje = datetime.date.today()


    dias = [hoje - datetime.timedelta(days=i) for i in range(365)]

    cotacoes = []

    for dia in dias:
        data = dia.strftime("%Y%m%d")  
        url = (
            "https://economia.awesomeapi.com.br/json/daily/USD-BRL/"
            f"?start_date={data}&end_date={data}"
        )

        valor = None
        try:
            resposta = requests.get(url, timeout=10)
            dados = resposta.json()
          
            if resposta.status_code == 200 and isinstance(dados, list) and dados:
                valor = float(dados[0]["bid"])
        except (requests.RequestException, ValueError, KeyError):
            valor = None

       
        if valor is None and cotacoes:
            valor = cotacoes[-1]

        cotacoes.append(valor)

    primeiro_valido = next((v for v in cotacoes if v is not None), None)
    cotacoes = [primeiro_valido if v is None else v for v in cotacoes]

    return cotacoes


if __name__ == "__main__":
    resultado = cotar()
    hoje = datetime.date.today()

    print(f"Total de cotações: {len(resultado)}")
    for i, valor in enumerate(resultado):
        dia = hoje - datetime.timedelta(days=i)
        print(f"{dia.strftime('%d/%m/%Y')}: R$ {valor:.4f}")