#   **Reconocedor de Pokémon**

##   **Descripción**

El **Reconocedor de Pokémon** es una aplicación que utiliza técnicas avanzadas de procesamiento de imágenes, algoritmos genéticos, lógica borrosa y aprendizaje automático para identificar Pokémon a partir de imágenes. Además de reconocer al Pokémon, la aplicación proporciona descripciones autogeneradas sobre su tipo, hábitat y peligrosidad.

##   **Tabla de Contenidos**

- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)
- [Agradecimientos](#agradecimientos)
##   **Características**

- **Procesamiento de Imágenes**: Preprocesamiento y segmentación de imágenes para resaltar al Pokémon.
- **Extracción de Características**: Obtención de características relevantes mediante momentos de Hu y descriptores de forma.
- **Clasificación con SVM**: Utilización de Máquinas de Vectores de Soporte para clasificar al Pokémon.
- **Optimización con Algoritmos Genéticos**: Optimización de parámetros del modelo SVM utilizando la biblioteca DEAP.
- **Lógica Borrosa**: Implementación de sistemas difusos para determinar la peligrosidad del Pokémon.
- **Descripciones Autogeneradas**: Generación de descripciones que incluyen tipo, hábitat y peligrosidad.
- **Interfaz Gráfica**: Aplicación GUI desarrollada con Tkinter para cargar imágenes y mostrar resultados.
##   **Requisitos Previos**

Antes de instalar y ejecutar la aplicación, asegúrate de tener lo siguiente:

- **Python 3.8 o superior**
- **Conda**: Se recomienda utilizar un entorno virtual de conda.
- **Paquetes de Python**: Las dependencias están listadas en ` requirements.txt `.
##   **Instalación**

***1. Clonar el Repositorio***

 ```bash
    git clone https://github.com/tu_usuario/proyecto_pokemon.git cd proyecto_pokemon
 ```
***2. Crear y Activar el Entorno Virtual***

 ```bash
    conda create --name pokemon_env python=3.8 conda activate pokemon_env
 ```
***3. Instalar las Dependencias***

 ```bash
    pip install -r requirements.txt
 ```

***4. Configurar el Dataset***

**Dataset de Imágenes**: Asegúrate de tener el conjunto de imágenes de Pokémon organizado en carpetas por etiqueta dentro de ` data/raw/ `.

**Diccionarios de Tipos y Hábitats**: Verifica que los archivos necesarios para tipos y hábitats estén presentes en ` data/processed/ ` o en la ruta especificada en el código.
##   **Uso**

***Ejecutar la Aplicación***

Para iniciar la interfaz gráfica de usuario:

 ```bash
    python main.py
 ```

***Funcionalidades de la Aplicación***

- **Cargar Imagen**: Haz clic en el botón " Cargar Imagen " y selecciona una imagen de un Pokémon.
- **Procesamiento y Clasificación**: La aplicación procesará la imagen, extraerá características y clasificará al Pokémon.
- **Mostrar Resultados**:
- **Imagen Procesada**: Se mostrará la imagen procesada en la interfaz.
- **Descripción**: Se mostrará una descripción autogenerada que incluye el nombre, tipo, hábitat y peligrosidad del Pokémon.
##   **Estructura del Proyecto**

 ``` 
 proyecto_pokemon/
│
├── src/
│   ├── __init__.py
│   ├── preprocesamiento.py
│   ├── segmentacion.py
│   ├── caracteristicas.py
│   ├── clasificacion.py
│   ├── optimizacion.py
│   ├── logica_borrosa.py
│   ├── descripciones.py
│   └── interfaz.py
│
├── data/
│   ├── raw/                 # Imágenes originales
│   ├── processed/           # Imágenes y datos procesados
│   └── models/              # Modelos entrenados
│
├── notebooks/               # Cuadernos Jupyter para exploración
│   └── exploracion.ipynb
│
├── requirements.txt         # Dependencias del proyecto
├── main.py                  # Script principal
├── README.md                # Descripción del proyecto
└── .gitignore               # Archivos y carpetas ignorados en Git
```

##   **Contribuciones**

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

**Haz un Fork** del repositorio.
Crea una **rama** para tu funcionalidad o corrección de errores (` git checkout -b feature/nueva-funcion `).
**Confirma** tus cambios (` git commit -m 'Agrega nueva función' `).
**Envía** a la rama (` git push origin feature/nueva-funcion `).
Abre un **Pull Request**.
##   **Licencia**

Este proyecto está licenciado bajo la **Licencia MIT**. Consulta el archivo [ LICENSE ] para obtener más detalles.

##   **Contacto**

- **Autor**: Tu Nombre
- **Correo Electrónico**: tuemail@example.com
- **LinkedIn**: [ Tu Perfil ]( https://www.linkedin.com/in/tuperfil )
##   **Agradecimientos**

- **Bibliotecas y Herramientas**: Agradecimiento a las bibliotecas de código abierto utilizadas en este proyecto, como OpenCV, scikit-learn, DEAP, scikit-fuzzy, entre otras.
- **Inspiración**: Este proyecto se inspiró en la combinación de técnicas de inteligencia artificial y procesamiento de imágenes para crear una aplicación educativa y entretenida.