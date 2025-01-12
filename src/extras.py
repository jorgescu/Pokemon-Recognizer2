# src/extras.py

import folium
import pandas as pd
from folium.plugins import MarkerCluster
import random
import tempfile
import os

class ExtrasManager:
    def __init__(self, df):
        self.df = df
        # Definir coordenadas base para cada generación (ficticias)
        self.generation_coordinates = {
            1: {"lat": 35.6895, "lon": 139.6917},  # Tokyo, Japón
            2: {"lat": 34.0522, "lon": -118.2437},  # Los Ángeles, USA
            3: {"lat": 51.5074, "lon": -0.1278},  # Londres, Reino Unido
            4: {"lat": 48.8566, "lon": 2.3522},  # París, Francia
            5: {"lat": 40.7128, "lon": -74.0060},  # Nueva York, USA
            6: {"lat": 55.7558, "lon": 37.6173},  # Moscú, Rusia
            7: {"lat": -33.8688, "lon": 151.2093},  # Sídney, Australia
            8: {"lat": 19.4326, "lon": -99.1332},  # Ciudad de México, México
            # Añadir más generaciones si es necesario
        }

    def get_habitat_map(self, pokedex_number):
        # Filtrar el Pokémon por número de Pokédex
        poke_data = self.df[self.df['pokedex_number'] == pokedex_number]
        if poke_data.empty:
            raise ValueError(f"No se encontró el Pokémon con número de Pokédex {pokedex_number}.")

        poke_data = poke_data.iloc[0]

        generation = poke_data['generation']
        name = poke_data['name']
        ptype1 = poke_data['type1']
        ptype2 = poke_data['type2'] if pd.notna(poke_data['type2']) else "N/A"
        classification = poke_data['classfication']
        height = poke_data['height_m']
        weight = poke_data['weight_kg']
        is_legendary = poke_data['is_legendary']

        # Obtener coordenadas base según generación
        if generation in self.generation_coordinates:
            base_lat = self.generation_coordinates[generation]['lat']
            base_lon = self.generation_coordinates[generation]['lon']
        else:
            # Coordenadas aleatorias si la generación no está definida
            base_lat = random.uniform(-90, 90)
            base_lon = random.uniform(-180, 180)

        # Simular múltiples hábitats por Pokémon
        num_habitats = random.randint(1, 3)  # 1 a 3 hábitats
        habitat_coords = []
        for _ in range(num_habitats):
            # Desplazamiento aleatorio para simular diferentes hábitats
            lat_offset = random.uniform(-5, 5)
            lon_offset = random.uniform(-5, 5)
            habitat_coords.append((base_lat + lat_offset, base_lon + lon_offset))

        # Crear el mapa centrado en la primera ubicación
        m = folium.Map(location=habitat_coords[0], zoom_start=5, tiles='OpenStreetMap', control_scale=True)

        # Añadir un cluster de marcadores para mayor eficiencia
        marker_cluster = MarkerCluster().add_to(m)

        for idx, (lat, lon) in enumerate(habitat_coords, start=1):
            popup_content = f"""
            <b>{name} (N.° {pokedex_number})</b><br>
            <b>Tipo:</b> {ptype1} / {ptype2}<br>
            <b>Clasificación:</b> {classification}<br>
            <b>Altura:</b> {height} m<br>
            <b>Peso:</b> {weight} kg<br>
            <b>Legendario:</b> {"Sí" if is_legendary else "No"}<br>
            <b>Hábitat {idx}:</b> Latitud {lat:.4f}, Longitud {lon:.4f}
            """
            folium.Marker(
                location=(lat, lon),
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='red' if is_legendary else 'blue', icon='info-sign')
            ).add_to(marker_cluster)

        # Añadir capas de tile con atribución adecuada
        folium.TileLayer(
            tiles='Stamen Terrain',
            name='Stamen Terrain',
            attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
        ).add_to(m)

        folium.TileLayer(
            tiles='Stamen Toner',
            name='Stamen Toner',
            attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
        ).add_to(m)

        folium.TileLayer(
            tiles='Stamen Watercolor',
            name='Stamen Watercolor',
            attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
        ).add_to(m)

        # Añadir control de capas
        folium.LayerControl().add_to(m)

        # Guardar el mapa en un archivo HTML temporal
        temp_dir = tempfile.gettempdir()
        map_file = os.path.join(temp_dir, f'pokemon_{pokedex_number}_habitat_map.html')
        m.save(map_file)

        return map_file

    def get_recommendations(self, pokedex_number):
        # Recomendaciones simples: Pokémon con tipo similar
        poke_data = self.df[self.df['pokedex_number'] == pokedex_number].iloc[0]
        same_type = self.df[self.df['type1'] == poke_data['type1']]
        if pd.notna(poke_data['type2']):
            same_type = same_type[same_type['type2'] == poke_data['type2']]
        recommended = same_type.sample(min(5, len(same_type)))['name'].tolist()
        return recommended

    def get_news(self):
        # Noticias falsas (placeholder)
        return [
            " "
        ]
