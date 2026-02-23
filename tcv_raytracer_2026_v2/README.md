# tcv_raytracer_2026  –  Solucao completa das tarefas

## Setup (igual ao original)
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Renderizar cada tarefa

```bash
# Tarefa 1 – Cubo e Cilindro
python raster.py -s scene_task1 -n 4 -j 4 -o task1.png

# Tarefa 2 – ObjectTransform (paraboloide, cubo rotacionado, cilindro inclinado)
python raster.py -s scene_task2 -n 4 -j 4 -o task2.png

# Tarefa 3 – Superficies implicitas Mitchell + Coracao  (mais lento!)
python raster.py -s scene_task3 -n 2 -j 4 -o task3.png

# Tarefa 4 – Espelhos (varie max_depth dentro de scene_task4.py)
python raster.py -s scene_task4 -n 4 -j 4 -o task4.png

# Tarefa 5 – Profundidade de campo (varie lens_radius em scene_task5.py)
python raster.py -s scene_task5 -n 16 -j 4 -o task5.png
```

## Parametros uteis
- `-n`  amostras por pixel: mais = menos ruido, mais lento
- `-j`  workers paralelos (use o numero de CPUs da sua maquina)

## Arquivos modificados / novos
| Arquivo | O que tem |
|---|---|
| `src/shapes.py` | `Cube`, `Cylinder`, `ObjectTransform`, `ImplicitSurface`, `mitchell_surface()`, `heart_surface()` |
| `src/materials.py` | `MirrorMaterial` (tarefa 4) |
| `src/camera.py` | `ThinLensCamera` (tarefa 5) |
| `scene_task1.py` | Cubo + Cilindro |
| `scene_task2.py` | ObjectTransform com paraboloide, cubo rotacionado, cilindro inclinado |
| `scene_task3.py` | Superficies implicitas Mitchell e Coracao |
| `scene_task4.py` | Dois espelhos opostos |
| `scene_task5.py` | Depth of Field com fileira de esferas |
