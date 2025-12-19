from luo_kps_peli import luo_peli


def main():
    while True:
        print(
            "Valitse pelataanko"
            "\n (a) Ihmistä vastaan"
            "\n (b) Tekoälyä vastaan"
            "\n (c) Parannettua tekoälyä vastaan"
            "\nMuilla valinnoilla lopetetaan"
        )

        vastaus = input()

        if vastaus not in ["a", "b", "c"]:
            break

        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )

        kps_peli = luo_peli(vastaus)
        kps_peli.pelaa()


if __name__ == "__main__":
    main()
