import os
import tkinter as tk
from src import gui
from src.data_manager import DataManager
from src.classification import PokemonClassifier
from src.description_generation import DescriptionGenerator
from src.fuzzy_logic import FuzzyDangerEvaluator
from src.extras import ExtrasManager
from src.feature_extraction import FeatureExtractor
from src.image_processing import ImagePreprocessor
from src.knowledge_manager import KnowledgeManager
from src.virtual_environment import VirtualEnvironmentIntegrator


def main():
    # Ruta de datos
    data_path = os.path.join("data", "csv", "pokemon.csv")
    images_path = os.path.join("data", "images", "pokemon-images")

    # Carga de datos
    data_mgr = DataManager(data_path)
    df = data_mgr.load_data()

    # Inicialización de componentes
    classifier = PokemonClassifier(model_path="models/svm_model.pkl", data=df)
    extractor = FeatureExtractor()
    preprocessor = ImagePreprocessor()
    danger_evaluator = FuzzyDangerEvaluator()
    desc_generator = DescriptionGenerator(df)
    extras_mgr = ExtrasManager(df)
    knowledge_mgr = KnowledgeManager(df)
    vr_integration = VirtualEnvironmentIntegrator()

    # Construcción de la GUI principal
    root = tk.Tk()
    app = gui.App(
        master=root,
        classifier=classifier,
        extractor=extractor,
        preprocessor=preprocessor,
        danger_evaluator=danger_evaluator,
        desc_generator=desc_generator,
        extras_manager=extras_mgr,
        knowledge_manager=knowledge_mgr,
        vr_integration=vr_integration,
        images_path=images_path,
        df_pokemon=df  # Pasar el DataFrame a la GUI
    )
    app.mainloop()


if __name__ == "__main__":
    main()
