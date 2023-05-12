# Y2_2023_84433: Srategiapeli "PetWorld"

## Esittely

Projekti on "turn-based strategy game", eli strategiapeli, jossa pelaajan täytyy pelata tekoälyä vastaan. Sekä pelaaja, että tietokone ohjaavat joukkoa eläinhahmoja, jotka taistelevat keskenään.
## Tiedosto- ja kansiorakenne

- Code -> sisältää kaikki tarvittavat tiedostot ohjelman suorittamiseen
  - Petworld -> sisältää ohjelmakoodin, sekä kaksi kansiota HUOM: Ohjelma on rakennettu käyttäen luentojen RobotWorld ohjelmaa pohjana. Sisältää siis näinollen muiden koodia.
  	- assets -> sisältää pelin hyödyntämiä valokuvatiedostoja
  	- savedata -> sisältää tasotiedostot, sekä pelin tallennukset ja näytönkaappaukset tasoista
- Documentation -> sisältää projektin dokumentaation

## Asennusohje
Ohjelma tarvitsee PyQt6 -kirjaston toimiakseen. Ohjelma ei käytä muita ulkoisia kirjastoja.

## Käyttöohje

Ohjelma voidaan ajaa ajamalla main.py tiedosto.
Peliä pelataan klikkaamalla hahmoja, ja valitsemalla liikkeistä jotka tulevat näkyville.
Pelissä vuoronsa aikana saa liikuttaa kaikkia hahmojaan kerran, sekä tehdä yksi liike (joko hyökkäys, tai itsensä parantaminen).
Kun ei enään pysty tekemään muuta, voi lopettaa vuoronsa painamalla "End turn" -nappia, jolloin vuoro siirtyy tietokoneelle.

Kenttäeditoriin pääsee käsiksi ajamalla level_editor.py. Vaihtoehtoisesti kenttäeditoriin pääsee myös lataamalla level editor graafisen käyttöliittymän kautta.