from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/verificar-data', methods=['POST'])
def verificar_data():
    try:
        # Obtém os dados do corpo da requisição
        data_requerimento = request.json.get('data')
        if not data_requerimento:
            return jsonify({"erro": "A data precisa ser informada no formato ISO 8601 (YYYY-MM-DD)"}), 400

        # Converte a string data para objeto datetime
        data_informada = datetime.fromisoformat(data_requerimento)
        data_atual = datetime.now()

        # Verifica a situação (passado, presente ou futuro)
        if data_informada.date() < data_atual.date():
            situacao = "passado"
        elif data_informada.date() > data_atual.date():
            situacao = "futuro"
        else:
            situacao = "presente"

        # Calcula as diferenças em dias, meses e anos
        diferenca = relativedelta(data_informada, data_atual)
        diferenca_dias = abs((data_informada - data_atual).days)
        diferenca_meses = abs(diferenca.months + (diferenca.years * 12))
        diferenca_anos = abs(diferenca.years)

        # Monta a resposta JSON
        resposta = {
            "situação": situacao,
            "dias_diferença": diferenca_dias if situacao in ["passado", "futuro"] else 0,
            "meses_diferença": diferenca_meses if situacao in ["passado", "futuro"] else 0,
            "anos_diferença": diferenca_anos if situacao in ["passado", "futuro"] else 0,
        }

        return jsonify(resposta)

    except ValueError:
        return jsonify({"erro": " Formato inválido de data, use o formato ISO 8601 (YYYY-MM-DD)"}), 400
    except Exception as e:
        return jsonify({"erro": f" Ocorreu um erro: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)






