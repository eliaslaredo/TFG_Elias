# TFG Elias Laredo Fernández

## Ingeniería de Sonido e Imagen
## UC3M - 2025/2026
### Distribuido bajo licencia GNU General Public License

¡Bienvenid@ al respositorio de mi TFG!

Aquí encontrarás el análisis de datos relativo al ensayo de 36 baterías de litio 13300 extraídas de vapeadores desechables. Los ensayos realizados son:

-Ciclado: Se sometieron a un ciclo de carga completa, descarga y carga.
    Objetivo: Obtener el estado de salud (SoH) de cada batería

-Espectroscopia de Impedancia Electroquímica:
    Objetivo: Obtener detalladamente la impedancia interna de cada batería.

## Estructura de carpetas

- data/ : Aquí se puede encontrar todos los datos utilizados para el análisis

    - raw/ : Datos sin modificar, tal cual fueron obtenidos
        - cicladores/ : Contiene la información extraída de los cicladores
        - eis/ : Contiene los archivos obtenidos del EIS
        - baterías.xlsx : Hoja de cálculo creada manualmente durante los ensayos para facilitar las correspondencias de archivos generados con cada batería individual.
    - processed/ : Datos filtrados, modificados y adaptados para facilitar el análisis.
        - cicladores/ : Contiene los archivos de los cicladores modifcados y adaptados
        - baterias/ : Contiene el archivo .txt proveniente de la última carga del ciclador correspondiente a cada una de las baterías.

- Capturas/ : Capturas de pantalla conteniendo la información de configuración de los diferentes ensayos.
- procesado_ciclados.ipynb : Cuaderno de Jupyter conteniendo los scripts de Python utilizados en el análisis.

