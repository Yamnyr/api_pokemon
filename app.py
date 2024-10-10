import streamlit as st
from pokemon_api import get_pokemon_stats, compare_pokemons, simulate_battle, get_fire_pokemon_average_hp

if __name__ == "__main__":
    st.title("TP Pokémon Api")

    menu = st.sidebar.selectbox("Choisissez une option",
                                 ["Afficher les statistiques d'un Pokémon",
                                  "Comparer deux Pokémon",
                                  "Simuler un combat entre deux Pokémon",
                                  "Moyenne des points de vie des Pokémon de type 'fire'"])

    if menu == "Afficher les statistiques d'un Pokémon":
        pokemon_name = st.text_input("Entrez le nom d'un Pokémon:")
        if st.button("Afficher les statistiques"):
            if not pokemon_name:
                st.error("Veuillez entrer un nom de Pokémon.")
            else:
                stats = get_pokemon_stats(pokemon_name)
                if stats:
                    st.markdown("### Statistiques de Pokémon")
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.image(stats['image_url'], caption=stats['name'].capitalize(), width=150)

                    with col2:
                        st.write(f"**Nom:** {stats['name'].capitalize()}")
                        st.write(f"**HP:** {stats['hp']}")
                        st.write(f"**Attaque:** {stats['attack']}")
                        st.write(f"**Défense:** {stats['defense']}")
                        st.write(f"**Vitesse:** {stats['speed']}")
                        st.write(f"**Types:** {', '.join(stats['types'])}")

    elif menu == "Comparer deux Pokémon":
        pokemon1_name = st.text_input("Entrez le nom du premier Pokémon:")
        pokemon2_name = st.text_input("Entrez le nom du deuxième Pokémon:")
        if st.button("Comparer"):
            if not pokemon1_name or not pokemon2_name:
                st.error("Veuillez entrer les noms des deux Pokémon.")
            else:
                compare_pokemons(pokemon1_name, pokemon2_name)

    elif menu == "Simuler un combat entre deux Pokémon":
        pokemon1_name = st.text_input("Entrez le nom du premier Pokémon pour le combat:")
        pokemon2_name = st.text_input("Entrez le nom du deuxième Pokémon pour le combat:")
        if st.button("Simuler le combat"):
            if not pokemon1_name or not pokemon2_name:
                st.error("Veuillez entrer les noms des deux Pokémon pour simuler le combat.")
            else:
                simulate_battle(pokemon1_name, pokemon2_name)

    elif menu == "Moyenne des points de vie des Pokémon de type 'fire'":
        if st.button("Calculer la moyenne"):
            get_fire_pokemon_average_hp()
