# Y2_2023_84433: Srategiapeli "PetWorld"

## Checkpoint1

## Tämänhetkiset ominaisuudet

Projekti on "turn-based strategy game", eli strategiapeli, jossa pelaajat tekevät vuoronsa aikana liikkeitä.
Huomio: Ohjelma on rakennettu käyttäen luentojen RobotWorld ohjelmaa pohjana. Tämän vuoksi pelissä on vielä yhtäläisyyksiä ja jäänteitä tästä ohjelmasta.
Pyrin jatkaessani projektia tehdä ohjelmastani aina enemmän omani näköisen, niin että RobotWorldin vaikutteet vähenevät.

Toistaiseksi olen toteuttanut seuraavat ominaisuudet peliin:
- Lemmikkihahmo, jolla on seuraavanlaisia ominaisuuksia:
	- Nimi
	- Tiimi
	- Elämä/Health -pisteet
	- "Movement range", eli kuinka monta ruutua lemmikki pystyy liikkumaan vuoronsa aikana
	- "Attack range", eli kuinka kauas lemmikin hyökkäys yltää
	- Vahvuus, eli kuinka paljon elämää lemmikki vie viholliselta hyökätessään
	- kolme liikettä, joita hahmo voi vuoronsa aikana tehdä "Move", "Attack" ja "Heal"
	- "Character sheet", widgetti, joka näyttää ajankohtaiset yksityiskohdat lemmikin tiedoista
	- "health bar" näyttää kuinka paljon elämää hahmolla on jäljellä
	- "name tag" näyttää lemmikin nimen
	- "context menu" joka näyttää hahmoa klikatessa mahdolliset liikkeet
- Ajastimen, joka näyttää kuinka kauan peli on kestänyt
- Kentän, jossa hahmot voivat liikkua
- Vuoro-, liike- ja status-logiikan, joka pitää huolen siitä, että peliä voidaan pelata vain sääntöjen mukaisesti
- Napin, jota painamalla vuoro vaihtuu. Tällöin myös pelin taustakuva vaihtuu reflektoimaan tiimin väriä, joka on paraikaa vuorossa.

 ## Käyttöohje

Ohjelma on jo käyttökelpoinen tässä vaiheessa. Se voidaan ajaa ajamalla main.py tiedosto.
Peliä pelataan klikkaamalla hahmoja, ja valitsemalla liikkeistä jotka tulevat näkyville.
Pelissä vuoronsa aikana saa liikuttaa kaikkia hahmojaan kerran, sekä tehdä yksi liike (joko hyökkäys, tai itsensä parantaminen).
Kun ei enään pysty tekemään muuta, voi lopettaa vuoronsa painamalla "End turn" -nappia, jolloin vuoro siirtyy toiselle pelaajalle.



 ## Aikataulu

Olen käyttänyt aikaa projektiin tähän mennessä noin 38.75 tuntia, eli olen pysynyt suunnitelmassa odotetun mukaan.
Ei ole ilmennyt vielä muutoksia aikatauluun.

 ## Muuta

Ei ole ilmennyt sen kummempia ongelmia tässä vaiheessa.
En ole joutunut tekemään vielä muutoksia suunnitelmaani.