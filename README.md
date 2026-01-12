🛠 **Projektin osat ja versiot**

**Bittinikkari (Pääversio - bittinikkari-medium.py)**

* Käyttötarkoitus: Täysiverinen projektieditori.
    
**Tärkeimmät ominaisuudet:** 
* .cbp (CodeBlocks) -projektitiedostojen tuki ja XML-pohjainen lukeminen.
* Sivupalkki projektin tiedostojen hallintaan.
* Välilehdet useille tiedostoille.
* Laajennettu työkalupalkki ja kontekstivalikot (oikea hiiren nappi).
* Integroitu LICENSE.txt -lukija (GPLv3).
            
**Bittinikkari Lite (bittinikkari-lite.py)**
    
* Käyttötarkoitus: Kevyt, yhden tiedoston "standalone" -editori.
* Tärkeimmät ominaisuudet:
* Kaikki logiikka yhdessä tiedostossa (ei riippuvuuksia).
* Tummataustainen editori perustoiminnoilla (Avaa/Tallenna).
* Nopea ja varma käynnistys hätämuokkauksiin.
            
✨ **Bittinikkarin hienosäätötoiminnot (Integroituna molempiin)**

* Varmuuskopiot: Automaattinen .bak-tiedoston luonti ennen jokaista tallennusta [cite: 2026-01-05].
* Kevyt muistinhallinta (C-kieli): Ohjelma analysoi koodia ja varoittaa, jos se löytää malloc-kutsun ilman vastaavaa free-kutsua [cite: 2026-01-05].
* Yhden komennon taktiikka: ⚡-painike tai Ctrl+Shift+B suorittaa massahienosäädön (sisennykset, tyhjien välilyöntien poisto ja varmuuskopiointi) koko projektille kerralla [cite: 2026-01-05].
* Lisenssi: Molemmat versiot noudattavat GPL-lisenssiä, mikä mahdollistaa avoimen kehityksen jatkossa [cite: 2026-01-05].
    
📍 **Huomioita jatkoa varten**

* Engine-moduuli: Pääversiossa on varaus erilliselle engine.py-tiedostolle, johon massakorjauslogiikka voidaan keskittää.
* Polut: Muista, että ohjelma etsii oletuksena Bittinikkari.cbp -tiedostoa samasta kansiosta.
* Riippuvuudet: Ohjelma käyttää vain Pythonin vakioalusta (Tkinter), joten se ei vaadi erillisiä asennuksia (pip).
