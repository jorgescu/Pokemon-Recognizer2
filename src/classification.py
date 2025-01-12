import pickle
from sklearn.svm import SVC

class PokemonClassifier:
    def __init__(self, model_path=None, data=None):
        self.model_path = model_path
        self.data = data
        self.model = self._load_model()

    def _load_model(self):
        """
        Carga un modelo SVM. (Aprendizaje automático, Reconocimiento de Patrones).
        """
        try:
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except:
            # Si no existe el modelo, se crea uno vacío.
            return SVC(probability=True)

    def predict(self, features):
        """
        Predice el Pokémon a partir de las características extraídas.
        """
        prediction = self.model.predict([features])[0]
        return prediction
