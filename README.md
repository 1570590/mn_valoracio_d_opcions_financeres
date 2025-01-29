# Mètodes numèrics per a la valoració d’opcions financeres

The study of the valuation of financial options is a fundamental part of financial mathematics for its practical value, since it allows to manage risks and improve decision making in the financial markets. This work focuses on the application of numerical methods to obtain estimates of the value of the options, with special attention to Asian options, characteried by their dependence on an cumulative average. Based on the Black-Scholes model, an adaptation is made to include the specific properties of this type of options. Subsequently, finite differences schemes are implemented, with a detailed analysis of their consistency and stability properties. Finally, the numerical results obtained are presented, analyzing their financial sense and checking the coherence and reliability of the methods used.

---

## Estructura del Projecte

```
mn_valoracio_d_opcions_financeres
> config
>> main.yaml
> data
>> grafics
>>> cn_H
>>> cn_W
>>> explicit_H
>>> explicit_W
> src
>> esquemes
>>> __init__.py
>>> cn_H.py
>>> cn_W.py
>>> explicit_H.py
>>> explicit_W.py
>> grafics
>>> __init__.py
>>> grafic_H_R.py
>>> grafic_H.py
>>> grafic_W_R.py
>>> grafic_W.py
>> __init__.py
>> logger.py
>> main.py
>> utils.py
> .gitignore
> LICENSE
> README.md
> requirements.txt
```

---

## Característiques Clau

### 1. **Disseny Modular:**

   - Cada esquema numèric està implementat a un mòdul, `src/esquemes`.
        - `cn_H` conté l'esquema numèric de Crank-Nicolson per l'equació H.
        - `cn_W` conté l'esquema numèric de Crank-Nicolson per l'equació W.
        - `explicit_H` conté l'esquema numèric explícit per l'equació H.
        - `explicit_W` conté l'esquema numèric explícit per l'equació W.
   - Cada gràfic per a cada equació i tipus de variable està implementat a un mòdul, `src/grafics`.
        - Dins d'una equació i tipus de variable, cada opció i esquema utilitza la mateixa funció per generar un gràfic.
        - Podem trobar un arxiu per cada combinació dels esquemes vists al punt anterior. 
   - A l'arxiu `src/` trobem els fitxers
        - `utils.py` amb funcionalitats generals.
        - `logger.py` que defineix la classe del logger.
        - `main.py` que defineix el pipeline principal.
   - Els gràfics per cada esquema numèric, equació i tipus de variable es guarda dins de `data\grafics`
   - A la carpeta `config` trobem la configuració general del pipeline:
        - L'arxiu `main.yaml` defineix la configuració general.

---

### 2. **Execució del Pipeline:**

   - La classe ResolutorEquació a `main.py` orquestra l'execució seqüencial de les diferents equacions, per cada mètode numèric, opció i tipus de variable.
   - Permet l'execució selectiva establint flags, podent executar equacions i mètodes concrets.
---

### 3. **Documentació:**

   - Inline docstrings utilitzant l'estil Numpy.
   - README amb un overview general.

---

### 4. **Dependències:**

   - Totes les llibreries estan llistades a l'arxiu `requirements.txt`.

---

### 5. **Funció Main**
La funció `main.py` permet resoldre equacions diferencials parcials, específicament les equacions H i W, mitjançant els esquemes numèrics explícit i Crank-Nicolson. A més, genera gràfics en 2D i 3D dels resultats i aplica acotacions als intervals de les solucions per obtenir respostes més precises i útils per a la visualització.

#### Components Principals

La funció principal està dissenyada per resoldre equacions utilitzant els següents mòduls:

1. **Equacions H i W**: Es resolen mitjançant els esquemes numèrics explícit i Crank-Nicolson, amb la possibilitat de generar gràfics de les solucions en diferents condicions.
2. **Esquemes Numèrics**: S’utilitzen els esquemes explícits i Crank-Nicolson per resoldre les equacions. Cada esquema té una implementació específica per a l'equació H i W.
3. **Generació de Gràfics**: La funció `_generar_grafic` crea gràfics en 2D i 3D dels resultats, permetent una visualització detallada de les solucions.
4. **Acotació de Solucions**: La funció aplica acotacions a les solucions, millorant la seva estabilitat i comportament numèric.

