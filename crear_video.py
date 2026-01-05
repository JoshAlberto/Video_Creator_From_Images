import os
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image

# --- Pedir datos al usuario ---
folder = input("📂 Nombre de la carpeta con las imágenes: ").strip()
duration_input = input("⏱️ Duración por imagen (segundos): ").strip()
resolution_input = input("🖼️ Resolución final (Ej: 1920x540): ").strip()

# Validar duración
try:
    duration = float(duration_input)
except:
    print("❌ Duración inválida.")
    raise SystemExit

# Validar resolución
try:
    width, height = map(int, resolution_input.lower().split("x"))
except:
    print("❌ Resolución inválida. Usa el formato 1920x540")
    raise SystemExit

# Ajustar a valores pares (H.264 lo requiere)
if width % 2 != 0:
    width -= 1
    print(f"ℹ️ Ancho ajustado a valor par: {width}")
if height % 2 != 0:
    height -= 1
    print(f"ℹ️ Alto ajustado a valor par: {height}")

# Verificar carpeta
if not os.path.isdir(folder):
    print("❌ La carpeta no existe.")
    raise SystemExit

# --- Buscar imágenes ---
files = sorted(
    [f for f in os.listdir(folder)
     if f.lower().startswith("imagen") and f.lower().endswith((".png", ".jpg", ".jpeg"))],
    key=lambda x: int("".join(filter(str.isdigit, x)))
)

if not files:
    print("❌ No hay imágenes tipo Imagen1, Imagen2,...")
    raise SystemExit

print("\n📷 Imágenes encontradas (orden):")
for f in files:
    print("   -", f)

# --- Preparar carpeta temporal escalada ---
scaled_folder_name = f"scaled_tmp_{width}x{height}"
scaled_dir = os.path.join(folder, scaled_folder_name)
os.makedirs(scaled_dir, exist_ok=True)

# Elegir modo de reescalado compatible con Pillow moderno
if hasattr(Image, "Resampling"):
    RESAMPLE = Image.Resampling.LANCZOS
else:
    RESAMPLE = Image.LANCZOS

print(f"\n🖼️ Reescalando todas las imágenes a {width}x{height} (estirando)...")

scaled_files = []
for f in files:
    src_path = os.path.join(folder, f)
    dst_path = os.path.join(scaled_dir, f"{os.path.splitext(f)[0]}_scaled.png")

    img = Image.open(src_path).convert("RGB")
    img = img.resize((width, height), RESAMPLE)
    img.save(dst_path, format="PNG")

    scaled_files.append(dst_path)
    print(f"   ✔️ {f} -> {os.path.basename(dst_path)}")

# --- Crear clips ---
clips = []
for path in scaled_files:
    clip = ImageClip(path).set_duration(duration)
    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")

# --- Exportar a MP4 con resolución incluida ---
mp4_filename = f"video_final_{width}x{height}.mp4"
mp4_path = os.path.join(folder, mp4_filename)

print(f"\n🎬 Generando MP4 final {mp4_filename} ...")
video.write_videofile(
    mp4_path,
    fps=1,
    codec="libx264",
    audio=False
)

print(f"\n✅ Vídeo final creado en: {mp4_path}")
print(f"📁 Carpeta de trabajo creada: {scaled_dir}")
print("ℹ️ Puedes borrar la carpeta auxiliar cuando ya no la necesites.")
print("🎉 ¡Imágenes escaladas exactamente y vídeo uniforme sin barras!")
