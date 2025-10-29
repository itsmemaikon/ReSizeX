#!/usr/bin/env python3
from PIL import Image, ImageFilter, UnidentifiedImageError
import os, sys

# ====== PADRÕES ======
DEFAULT_MAX_WIDTH = 360
DEFAULT_MAX_HEIGHT = 360
DEFAULT_BG = (255, 255, 255)
DEFAULT_QUALITY = 95
SUPPORTED_OUTPUT = ("jpg", "jpeg", "png", "webp")

def get_resample_filter():
    try:
        return Image.Resampling.LANCZOS
    except AttributeError:
        return getattr(Image, "LANCZOS", Image.BICUBIC)

RESAMPLE = get_resample_filter()

def normalize_ext_list(ext_input):
    """
    Recebe string tipo "png,jpg" ou ".png, .JPG" e retorna lista ['png','jpg'].
    """
    parts = [p.strip().lower().lstrip(".") for p in ext_input.split(",") if p.strip() != ""]
    return list(dict.fromkeys(parts))  # remove duplicatas mantendo ordem

def ask_user_settings():
    # extensões originais
    raw_in = input("Informe a extensão original da imagem (PNG ou JPG): ").strip()
    if raw_in == "":
        orig_exts = ["png"]
    else:
        orig_exts = normalize_ext_list(raw_in)

    # extensão de saída
    raw_out = input(f"Informe a extensão para ser convertida a imagem ({'/'.join(SUPPORTED_OUTPUT)}): ").strip().lower()
    if raw_out == "":
        out_ext = "jpg"
    else:
        out_ext = raw_out.lstrip(".")
    if out_ext not in SUPPORTED_OUTPUT:
        print(f"Extensão '{out_ext}' não suportada. Usando 'jpg'.")
        out_ext = "jpg"

    # dimensões
    try:
        mw = input(f"Informe a largura máxima em px (Padrão {DEFAULT_MAX_WIDTH}): ").strip()
        max_w = int(mw) if mw != "" else DEFAULT_MAX_WIDTH
        if max_w <= 0: raise ValueError()
    except Exception:
        print("Valor inválido para largura — usando padrão.")
        max_w = DEFAULT_MAX_WIDTH

    try:
        mh = input(f"Informe a altura máxima em px (Padrão {DEFAULT_MAX_HEIGHT}): ").strip()
        max_h = int(mh) if mh != "" else DEFAULT_MAX_HEIGHT
        if max_h <= 0: raise ValueError()
    except Exception:
        print("Valor inválido para altura — usando padrão.")
        max_h = DEFAULT_MAX_HEIGHT

    # qualidade
    try:
        qin = input(f"Informe o percentual de qualidade da imagem 1 à 100 (Padrão = {DEFAULT_QUALITY}): ").strip()
        quality = int(qin) if qin != "" else DEFAULT_QUALITY
        if not (1 <= quality <= 100): raise ValueError()
    except Exception:
        print("Valor inválido para qualidade — usando padrão.")
        quality = DEFAULT_QUALITY

    # background para JPEG
    bg_raw = input("Informe a cor de fundo da imagem em RGB (Padrão 255,255,255 aplicável somente de PNG x JPG): ").strip()
    if bg_raw == "":
        bg = DEFAULT_BG
    else:
        try:
            parts = [int(x) for x in bg_raw.split(",")]
            if len(parts) != 3 or not all(0 <= p <= 255 for p in parts):
                raise ValueError()
            bg = tuple(parts)
        except Exception:
            print("Formato inválido para cor — usando branco.")
            bg = DEFAULT_BG

    return {
        "orig_exts": orig_exts,
        "out_ext": out_ext,
        "max_width": max_w,
        "max_height": max_h,
        "quality": quality,
        "background": bg
    }

def resize_image(img, max_width, max_height):
    w, h = img.size
    # ratio = min(max_width / w, max_height / h, 1.0)
    # new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
    new_size = (max_width, max_height)
    if new_size != img.size:
        return img.resize(new_size, RESAMPLE)
    return img

def save_as_output(img, out_path, out_ext, background, quality):
    out_ext = out_ext.lower()
    save_kwargs = {}
    if out_ext in ("jpg", "jpeg"):
        canvas = Image.new("RGB", img.size, background)
        try:
            alpha = img.split()[3]
            canvas.paste(img, mask=alpha)
        except Exception:
            canvas.paste(img.convert("RGB"))
        save_kwargs.update({"format": "JPEG", "quality": quality})
        try:
            canvas.save(out_path, subsampling=0, optimize=True, **save_kwargs)
        except TypeError:
            canvas.save(out_path, **save_kwargs)
        except Exception as e:
            raise e
    elif out_ext == "png":
        # tenta preservar alfa
        try:
            img.save(out_path, format="PNG", optimize=True)
        except Exception:
            img.convert("RGB").save(out_path, format="PNG")
    elif out_ext == "webp":
        save_kwargs.update({"format": "WEBP", "quality": quality})
        try:
            img.save(out_path, **save_kwargs)
        except Exception:
            img.convert("RGB").save(out_path, **save_kwargs)
    else:
        raise ValueError("Extensão de saída não suportada.")

def process_folder(folder, orig_exts, out_ext, max_w, max_h, background, quality):
    output_dir = os.path.join(folder, "output")
    os.makedirs(output_dir, exist_ok=True)

    files = sorted(os.listdir(folder))
    count = 0
    orig_set = set([e.lower() for e in orig_exts])

    for file in files:
        full = os.path.join(folder, file)
        if os.path.isdir(full):
            continue
        name, ext = os.path.splitext(file)
        if ext == "":
            continue
        ext_clean = ext.lstrip(".").lower()
        if ext_clean not in orig_set:
            continue

        try:
            img = Image.open(full).convert("RGBA")
        except UnidentifiedImageError:
            print(f"⚠ Arquivo não é imagem válida: {file}")
            continue
        except Exception as e:
            print(f"⚠ Erro abrindo {file}: {e}")
            continue

        img = resize_image(img, max_w, max_h)
        # aplica leve nitidez
        try:
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        except Exception:
            pass

        out_name = f"{name}.{out_ext}"
        out_path = os.path.join(output_dir, out_name)
        try:
            save_as_output(img, out_path, out_ext, background, quality)
            count += 1
            print(f"✔ {file} → output/{out_name}")
        except Exception as e:
            print(f"✖ Falha salvando {out_name}: {e}")

    if count == 0:
        print("Nenhum arquivo com as extensões informadas encontrado na pasta.")
    else:
        print(f"\n✅ {count} arquivo(s) processado(s). Salvos em: {output_dir}")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        current_folder = os.path.dirname(sys.executable)
    else:
        current_folder = os.path.dirname(os.path.abspath(__file__))

    print("=== ReSizeX | Utilitário leve em Python para redimensionamento e conversão de imagens ===")
    settings = ask_user_settings()
    print(f"Processando: {current_folder}")
    print(f"Entradas: {', '.join(settings['orig_exts'])} → Saída: .{settings['out_ext']} | Max: {settings['max_width']}x{settings['max_height']} | Qualidade: {settings['quality']}")
    process_folder(current_folder,
                   settings['orig_exts'],
                   settings['out_ext'],
                   settings['max_width'],
                   settings['max_height'],
                   settings['background'],
                   settings['quality'])
