import httpx
from tabulate import tabulate
import asyncio

async def buscar_carros(filtros):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1:8000/buscar_carros",
                params={k: v for k, v in filtros.items() if v is not None},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"\n⚠️ Erro na busca: {str(e)}")
        return None

def mostrar_resultados(carros):
    if not carros:
        print("\n❌ Nenhum carro encontrado com os filtros informados")
        return

    tabela = []
    for carro in carros:
        tabela.append([
            carro.get('marca', 'N/A'),
            carro.get('modelo', 'N/A'),
            carro.get('ano', 'N/A'),
            carro.get('cor', 'N/A'),
            f"{carro.get('quilometragem', 0):,} km".replace(",", "."),
            f"R$ {carro.get('preco', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            carro.get('tipo_combustivel', 'N/A')
        ])

    headers = ["Marca", "Modelo", "Ano", "Cor", "Quilometragem", "Preço", "Combustível"]
    print("\n" + tabulate(tabela, headers=headers, tablefmt="grid"))
    print(f"\n✅ {len(carros)} carro(s) encontrado(s)")

async def main_loop():
    while True:
        print("\n" + "="*50)
        print("🔍 AGENTE VIRTUAL DE BUSCA DE CARROS".center(50))
        print("="*50)
        print("\nPreencha os filtros (ou deixe em branco para ignorar)")
        print("Digite 'sair' a qualquer momento para encerrar\n")

        filtros = {}
        campos = [
            ('marca', "Marca: "),
            ('modelo', "Modelo: "),
            ('ano', "Ano: "),
            ('tipo_combustivel', "Tipo de Combustível: "),
            ('preco_min', "Preço Mínimo (R$): "),
            ('preco_max', "Preço Máximo (R$): ")
        ]

        for campo, prompt in campos:
            entrada = input(prompt).strip()
            if entrada.lower() == 'sair':
                print("\n👋 Programa encerrado pelo usuário")
                return
            
            if entrada:
                try:
                    if campo in ['ano']:
                        filtros[campo] = int(entrada)
                    elif campo in ['preco_min', 'preco_max']:
                        filtros[campo] = float(entrada)
                    else:
                        filtros[campo] = entrada
                except ValueError:
                    print(f"⚠️ Valor inválido para {campo}. Use números para ano e preço.")
                    break
        else:
            print("\n⏳ Buscando carros...")
            carros = await buscar_carros(filtros)
            
            if carros is not None:
                mostrar_resultados(carros)
            
            continuar = input("\nDeseja fazer nova busca? (s/n): ").strip().lower()
            if continuar == 'n' or continuar == 'sair':
                print("\n👋 Programa encerrado. Até a próxima!")
                return

async def main():
    try:
        await main_loop()
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())