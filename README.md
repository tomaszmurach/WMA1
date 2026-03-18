# LAB1 – Detekcja i śledzenie czerwonego obiektu w wideo

Projekt z wykorzystaniem **OpenCV** i **NumPy**, którego celem jest detekcja oraz śledzenie czerwonego obiektu w nagraniu wideo.  
Pozycja obiektu wyznaczana jest na podstawie **momentów geometrycznych** obliczanych z binarnej maski koloru czerwonego.

## Funkcjonalności

- wczytywanie pliku wideo z parametru uruchomieniowego `--video`
- detekcja czerwonego obiektu w przestrzeni barw **HSV**
- uwzględnienie dwóch zakresów czerwieni (ze względu na zawijanie Hue w HSV)
- czyszczenie maski operacjami morfologicznymi:
  - **OPEN** – usuwanie drobnych szumów
  - **CLOSE** – zamykanie dziur w obiekcie
- wyznaczanie środka obiektu z **momentów**
- wizualizacja:
  - okrąg obejmujący wykryty obiekt
  - zaznaczenie środka obiektu
  - pionowa linia środka kadru
  - paski pokazujące odchylenie obiektu od środka obrazu
- dwa okna podglądu:
  - obraz oryginalny z oznaczeniami
  - obraz przetworzony (maska po segmentacji i morfologii)

## Wymagania

Projekt został napisany w **Python 3**.

Wymagane biblioteki:
- `opencv-python`
- `numpy`

## Instalacja

Zainstaluj wymagane pakiety poleceniem:

```bash
pip install opencv-python numpy
```

Uruchomienie

```bash
python main.py --video sample.mp4
```

Można także ustawić minimalne pole wykrywanego obiektu:

```bash
python main.py --video sample.mp4 --min-pole 300
```

## Parametry

- `--video` – ścieżka do pliku wideo (wymagany parametr)
- `--min-pole` – minimalne pole obiektu w pikselach, poniżej którego obiekt jest ignorowany

## Jak działa program

1. Program wczytuje kolejne klatki z pliku wideo.
2. Każda klatka jest konwertowana z przestrzeni **BGR** do **HSV**.
3. Tworzona jest maska dla koloru czerwonego z dwóch zakresów Hue.
4. Maska jest czyszczona przy pomocy operacji morfologicznych **OPEN** i **CLOSE**.
5. Na podstawie maski obliczane są momenty geometryczne.
6. Jeśli pole wykrytego obiektu jest wystarczająco duże:
   - wyznaczany jest środek obiektu
   - szacowany jest promień okręgu na podstawie pola
   - rysowane są elementy wizualizacji na obrazie oryginalnym
7. Program wyświetla dwa okna podglądu aż do końca nagrania lub naciśnięcia `q` / `ESC`.

## Struktura projektu

```text
.
├── main.py
└── README.md
```

## Sterowanie

- `q` – zakończenie programu
- `ESC` – zakończenie programu

## Zastosowane techniki

- segmentacja koloru w przestrzeni **HSV**
- progowanie obrazu przy użyciu `cv2.inRange()`
- operacje morfologiczne:
  - `cv2.MORPH_OPEN`
  - `cv2.MORPH_CLOSE`
- wyznaczanie środka obiektu z wykorzystaniem `cv2.moments()`
- wizualizacja wyników przy pomocy funkcji rysujących OpenCV

Program uruchamia się z poziomu terminala, podając ścieżkę do pliku wideo:
