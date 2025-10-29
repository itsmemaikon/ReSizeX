# 🖼️ ReSizeX

**ReSizeX** é um utilitário leve desenvolvido em **Python** para redimensionamento e conversão em lote de imagens.  
Com interface simples em linha de comando, permite ajustar dimensões fixas, converter formatos e aplicar nitidez, tudo de forma automatizada e rápida.

---

## 🚀 Funcionalidades

- 🔧 **Redimensionamento direto** — ajusta todas as imagens para largura e altura definidas, sem preservar proporção.  
- 🧩 **Conversão entre formatos** — suporta entrada em `JPG`, `PNG` e saída em `JPG`, `PNG`, `WEBP`.  
- 🎨 **Controle de fundo RGB** — define cor de fundo para conversões de imagens com transparência para `JPG`.  
- 💎 **Ajuste de qualidade** — permite definir compressão de 1 a 100%.  
- ⚙️ **Processamento em lote** — percorre automaticamente todos os arquivos da pasta atual.  
- 🪶 **Nitidez automática** — aplica leve filtro de *Unsharp Mask* nas imagens processadas.  
- 💾 **Organização automática** — resultados são salvos na subpasta `./output/`.  

---

## 📦 Requisitos

- Python **3.8+**  
- Biblioteca **Pillow**

Instale executando:
```bash pip install pillow```

## 🧭 Como usar

1. Coloque o arquivo resizex.py na pasta contendo as imagens.

2. Execute o script:
```python resizex.py```

3. Informe as opções solicitadas no console:
	- Extensão original (png, jpg, etc.)
	- Formato de saída (jpg, png, webp)
	- Largura e altura máximas
	- Qualidade da imagem (1–100)
	- Cor de fundo RGB (opcional)
	- Após o processamento, os arquivos redimensionados estarão em ./output/
	
## 🪪 Licença

Distribuído sob a licença MIT — uso livre, sem garantias.	
