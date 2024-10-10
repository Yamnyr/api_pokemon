import requests
import streamlit as st
import time

def get_pokemon_stats(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Erreur : Pokémon non trouvé.")
        return None

    data = response.json()
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}

    image_url = data['sprites']['front_default']

    return {
        'name': data['name'],
        'hp': stats.get('hp'),
        'attack': stats.get('attack'),
        'defense': stats.get('defense'),
        'speed': stats.get('speed'),
        'types': [t['type']['name'] for t in data['types']],
        'image_url': image_url
    }

def display_pokemon_stats(pokemon1, pokemon2):
    col1, col2 = st.columns(2)

    with col1:
        subcol1, subcol2 = st.columns([1, 2])
        with subcol1:
            st.image(pokemon1['image_url'], caption=pokemon1['name'].capitalize(), width=150)
        with subcol2:
            st.write(f"**Nom:** {pokemon1['name'].capitalize()}")
            st.write(f"**HP:** {pokemon1['hp']}")
            st.write(f"**Attaque:** {pokemon1['attack']}")
            st.write(f"**Défense:** {pokemon1['defense']}")
            st.write(f"**Vitesse:** {pokemon1['speed']}")
            st.write(f"**Types:** {', '.join(pokemon1['types'])}")

    with col2:
        subcol1, subcol2 = st.columns([1, 2])
        with subcol1:
            st.image(pokemon2['image_url'], caption=pokemon2['name'].capitalize(), width=150)
        with subcol2:
            st.write(f"**Nom:** {pokemon2['name'].capitalize()}")
            st.write(f"**HP:** {pokemon2['hp']}")
            st.write(f"**Attaque:** {pokemon2['attack']}")
            st.write(f"**Défense:** {pokemon2['defense']}")
            st.write(f"**Vitesse:** {pokemon2['speed']}")
            st.write(f"**Types:** {', '.join(pokemon2['types'])}")

def compare_pokemons(pokemon1_name, pokemon2_name):
    pokemon1 = get_pokemon_stats(pokemon1_name)
    pokemon2 = get_pokemon_stats(pokemon2_name)

    if pokemon1 and pokemon2:
        st.subheader("Comparaison des Pokémon")
        display_pokemon_stats(pokemon1, pokemon2)

        if pokemon1['hp'] > pokemon2['hp']:
            st.success(f"{pokemon1['name'].capitalize()} a plus de points de vie que {pokemon2['name'].capitalize()}.")
        elif pokemon1['hp'] < pokemon2['hp']:
            st.success(f"{pokemon2['name'].capitalize()} a plus de points de vie que {pokemon1['name'].capitalize()}.")
        else:
            st.success(f"{pokemon1['name'].capitalize()} et {pokemon2['name'].capitalize()} ont le même nombre de points de vie.")

        if pokemon1['attack'] > pokemon2['attack']:
            st.success(f"{pokemon1['name'].capitalize()} a une attaque plus élevée que {pokemon2['name'].capitalize()}.")
        elif pokemon1['attack'] < pokemon2['attack']:
            st.success(f"{pokemon2['name'].capitalize()} a une attaque plus élevée que {pokemon1['name'].capitalize()}.")
        else:
            st.success(f"{pokemon1['name'].capitalize()} et {pokemon2['name'].capitalize()} ont la même attaque.")

        if pokemon1['defense'] > pokemon2['defense']:
            st.success(f"{pokemon1['name'].capitalize()} a une défense plus élevée que {pokemon2['name'].capitalize()}.")
        elif pokemon1['defense'] < pokemon2['defense']:
            st.success(f"{pokemon2['name'].capitalize()} a une défense plus élevée que {pokemon1['name'].capitalize()}.")
        else:
            st.success(f"{pokemon1['name'].capitalize()} et {pokemon2['name'].capitalize()} ont la même défense.")

        if pokemon1['speed'] > pokemon2['speed']:
            st.success(f"{pokemon1['name'].capitalize()} est plus rapide que {pokemon2['name'].capitalize()}.")
        elif pokemon1['speed'] < pokemon2['speed']:
            st.success(f"{pokemon2['name'].capitalize()} est plus rapide que {pokemon1['name'].capitalize()}.")
        else:
            st.success(f"{pokemon1['name'].capitalize()} et {pokemon2['name'].capitalize()} ont la même vitesse.")

def simulate_battle(pokemon1_name, pokemon2_name):
    pokemon1 = get_pokemon_stats(pokemon1_name)
    pokemon2 = get_pokemon_stats(pokemon2_name)

    if not pokemon1 or not pokemon2:
        return

    st.subheader("Statistiques des Pokémon")
    display_pokemon_stats(pokemon1, pokemon2)

    pokemon1_hp = pokemon1['hp']
    pokemon2_hp = pokemon2['hp']
    round_number = 1
    battle_log = st.empty()
    progress_bar1 = st.progress(0)
    progress_bar2 = st.progress(0)
    while pokemon1_hp > 0 and pokemon2_hp > 0 and round_number <= 15:

        time.sleep(2)
        battle_log.info(f"--- Tour {round_number} ---")

        pokemon1_damage = max(0, pokemon1['attack'] - pokemon2['defense'])
        pokemon2_damage = max(0, pokemon2['attack'] - pokemon1['defense'])

        pokemon2_hp -= pokemon1_damage
        pokemon1_hp -= pokemon2_damage

        pokemon1_hp_percent = max(0, min(100, (pokemon1_hp / pokemon1['hp']) * 100))
        pokemon2_hp_percent = max(0, min(100, (pokemon2_hp / pokemon2['hp']) * 100))

        progress_bar1.progress(int(pokemon1_hp_percent))
        progress_bar2.progress(int(pokemon2_hp_percent))

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{pokemon1['name'].capitalize()}**")
            st.write(f"PV: {max(0, pokemon1_hp)} / {pokemon1['hp']}")
        with col2:
            st.write(f"**{pokemon2['name'].capitalize()}**")
            st.write(f"PV: {max(0, pokemon2_hp)} / {pokemon2['hp']}")

        battle_log.info(
            f"{pokemon1['name'].capitalize()} inflige {pokemon1_damage} dégâts à {pokemon2['name'].capitalize()}.\n"
            f"{pokemon2['name'].capitalize()} inflige {pokemon2_damage} dégâts à {pokemon1['name'].capitalize()}."
        )

        round_number += 1
        time.sleep(1)

    st.subheader("Résultat du combat:")
    if pokemon1_hp > 0 and pokemon2_hp <= 0:
        st.success(f"{pokemon1['name']} remporte le combat avec {pokemon1_hp} PV restants!")
    elif pokemon2_hp > 0 and pokemon1_hp <= 0:
        st.success(f"{pokemon2['name']} remporte le combat avec {pokemon2_hp} PV restants!")
    else:
        st.success("C'est un match nul!")

def get_fire_pokemon_average_hp():
    url = "https://pokeapi.co/api/v2/type/fire"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Erreur : Type 'fire' non trouvé.")
        return

    data = response.json()
    fire_pokemon = data['pokemon']

    total_hp = 0
    count = 0

    for pokemon in fire_pokemon:
        pokemon_stats = get_pokemon_stats(pokemon['pokemon']['name'])
        if pokemon_stats:
            total_hp += pokemon_stats['hp']
            count += 1

    if count > 0:
        average_hp = total_hp / count
        st.success(f"Moyenne des points de vie des Pokémon de type 'fire': {average_hp:.2f}")
    else:
        st.warning("Aucun Pokémon de type 'fire' trouvé.")