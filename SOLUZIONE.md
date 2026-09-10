# Soluzione

## Come far partire tutto

Ho lavorato su Windows 10 con PowerShell: i comandi del README sono per bash e cambiano
solo nell'attivazione del venv.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
pytest -v
```

Il frontend è invariato rispetto a `frontend/README.md`.

---

## Domande

### Sul codice che ho scritto

**1. `generate_board()`: scarta-e-riprova o mosse casuali da GOAL?**

_(da scrivere)_

**2. Perché metà delle disposizioni non è risolvibile?**

_(da scrivere)_

**3. Come ho trovato il bug del TODO(1)**

`pytest -v` dava `assert [3, 4, 5] == [3, 4]`: `movable_tiles` restituiva una tessera in
più, il 5. Ho letto il codice a strati, come una matrioska: `movable_tiles` si limita a
tradurre indici in tessere, `blank_index` è un `.index(0)`, quindi l'unico posto con della
logica vera era `neighbors`.

Ho disegnato la griglia 4x4 sulla whiteboard con gli indici da 0 a 15. Il vuoto sta
all'indice 3, fine della prima riga; `+1` dà 4, che nella lista è il numero successivo ma
sulla griglia è l'inizio della seconda riga. Il controllo `0 <= candidate < 16` non se ne
accorge perché 4 è un indice valido: il problema non è uscire dalla lista, è scavalcare il
bordo della riga restando dentro la lista.

Da lì ho cercato una regola valida per ogni cella, non solo per l'esempio. Prima ho provato
a calcolare gli estremi della riga (`riga * SIZE` ecc.), poi mi sono accorto che
`index % SIZE` dà direttamente la colonna ed è più semplice. Il fix: dalla colonna 0 non si
va a `-1`, dalla colonna 3 non si va a `+1`. I passi verticali non hanno bisogno di niente
perché restano nella stessa colonna: possono solo uscire dalla lista, e lì il controllo
esistente basta.

Per provarlo: il test rosso è verde, i tre test verdi che dipendono da `neighbors` lo sono
rimasti, e ho aggiunto `tests/test_neighbors.py` che controlla tutte e 16 le celle. Ho
verificato che 6 di quei test diventino rossi se rimetto la versione buggata: un test che
non si accorge del bug non serve.

**4. `apply_move()` restituisce una nuova board: che differenza fa?**

_(da scrivere)_

### Sulle scelte di progetto

**5. Classifica: premiare "chi ha giocato meglio"**

_(da scrivere)_

**6. Due processi dietro un load balancer**

_(da scrivere)_

**7. Il frontend chiede le mosse valide al backend**

_(da scrivere)_

**8. Si può barare con questa API?**

_(da scrivere)_

### Per chiudere

**9. Cosa ho lasciato indietro**

_(da scrivere)_

**10. Qualcosa di sbagliato o poco chiaro nella traccia?**

_(da scrivere)_
