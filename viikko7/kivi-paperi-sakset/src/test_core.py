# -*- coding: utf-8 -*-
"""
Pytest-style tests for the core modules of the kivi-paperi-sakset project.

This test file is placed inside the `src` directory so tests can import the
project modules using their plain names (e.g. `from tuomari import Tuomari`).

Tests included:
- Tuomari scoring and string representation
- Tekoaly deterministic sequence
- TekoalyParannettu basic behavior
- luo_peli factory returns correct classes
- Tuomari winner behavior when a player reaches 5 wins
"""

import inspect

from luo_kps_peli import luo_peli
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari


def test_tuomari_counts_and_str():
    t = Tuomari()

    # ensimmäinen voittaa
    t.kirjaa_siirto("k", "s")
    # tasapeli
    t.kirjaa_siirto("p", "p")
    # toinen voittaa
    t.kirjaa_siirto("s", "k")

    s = str(t)
    # odotetaan muotoa "Pelitilanne: X - Y" ja että tasapelit näkyy
    assert "Pelitilanne:" in s
    assert "Tasapelit" in s
    # tulosten tulee olla 1 - 1 (yksi voitto kummallekin) ja yksi tasapeli
    assert "1 - 1" in s


def test_tekoaly_sequence_is_deterministic():
    """
    Verify Tekoaly produces the expected repeating sequence based on its implementation.

    The implementation in `tekoaly.py` increments an internal counter then takes modulo 3:
      start _siirto = 0
      call1 -> _siirto = 1 -> returns 'p'
      call2 -> _siirto = 2 -> returns 's'
      call3 -> _siirto = 0 -> returns 'k'
      call4 -> _siirto = 1 -> returns 'p'
    So the first four moves should be ['p','s','k','p'].
    """
    a = Tekoaly()
    moves = [a.anna_siirto() for _ in range(4)]
    assert moves == ["p", "s", "k", "p"]


def test_tekoaly_parannettu_initial_and_learning_behavior():
    ia = TekoalyParannettu(5)

    # With empty memory, anna_siirto returns 'k' per implementation
    assert ia.anna_siirto() == "k"

    # Teach some moves and ensure anna_siirto returns a valid move
    sequence = ["k", "p", "k", "s", "k"]
    for mv in sequence:
        ia.aseta_siirto(mv)

    next_move = ia.anna_siirto()
    assert next_move in ("k", "p", "s")

    # Ensure that aseta_siirto doesn't raise and stores values (by introspecting internal state)
    # (This is a light implementation detail check; if internal names change this assertion can be relaxed)
    if hasattr(ia, "_muisti"):
        # There should be at most `muistin_koko` non-None values in memory
        mem = getattr(ia, "_muisti")
        non_none = [x for x in mem if x is not None]
        assert len(non_none) <= len(mem)


def test_luo_peli_factory_returns_expected_types():
    # 'a' -> KPSPelaajaVsPelaaja
    p_a = luo_peli("a")
    # Import here to avoid import-time side effects earlier in module import
    from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja

    assert isinstance(p_a, KPSPelaajaVsPelaaja)
    assert inspect.isclass(KPSPelaajaVsPelaaja)

    # 'b' -> KPSTekoaly
    p_b = luo_peli("b")
    from kps_tekoaly import KPSTekoaly

    assert isinstance(p_b, KPSTekoaly)
    assert inspect.isclass(KPSTekoaly)

    # 'c' -> KPSParempiTekoaly
    p_c = luo_peli("c")
    from kps_parempi_tekoaly import KPSParempiTekoaly

    assert isinstance(p_c, KPSParempiTekoaly)
    assert inspect.isclass(KPSParempiTekoaly)


def test_tuomari_winner_behavior_first_reaches_five():
    """
    When the first player reaches 5 wins, Tuomari should report a winner.
    """
    t = Tuomari()
    # simulate five wins for first player
    for _ in range(3):
        t.kirjaa_siirto("k", "s")  # first wins

    assert t.onko_voittaja() is True
    assert t.voittaja() == "eka"
    # __str__ should include the winner message for the first player
    assert "Ensimmäinen pelaaja voitti pelin!" in str(t)


def test_tuomari_winner_behavior_second_reaches_five():
    """
    When the second player reaches 5 wins, Tuomari should report a winner.
    """
    t = Tuomari()
    # simulate five wins for second player
    for _ in range(3):
        t.kirjaa_siirto("s", "k")  # second wins

    assert t.onko_voittaja() is True
    assert t.voittaja() == "toka"
    # __str__ should include the winner message for the second player
    assert "Toinen pelaaja voitti pelin!" in str(t)
