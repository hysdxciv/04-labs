import os
import tkinter as tk
from tkinter import filedialog
import time

def criar_documentacao_txt(pasta_raiz, arquivo_saida="documentacao_projeto.txt"):
    """Cria documentação estruturada em TXT - Leve e otimizada para IA"""
    
    print(f"📝 Criando documentação TXT para: {pasta_raiz}")
    print(f"💾 Arquivo de saída: {arquivo_saida}")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as doc:
        # Cabeçalho
        doc.write("=" * 80 + "\n")
        doc.write("DOCUMENTAÇÃO DO PROJETO - ESTRUTURA OTIMIZADA PARA IA\n")
        doc.write("=" * 80 + "\n\n")
        
        doc.write(f"PROJETO: {os.path.basename(pasta_raiz)}\n")
        doc.write(f"CAMINHO: {pasta_raiz}\n")
        doc.write(f"DATA: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
        doc.write("\n" + "=" * 80 + "\n\n")
        
        contadores = {
            'pastas': 0,
            'arquivos': 0,
            'arquivos_codigo': 0,
            'linhas_codigo': 0
        }
        
        def processar_pasta(caminho_pasta, nivel=0):
            try:
                itens = sorted(os.listdir(caminho_pasta))
                indentacao = "  " * nivel
                
                for item in itens:
                    caminho_completo = os.path.join(caminho_pasta, item)
                    
                    if os.path.isdir(caminho_completo):
                        # Ignorar pastas do sistema
                        if item in ['.git', '__pycache__', 'venv', 'env', '.idea', '.vscode', 'node_modules']:
                            continue
                        
                        contadores['pastas'] += 1
                        doc.write(f"{indentacao}📁 {item}/\n")
                        
                        # Processar subpastas
                        processar_pasta(caminho_completo, nivel + 1)
                        
                    else:
                        processar_arquivo(caminho_completo, nivel, indentacao)
                        
            except PermissionError:
                doc.write(f"{indentacao}⚠️  [ACESSO NEGADO]\n")
            except Exception as e:
                doc.write(f"{indentacao}❌ [ERRO: {str(e)}]\n")
        
        def processar_arquivo(caminho_arquivo, nivel, indentacao):
            nome_arquivo = os.path.basename(caminho_arquivo)
            extensao = os.path.splitext(nome_arquivo)[1].lower()
            
            # Ignorar arquivos do sistema
            if nome_arquivo in ['.gitignore', '.DS_Store', 'Thumbs.db']:
                return
            
            contadores['arquivos'] += 1
            
            # Extensões de código
            extensoes_codigo = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', 
                              '.php', '.rb', '.go', '.rs', '.ts', '.json', '.xml']
            
            if extensao in extensoes_codigo:
                contadores['arquivos_codigo'] += 1
                doc.write(f"{indentacao}📄 {nome_arquivo}\n")
                adicionar_codigo_resumido(caminho_arquivo, nivel + 1, doc)
            else:
                doc.write(f"{indentacao}📎 {nome_arquivo} [OUTRO]\n")
        
        def adicionar_codigo_resumido(caminho_arquivo, nivel, documento):
            """Adiciona apenas informações essenciais do código"""
            try:
                indentacao = "  " * nivel
                
                # Tentar ler o arquivo
                encodings = ['utf-8', 'latin-1', 'cp1252']
                linhas = None
                
                for encoding in encodings:
                    try:
                        with open(caminho_arquivo, 'r', encoding=encoding) as arquivo:
                            linhas = arquivo.readlines()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if linhas is None:
                    documento.write(f"{indentacao}  ❌ [Não foi possível ler o arquivo]\n")
                    return
                
                # Estatísticas básicas
                total_linhas = len(linhas)
                linhas_codigo = len([l for l in linhas if l.strip() and not l.strip().startswith(('#', '//', '/*', '*', '*/'))])
                contadores['linhas_codigo'] += linhas_codigo
                
                documento.write(f"{indentacao}  📊 Linhas: {total_linhas} (código: ~{linhas_codigo})\n")
                
                # Extrair informações importantes (apenas para arquivos principais)
                if total_linhas < 500:  # Só mostra conteúdo se for pequeno
                    documento.write(f"{indentacao}  ┌─ CÓDIGO ──────────────────────────────────────────────────────────────┐\n")
                    
                    # Mostrar apenas as primeiras 30 linhas e últimas 10
                    if total_linhas <= 40:
                        for i, linha in enumerate(linhas, 1):
                            documento.write(f"{indentacao}  │ {i:3d} │ {linha.rstrip()}\n")
                    else:
                        # Primeiras 20 linhas
                        for i, linha in enumerate(linhas[:20], 1):
                            documento.write(f"{indentacao}  │ {i:3d} │ {linha.rstrip()}\n")
                        documento.write(f"{indentacao}  │ ... [{total_linhas - 40} linhas omitidas] ...\n")
                        # Últimas 20 linhas
                        for i, linha in enumerate(linhas[-20:], total_linhas - 19):
                            documento.write(f"{indentacao}  │ {i:3d} │ {linha.rstrip()}\n")
                    
                    documento.write(f"{indentacao}  └───────────────────────────────────────────────────────────────────────┘\n")
                else:
                    documento.write(f"{indentacao}  📋 [Arquivo muito grande - {total_linhas} linhas - conteúdo omitido]\n")
                
                documento.write(f"{indentacao}\n")
                
            except Exception as e:
                documento.write(f"{indentacao}  ❌ [Erro ao ler: {str(e)}]\n")
        
        # Processar estrutura
        doc.write("ESTRUTURA DO PROJETO:\n")
        doc.write("=" * 50 + "\n")
        processar_pasta(pasta_raiz)
        
        # Resumo final
        doc.write("\n" + "=" * 80 + "\n")
        doc.write("RESUMO ESTATÍSTICO:\n")
        doc.write("=" * 80 + "\n")
        doc.write(f"• Pastas: {contadores['pastas']}\n")
        doc.write(f"• Arquivos totais: {contadores['arquivos']}\n")
        doc.write(f"• Arquivos de código: {contadores['arquivos_codigo']}\n")
        doc.write(f"• Linhas de código estimadas: {contadores['linhas_codigo']}\n")
        doc.write(f"• Outros arquivos: {contadores['arquivos'] - contadores['arquivos_codigo']}\n")
        doc.write("\n" + "=" * 80 + "\n")
        doc.write("DOCUMENTAÇÃO GERADA PARA ANÁLISE DE IA\n")
        doc.write("=" * 80 + "\n")
    
    return arquivo_saida, contadores

