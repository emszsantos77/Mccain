import pandas as pd
import json
import os

def converter_excel_para_json():
    arquivo_excel = 'MCCAIN.xlsx'
    
    if not os.path.exists(arquivo_excel):
        print(f"Erro: O arquivo '{arquivo_excel}' não foi encontrado na pasta!")
        return

    print("Lendo dados do arquivo Excel (.xlsx)...")
    df = pd.read_excel(arquivo_excel)

    # 1. Cálculos dos KPIs Gerais
    faturamento_total = df['Vlr. Total'].sum()
    volume_total = int(df['Quantidade'].sum())
    pdvs_totais = df['Cnpj_CPF'].nunique()

    # 2. Processamento do Ranking dos Vendedores
    ranking = df.groupby('Nome Vendedor').agg(
        Faturamento=('Vlr. Total', 'sum'),
        Volume=('Quantidade', 'sum'),
        PDVs=('Cnpj_CPF', 'nunique')
    ).reset_index()

    ranking = ranking.sort_values(by='Faturamento', ascending=False).reset_index(drop=True)

    # 3. Identificar os Campeões do Pódio
    p1_nome = ranking.loc[0, 'Nome Vendedor'] if len(ranking) > 0 else "NENHUM"
    p1_vol = int(ranking.loc[0, 'Volume']) if len(ranking) > 0 else 0
    p1_fat = f"{ranking.loc[0, 'Faturamento']/1000:.1f}K".replace('.', ',') if len(ranking) > 0 else "0K"
    p1_pdv = int(ranking.loc[0, 'PDVs']) if len(ranking) > 0 else 0

    p2_nome = ranking.loc[1, 'Nome Vendedor'] if len(ranking) > 1 else "NENHUM"
    p2_vol = int(ranking.loc[1, 'Volume']) if len(ranking) > 1 else 0
    p2_fat = f"{ranking.loc[1, 'Faturamento']/1000:.1f}K".replace('.', ',') if len(ranking) > 1 else "0K"
    p2_pdv = int(ranking.loc[1, 'PDVs']) if len(ranking) > 1 else 0

    # 4. Montar a lista do Ranking Geral (Agora incluindo o campo 'foto' para cada um)
    lista_ranking_geral = []
    for idx, row in ranking.iterrows():
        nome_vendedor = row['Nome Vendedor']
        lista_ranking_geral.append({
            "posicao": f"{idx + 1}º",
            "nome": nome_vendedor,
            "foto": f"{nome_vendedor}.png",  # Nome da foto baseado no nome do vendedor
            "faturamento": f"R$ {row['Faturamento']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            "volume": str(int(row['Volume'])),
            "positivacoes": str(int(row['PDVs']))
        })

    # 5. Estruturar o objeto JSON
    dados_dashboard = {
        "kpis": {
            "faturamentoAcumulado": f"R$ {faturamento_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
            "faturamentoMeta": "R$ 150.000,00",
            "volumeVendas": f"{volume_total:,}".replace(',', '.'),
            "volumeMeta": "8.500",
            "pdvsAtivados": str(pdvs_totais),
            "pdvsMeta": "400"
        },
        "podio": {
            "primeiro": {
                "nome": p1_nome,
                "foto": f"{p1_nome}.png",
                "volume": str(p1_vol),
                "faturamento": p1_fat,
                "positivacoes": str(p1_pdv)
            },
            "segundo": {
                "nome": p2_nome,
                "foto": f"{p2_nome}.png",
                "volume": str(p2_vol),
                "faturamento": p2_fat,
                "positivacoes": str(p2_pdv)
            },
            "terceiro": {
                "nome": "PROMOTOR MERCH",
                "foto": "PROMOTOR.png",
                "volume": "FOTOS",
                "faturamento": "TOP",
                "positivacoes": "1 MANTO"
            }
        },
        "rankingGeral": lista_ranking_geral
    }

    with open('dados.json', 'w+', encoding='utf-8') as f:
        json.dump(dados_dashboard, f, indent=2, ensure_ascii=False)
        
    print("Sucesso! O arquivo 'dados.json' foi atualizado com as fotos do ranking.")

if __name__ == "__main__":
    converter_excel_para_json()