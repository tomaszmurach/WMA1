#!/usr/bin/env python3

"""
LAB1: Detekcja kolorów – detekcja i śledzenie czerwonego obiektu w wideo

Zgodnie z treścią zadania:
1) wczytanie pliku wideo jako parametr uruchomieniowy (--video)
2) detekcja i śledzenie obiektu czerwonego, pozycja liczona z MOMENTÓW
3) usuwanie artefaktów (szum, dziury) operacjami morfologicznymi: OPEN i CLOSE
4) dwa okna: oryginalne + przetworzone/progowane
5) na obrazie oryginalnym: okrąg na obiekcie oraz odchylenie lewo/prawo jako paski (bars)

Autor: (wersja referencyjna do LAB)
"""

import argparse
import math
import sys

import cv2
import numpy as np


def buduj_maske_czerwieni(bgr: np.ndarray) -> np.ndarray:
    """Segmentacja czerwieni w HSV + czyszczenie maski (OPEN i CLOSE). Zwraca maskę 0/255."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # Czerwony „zawija się” w HSV -> dwa zakresy Hue
    dolny_zakres1 = np.array([0, 140, 90])
    gorny_zakres1 = np.array([6, 255, 255])

    dolny_zakres2 = np.array([174, 140, 90])
    gorny_zakres2 = np.array([180, 255, 255])

    maska1 = cv2.inRange(hsv, dolny_zakres1, gorny_zakres1)
    maska2 = cv2.inRange(hsv, dolny_zakres2, gorny_zakres2)

    #Połączenie obu masek czerwieni w jedną maskę końcową
    maska = cv2.bitwise_or(maska1, maska2)

    #Jądro operacji morfologicznych
    kernel = np.ones((15, 15), np.uint8)

    # Morfologia: OPEN (erozja->dylatacja) usuwa kropki, CLOSE (dylatacja->erozja)
    maska = cv2.morphologyEx(maska, cv2.MORPH_OPEN, kernel)
    maska = cv2.morphologyEx(maska, cv2.MORPH_CLOSE, kernel)

    return maska


def obiekt_z_momentow(maska_0_255: np.ndarray, min_pole: float = 300.0):
    """
    Liczy momenty bez konturów (założenie: jest tylko jeden czerwony obiekt).
    Zwraca:
      (cx, cy), pole_px, promien_px  albo (None, None, None)
    """

    # Obliczenie momentów geometrycznych z maski binarnej
    momenty = cv2.moments(maska_0_255, binaryImage=True)

    pole = momenty["m00"]
    if pole < min_pole:
        return None, None, None

    cx = int(momenty["m10"] / pole)
    cy = int(momenty["m01"] / pole)


    promien = int(math.sqrt(pole / math.pi))

    return (cx, cy), pole, promien


def rysuj_paski_odchylenia(
    img: np.ndarray,
    cx: int,
    szerokosc: int,
    y: int = 90,
    wysokosc_paska: int = 16,
    margines: int = 10,
):
    """
    Rysuje paski (bars) pokazujące odchylenie lewo/prawo od środka kadru.
    - belka odniesienia: pełna szerokość (w ramce)
    - środek: pionowa kreska
    - wypełnienie: od środka do położenia obiektu (lewo/prawo)
    """
    x_lewo = margines
    x_prawo = szerokosc - margines
    x_srodek = szerokosc // 2

    y_gora = y
    y_dol = y + wysokosc_paska

    #Belka odniesienia
    cv2.rectangle(img, (x_lewo, y_gora), (x_prawo, y_dol), (255, 255, 255), 1)

    #Linia środka
    cv2.line(img, (x_srodek, y_gora), (x_srodek, y_dol), (255, 255, 255), 1)

    # Ograniczenie cx do zakresu belki
    cx_ograniczone = max(x_lewo, min(cx, x_prawo))

    # Wypełnienie od środka do pozycji obiektu
    if cx_ograniczone < x_srodek:
        cv2.rectangle(
            img,
            (cx_ograniczone, y_gora),
            (x_srodek, y_dol),
            (0, 0, 255),
            -1
        )
    elif cx_ograniczone > x_srodek:
        cv2.rectangle(
            img,
            (x_srodek, y_gora),
            (cx_ograniczone, y_dol),
            (0, 0, 255),
            -1
        )

    # Ponowne rysowanie ramki i środka, żeby nie zostały przykryte przez wypełnienie
    cv2.rectangle(img, (x_lewo, y_gora), (x_prawo, y_dol), (255, 255, 255), 1)
    cv2.line(img, (x_srodek, y_gora), (x_srodek, y_dol), (255, 255, 255), 1)



def main() -> int:
    parser = argparse.ArgumentParser(
        description="LAB1: Detekcja czerwonego obiektu (momenty + bars)"
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Ścieżka do pliku wideo, np. sample.mp4",
    )
    parser.add_argument(
        "--min-pole",
        type=float,
        default=300.0,
        help="Minimalne pole obiektu [px^2]",
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"BŁĄD: Nie można otworzyć pliku wideo: {args.video}", file=sys.stderr)
        return 1

    fps = cap.get(cv2.CAP_PROP_FPS)
    opoznienie_ms = int(1000 / fps) if fps and fps > 1e-3 else 20

    while True:
        ok, klatka = cap.read()
        if not ok:
            break

        h, w = klatka.shape[:2]
        x_srodek = w // 2

        maska = buduj_maske_czerwieni(klatka)
        centrum, pole, promien = obiekt_z_momentow(maska, min_pole=args.min_pole)

        # Okno 2: przetworzone i progowane (maska)
        cv2.imshow("Obraz przetworzony (maska po HSV + morfologia)", maska)

        # Okno 1: oryginał + oznaczenia
        wiz = klatka.copy()

        # Linia środka kadru (pomocniczo)
        cv2.line(wiz, (x_srodek, 0), (x_srodek, h), (255, 255, 255), 1)

        if centrum is not None:
            cx, cy = centrum
            odchylenie = cx - x_srodek

            # Okrąg obejmujący obiekt (promień z pola, założenie: koło)
            cv2.circle(wiz, (cx, cy), max(promien, 1), (0, 0, 255), 2)
            cv2.circle(wiz, (cx, cy), 3, (0, 0, 255), -1)

            # Paski odchylenia (bars)
            rysuj_paski_odchylenia(wiz, cx=cx, szerokosc=w, y=40, wysokosc_paska=16)

        cv2.imshow("Obraz oryginalny (sledzenie + odchylenie)", wiz)

        klawisz = cv2.waitKey(opoznienie_ms) & 0xFF
        if klawisz in (ord("q"), 27):  # q lub ESC
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())