#### Paràmetres:
- `run_explicit_H`: Si és `True`, executa l'esquema explícit per a l'equació H.
- `run_crank_nicolson_H`: Si és `True`, executa l'esquema Crank-Nicolson per a l'equació H.
- `run_explicit_W`: Si és `True`, executa l'esquema explícit per a l'equació W.
- `run_crank_nicolson_W`: Si és `True`, executa l'esquema Crank-Nicolson per a l'equació W.

#### Exemple d'Execució:

```python
if __name__ == "__main__":
    main(
        run_explicit_H=True,
        run_crank_nicolson_H=True,
        run_explicit_W=True,
        run_crank_nicolson_W=True,
    )
```

En aquest exemple, el programa executarà els esquemes explícit i Crank-Nicolson per a ambdues equacions H i W. Es generaran els gràfics per a cada esquema i equació.

#### Descripció de la Classe `ResolutorEquacio`

La classe `ResolutorEquacio` és la responsable de la resolució numèrica de les equacions. Aquesta classe gestiona els diferents esquemes numèrics i la generació de gràfics. Els atributs principals són:

- **config**: Configuració carregada des d'un fitxer YAML que conté els paràmetres per a la resolució de l'equació.
- **equacio**: Determina si s'ha de resoldre l'equació H o W.
- **run_explicit**: Indica si s'ha d'executar l'esquema explícit.
- **run_crank_nicolson**: Indica si s'ha d'executar l'esquema Crank-Nicolson.

#### Mètodes Principals

- **`resoldre_equacio()`**: Resol l'equació especificada utilitzant els esquemes numèrics i genera els gràfics corresponents.
- **`_resoldre_esquema_numeric()`**: Resol numèricament un esquema específic i genera els gràfics per a l'equació seleccionada.
- **`_generar_grafic()`**: Genera gràfics en 2D i 3D de les solucions obtingudes, aplicant o no acotacions segons la configuració.

#### Exemple d'Execució

```python
config = carregar_configuracio("config/main.yaml")
resolutor_H = ResolutorEquacio(config=config["H_equacio"], equacio="H", run_explicit=True, run_crank_nicolson=True)
resolutor_H.resoldre_equacio()
```

Aquesta instància resoldrà l'equació H utilitzant els esquemes especificats i generarà els gràfics corresponents.

## Instruccions de Setup

### 1. Instal·la les dependències

1. Crea un entorn virtual:
   ```bash
   python -m venv env
   ```
2. Activa l'entorn:
   - Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source env/bin/activate
     ```
3. Instal·la les dependències:
   ```bash
   pip install -r requirements.txt 
   ```
   Si no té instal·lat pip, pot probar amb
      ```bash
   brew install -r requirements.txt 
   ```

### 2. Estableix el Python Path

Abans d'executar el projecte, establiu el `PYTHONPATH`:

```bash
$env:PYTHONPATH="<root_folder>\mn_valoracio_d_opcions_financeres"
```

---

## Com executar-lo

Per a executar totes les equacions i mètodes seqüencialment:

```bash
python src/main.py
```

### Execució Sel·lectiva

Per executar exercicis específics, ajusteu les variables d'entrada al `main.py`:

```python
main(
    run_explicit_H=True,
    run_crank_nicolson_H=True,
    run_explicit_W=True,
    run_crank_nicolson_W=True,
)
```

---

## Llicència

Aquest projecte està llicenciat sota la Llicència MIT.

---

## Contribucions

Considera't lliure de bifurcar aquest repositori i enviar sol·licituds de pull per a millores o correccions.

---

## Reconeixements

- **Treball Final de Grau: *Mètodes numèrics per a la valoració d’opcions financeres* del Grau de Matemàtiques de la UAB.

---

## Contacte

Per a qualsevol dubte, contacteu 1570590uab@gmail.com.