def main():
    """Função principal - Versão TXT"""
    print("=== GERADOR DE DOCUMENTAÇÃO TXT PARA IA ===")
    print("Este programa criará uma documentação LEVE e ESTRUTURADA do seu projeto.")
    print()
    
    # Selecionar pasta
    root = tk.Tk()
    root.withdraw()
    pasta_raiz = filedialog.askdirectory(title="Selecione a pasta raiz do projeto")
    
    if not pasta_raiz:
        print("❌ Nenhuma pasta selecionada.")
        return
    
    print(f"✅ Pasta selecionada: {pasta_raiz}")
    
    # Nome do arquivo de saída
    nome_projeto = os.path.basename(pasta_raiz) or "projeto"
    arquivo_saida = f"documentacao_{nome_projeto}.txt"
    
    # Criar documentação
    print("📝 Criando documentação TXT...")
    inicio = time.time()
    
    try:
        arquivo_gerado, estatisticas = criar_documentacao_txt(pasta_raiz, arquivo_saida)
        
        fim = time.time()
        tempo_decorrido = fim - inicio
        
        print(f"✅ Documentação criada com sucesso: {arquivo_gerado}")
        print(f"⏱️  Tempo: {tempo_decorrido:.2f} segundos")
        print(f"📊 Estatísticas:")
        print(f"   • Pastas: {estatisticas['pastas']}")
        print(f"   • Arquivos: {estatisticas['arquivos']}")
        print(f"   • Arquivos de código: {estatisticas['arquivos_codigo']}")
        print(f"   • Linhas de código: {estatisticas['linhas_codigo']}")
        print(f"💾 Tamanho do arquivo: {os.path.getsize(arquivo_gerado)} bytes")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()