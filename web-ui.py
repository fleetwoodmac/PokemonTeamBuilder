# ~~~~~~~ import libs ~~~~~~
import streamlit as st
import zmq
import subprocess
import os
import time
import uuid
from PIL import Image


# ~~~~~~~ Web app init info ~~~~~~~~
st.set_page_config(
    page_title='Pokemon Team Builder!',
    page_icon='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png',
    layout='wide'
)


# ~~~~~~~ run first time setup if needed ~~~~~~~~~
if os.path.exists('./functional_data/') is not True:
    os.mkdir('./functional_data/')
if os.path.exists('./functional_data/has_run.txt') is not True:
    with st.spinner('Running First Time Setup, Please Wait!'):
        first_time_run = subprocess.Popen(['python3', './first_time_setup.py'])
        time.sleep(20)
        subprocess.Popen.terminate(first_time_run)
        with open('./functional_data/has_run.txt', 'w', encoding='utf-8') as f:
            f.write('First time setup ran successfully!')
    st.success('Done!')

# ~~~~~~~ import data ~~~~~~~

#  1 . import pokemon

with open('./functional_data/full_pokemon_list.txt', 'r', encoding='utf-8') as f:  # import pokemon
    pkmn_list = f.read()
    pkmn_list = pkmn_list.splitlines()

#  2 . import items
with open('./functional_data/full_item_list.txt', 'r', encoding='utf-8') as f:  # import items
    item_list = f.read()
    item_list = item_list.splitlines()


# ~~~~~~helper functions~~~~~~~~
@st.cache_data(experimental_allow_widgets=True)
def pokemon_data_fetcher(requested_pokemon: str):
    """take pokemon from option and fetch it. then parse out and return data"""
    # start zmq service
    pkmn_data_srvc = subprocess.Popen(['python3', './zmqServices/pokemon_data_service.py'])
    pokedex_srvc = subprocess.Popen(['python3', './zmqServices/pokedex_service.py'])

    # connect to zmq pokemon data service
    context = zmq.Context()

    socket1 = context.socket(zmq.REQ)
    socket1.connect("tcp://127.0.0.1:5555")
    socket1.send_pyobj(requested_pokemon)
    pkmn_received = socket1.recv_pyobj()

    socket2 = context.socket(zmq.REQ)
    socket2.connect("tcp://127.0.0.1:5556")

    # parse out data
    if pkmn_received == 'Could not find pokemon!':
        return 'Could not find pokemon!'
    else:
        try:
            # sprite
            sprite_url = pkmn_received['sprites']['front_default']
            # pokemon desc
            species_url = pkmn_received['species']['url']
            socket2.send_pyobj(species_url)
            species_received = socket2.recv_pyobj()
            flavor_list = species_received['flavor_text_entries']
            for item in flavor_list:
                if item['language']['name'] == "en":
                    dex_entry = item['flavor_text']
                    break
                else:
                    pass
            # species name
            species_name = species_received['name']
            # learnset
            learn_set = pkmn_received['moves']
            # type
            type_list = pkmn_received['types']
            types = []
            for item in type_list:
                types.append(item['type']['name'])
        except Exception:
            print('Unknown error!')

    # terminate zmq services
    subprocess.Popen.terminate(pkmn_data_srvc)
    subprocess.Popen.terminate(pokedex_srvc)

    return sprite_url, dex_entry, learn_set, types, species_name


@st.cache_data(experimental_allow_widgets=True)
def move_list(learnset: list):
    move_dictionary = {}
    for item in learnset:
        if type(item) == list:
            pass
        else:
            move_dictionary[item['move']['name']] = item['move']['url']
    return move_dictionary


@st.cache_data(experimental_allow_widgets=True)
def move_data_fetcher(move_sel, move: str):
    """take move and request data. then parse out and return data"""

    # start zmq service
    move_srvc = subprocess.Popen(['python3', './zmqServices/move_service.py'])

    # connect to move_service
    context = zmq.Context()
    socket3 = context.socket(zmq.REQ)
    socket3.connect("tcp://127.0.0.1:5557")

    # request and parse
    socket3.send_pyobj(move)
    movedata_rcvd = socket3.recv_pyobj()

    # move desc
    try:
        move_desc = movedata_rcvd['effect_entries'][0]['effect']
    except Exception:
        temp = move_sel
        temp = str.title(temp)
        temp = temp.replace('-', '_')
        move_desc = f'Couldn\'t find move description on PokeAPI. ' \
                    f'See Bulbapedia entry! https://bulbapedia.bulbagarden.net/wiki/{temp}_(move)'
    # move type
    move_type = movedata_rcvd['type']['name']
    # move power and acc
    move_pw = movedata_rcvd['power']
    if move_pw is None:
        move_pw = 'N/A'
    move_acc = movedata_rcvd['accuracy']
    if move_acc is None:
        move_acc = 'N/A'

    # terminate zmq service
    subprocess.Popen.terminate(move_srvc)

    return move_desc, move_type, move_pw, move_acc


@st.cache_data(experimental_allow_widgets=True)
def item_data_fetcher(item_sel: str):
    """take item from option and fetch it. then parse out and return data"""
    # start zmq service
    item_srvc = subprocess.Popen(['python3', './zmqServices/item_service.py'])

    # connect to zmq item data service
    context = zmq.Context()
    socket4 = context.socket(zmq.REQ)
    socket4.connect("tcp://127.0.0.1:5558")

    # request and parse
    socket4.send_pyobj(item_sel)
    item_received = socket4.recv_pyobj()
    # item desc
    try:
        item_desc = item_received['effect_entries'][0]['effect']
    except Exception:
        item_desc = 'Couldn\'t find description on PokeAPI.'
    # item sprite url
    try:
        item_sprite = item_received['sprites']['default']
        if item_sprite is None:
            item_sprite = 'https://pokeapi.co/media/sprites/items/master-ball.png'
    except Exception:
        item_sprite = 'https://pokeapi.co/media/sprites/items/master-ball.png'

    subprocess.Popen.terminate(item_srvc)

    return item_desc, item_sprite


def add_row(state_key: str, pkmn_move_collection: list):
    if len(pkmn_move_collection)+1 == 5:
        st.error('Cannot add more than 4 moves!', icon="🚨")
        return
    else:
        element_id = uuid.uuid4()
        st.session_state[f'{state_key}'].append(str(element_id))


def remove_row(state_key: str, row_id):
    st.session_state[f'{state_key}'].remove(str(row_id))


def generate_row(poke_data, state_key: str, row_id: str):
    move_dict = move_list(poke_data[2])
    pkmn_moves = move_dict.keys()
    mv_sel = st.selectbox("Select Move", pkmn_moves, key=f'pk_mv_{row_id}')
    mv_data = move_data_fetcher(mv_sel, move_dict[mv_sel])
    with st.expander("Move Information & Remove Button"):
        mv_col1, mv_col2, del_col = st.columns([0.8, .75 * 4, 0.5])
        with mv_col1:
            st.text("Type:")
            st.image(f'./functional_data/icons/{mv_data[1]}.png')
            st.text(f'Pow: {mv_data[2]}')
            st.text(f'Acc: {mv_data[3]}')
        with mv_col2:
            st.write(mv_data[0])
        with del_col:
            st.button("🗑️", key=f"del_{row_id}", on_click=remove_row, args=[state_key, row_id])

    return {"Move": mv_col1, "Info": mv_col2}


def add_p_row(state_key):
    element_id = uuid.uuid4()
    st.session_state[f'{state_key}'].append(str(element_id))


def generate_p_row(full_pkmn_list, row_id: str):
    # Select Pokemon
    poke_col1, poke_col2 = st.columns([.65, .75])
    with poke_col1:
        pkmn_selection = st.selectbox("Select a Pokemon", full_pkmn_list, key=f'pkmn_{row_id}')
        poke_data = pokemon_data_fetcher(pkmn_selection)
        if poke_data[0] is None:
            st.write('Couldn\'t find sprite on PokeAPI.')
        else:
            st.image(poke_data[0])
        st.text("Type:")
        for item in poke_data[3]:
            image = Image.open(f'./functional_data/icons/{item}.png')
            new_image = image.resize((100, 20))
            st.image(new_image)
    with poke_col2:
        # display dex entry
        st.image(f'./functional_data/icons/pokedex.png')
        st.write(poke_data[1])
        st.slider('Level', min_value=1, max_value=100, step=1, key=f'pkmn_lvl_{row_id}')
        # try to find smogon link
        st.write('Smogon Competitive Anaylsis:')
        ver_selection = st.selectbox("Select a version",
                                      ['RB', 'GS', 'RS',
                                       'DP', 'BW', 'XY',
                                       'SM', 'SS', 'SV'],
                                      key=f'comp_analysis_{row_id}')
        st.markdown(f'[Smogon Link](https://www.smogon.com/dex/{str.lower(ver_selection)}/pokemon/{[poke_data[4]]})')
    return {"PokeCol1": poke_col1, "PokeCol2": poke_col2}, poke_data


def add_i_row(state_key):
    element_id = uuid.uuid4()
    st.session_state[f'{state_key}'].append(str(element_id))


def generate_i_row(full_item_list, row_id: str):
    # Select Items
    item_selection = st.selectbox("Select a held item", full_item_list, key=f'item_{row_id}')
    i_desc, i_sprite_url = item_data_fetcher(item_selection)
    with st.expander("Item Information"):
        i_col1, i_col2 = st.columns([0.5, 2])
        with i_col1:
            st.text("Sprite:")
            st.image(i_sprite_url)
        with i_col2:
            st.write(i_desc)
    return {"ItemCol1": i_col1, "ItemCol2": i_col2}


# ~~~~~~~~~ Layout stuff ~~~~~~~~~~

# Web App Header/Title
st.title('Pokemon Team Builder')
st.markdown('by [fleetwoodmac](https://github.com/fleetwoodmac)')
st.write('v0.1 Notes: \n'
         'May not work for all Pokemon. Lots of checks need to be added for things like sprite image format, '
         'if moves exist for the pokemon, and special cases like really legendaries, which tend to break the app. '
         'This may change on its own as PokeAPI is updated with more info. Please feel free to inspect the source code'
         'and extend the function of this application if you would like to!')
choice = st.selectbox('Team View Mode?', ('SinglePage', 'Tabbed'))

# init tabs session state
if 'tabs' not in st.session_state:
    st.session_state['tabs'] = ["Pokemon 1", "Pokemon 2", "Pokemon 3", "Pokemon 4", "Pokemon 5", "Pokemon 6"]

# init pkmn state session
if 'pkmn' not in st.session_state:
    st.session_state['pkmn'] = []

pkmn_collection = []

# init move state sessions
if 'pk1_mvs' not in st.session_state:
    st.session_state['pk1_mvs'] = []
if 'pk2_mvs' not in st.session_state:
    st.session_state['pk2_mvs'] = []
if 'pk3_mvs' not in st.session_state:
    st.session_state['pk3_mvs'] = []
if 'pk4_mvs' not in st.session_state:
    st.session_state['pk4_mvs'] = []
if 'pk5_mvs' not in st.session_state:
    st.session_state['pk5_mvs'] = []
if 'pk6_mvs' not in st.session_state:
    st.session_state['pk6_mvs'] = []

pk1_collection = []
pk2_collection = []
pk3_collection = []
pk4_collection = []
pk5_collection = []
pk6_collection = []

# init item state session
if 'item' not in st.session_state:
    st.session_state['item'] = []

item_collection = []


def tabbed(selection):
    if selection == 'Tabbed':
        # Teamslot display stuff
        tabs = st.tabs(st.session_state["tabs"])

        with tabs[0]:
            st.header("Teamslot 1")
            # Pokemon
            state_key_pkmn = 'pkmn'
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][0])
            pkmn_collection.append(pokerow_data)
            # Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][0])
            item_collection.append(itemrow_data)
            # Moves
            state_key_pk1 = 'pk1_mvs'
            for move in st.session_state[state_key_pk1]:
                row_data = generate_row(poke_data, state_key_pk1, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk1, pk1_collection], key='pk1')
        with tabs[1]:
            st.header("Teamslot 2")
            # Select Pokemon
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][1])
            pkmn_collection.append(pokerow_data)
            # Select Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][1])
            item_collection.append(itemrow_data)
            # Select Moves
            state_key_pk2 = 'pk2_mvs'
            for move in st.session_state[state_key_pk2]:
                row_data = generate_row(poke_data, state_key_pk2, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk2, pk2_collection], key='pk2')
        with tabs[2]:
            st.header("Teamslot 3")
            # Select Pokemon
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][2])
            pkmn_collection.append(pokerow_data)
            # Select Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][2])
            item_collection.append(itemrow_data)
            # Select Moves
            state_key_pk3 = 'pk3_mvs'
            for move in st.session_state[state_key_pk3]:
                row_data = generate_row(poke_data, state_key_pk3, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk3, pk3_collection], key='pk3')
        with tabs[3]:
            st.header("Teamslot 4")
            # Select Pokemon
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][3])
            pkmn_collection.append(pokerow_data)
            # Select Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][3])
            item_collection.append(itemrow_data)
            # Select Moves
            state_key_pk4 = 'pk4_mvs'
            for move in st.session_state[state_key_pk4]:
                row_data = generate_row(poke_data, state_key_pk4, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk4, pk4_collection], key='pk4')
        with tabs[4]:
            st.header("Teamslot 5")
            # Select Pokemon
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][4])
            pkmn_collection.append(pokerow_data)
            # Select Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][4])
            item_collection.append(itemrow_data)
            # Select Moves
            state_key_pk5 = 'pk5_mvs'
            for move in st.session_state[state_key_pk5]:
                row_data = generate_row(poke_data, state_key_pk5, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk5, pk5_collection], key='pk5')
        with tabs[5]:
            st.header("Teamslot 6")
            # Select Pokemon
            add_p_row(state_key_pkmn)
            pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][5])
            pkmn_collection.append(pokerow_data)
            # Select Item
            state_key_item = 'item'
            add_i_row(state_key_item)
            itemrow_data = generate_i_row(item_list, st.session_state['item'][5])
            item_collection.append(itemrow_data)
            # Select Moves
            state_key_pk6 = 'pk6_mvs'
            for move in st.session_state[state_key_pk6]:
                row_data = generate_row(poke_data, state_key_pk6, move)
                pk1_collection.append(row_data)
            menu = st.columns(2)
            with menu[0]:
                st.button("Add Move", on_click=add_row, args=[state_key_pk6, pk6_collection], key='pk6')
    else:
        return


def single_page(selection):
    if selection == 'SinglePage':
        teamslot1, teamslot2, teamslot3 = st.columns(3, gap='large')

        with st.container():
            with teamslot1:
                st.header("Teamslot 1")
                state_key_pkmn = 'pkmn'
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][0])
                pkmn_collection.append(pokerow_data)
                state_key_pk1 = 'pk1_mvs'
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][0])
                item_collection.append(itemrow_data)
                # Select Moves
                for move in st.session_state[state_key_pk1]:
                    row_data = generate_row(poke_data, state_key_pk1, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk1, pk1_collection], key='pk1')
            with teamslot2:
                st.header("Teamslot 2")
                # Select Pokemon
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][1])
                pkmn_collection.append(pokerow_data)
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][1])
                item_collection.append(itemrow_data)
                # Select Moves
                state_key_pk2 = 'pk2_mvs'
                for move in st.session_state[state_key_pk2]:
                    row_data = generate_row(poke_data, state_key_pk2, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk2, pk2_collection], key='pk2')
            with teamslot3:
                st.header("Teamslot 3")
                # Select Pokemon
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][2])
                pkmn_collection.append(pokerow_data)
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][2])
                item_collection.append(itemrow_data)
                # Select Moves
                state_key_pk3 = 'pk3_mvs'
                for move in st.session_state[state_key_pk3]:
                    row_data = generate_row(poke_data, state_key_pk3, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk3, pk3_collection], key='pk3')

        teamslot4, teamslot5, teamslot6 = st.columns(3)

        with st.container():
            with teamslot4:
                st.header("Teamslot 4")
                # Select Pokemon
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][3])
                pkmn_collection.append(pokerow_data)
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][3])
                item_collection.append(itemrow_data)
                # Select Moves
                state_key_pk4 = 'pk4_mvs'
                for move in st.session_state[state_key_pk4]:
                    row_data = generate_row(poke_data, state_key_pk4, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk4, pk4_collection], key='pk4')
            with teamslot5:
                st.header("Teamslot 5")
                # Select Pokemon
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][4])
                pkmn_collection.append(pokerow_data)
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][4])
                item_collection.append(itemrow_data)
                # Select Moves
                state_key_pk5 = 'pk5_mvs'
                for move in st.session_state[state_key_pk5]:
                    row_data = generate_row(poke_data, state_key_pk5, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk5, pk5_collection], key='pk5')
            with teamslot6:
                st.header("Teamslot 6")
                # Select Pokemon
                add_p_row(state_key_pkmn)
                pokerow_data, poke_data = generate_p_row(pkmn_list, st.session_state['pkmn'][5])
                pkmn_collection.append(pokerow_data)
                # Select Item
                state_key_item = 'item'
                add_i_row(state_key_item)
                itemrow_data = generate_i_row(item_list, st.session_state['item'][5])
                item_collection.append(itemrow_data)
                # Select Moves
                state_key_pk6 = 'pk6_mvs'
                for move in st.session_state[state_key_pk6]:
                    row_data = generate_row(poke_data, state_key_pk6, move)
                    pk1_collection.append(row_data)
                menu = st.columns(2)
                with menu[0]:
                    st.button("Add Move", on_click=add_row, args=[state_key_pk6, pk6_collection], key='pk6')
    else:
        return


view_mode = {'SinglePage': single_page(choice), 'Tabbed': tabbed(choice)}

# ~~~~~ Code Graveyard ~~~~~~

# Select Pokemon
# poke_col1, poke_col2 = st.columns([.65, .75])
# Go Beavs!!!
# with poke_col1:
#     pkmn_selection = st.selectbox("Select a Pokemon", pkmn_list, key='pkmn1')
#     poke_data = pokemon_data_fetcher(pkmn_selection)
#     st.image(poke_data[0])
#     st.text("Type:")
#     for item in poke_data[3]:
#         image = Image.open(f'./functional_data/icons/{item}.png')
#         new_image = image.resize((100, 20))
#         st.image(new_image)
# with poke_col2:
#     # display dex entry
#     st.image(f'./functional_data/icons/pokedex.png')
#     st.write(poke_data[1])
#     st.slider('Level', min_value=1, max_value=100, step=1)


# Select moves
# move_dict = move_list(poke_data[2])
# pkmn_moves = move_dict.keys()
# pk1mv1_sel = st.selectbox("Select Move 1", pkmn_moves, key='pk1mv1')
# pk1mv1_data = move_data_fetcher(move_dict[pk1mv1_sel])
# with st.expander("Move Information"):
#     mv_col1, mv_col2 = st.columns([0.8, .75*4])
#     with mv_col1:
#         st.text("Type:")
#         st.image(f'./functional_data/icons/{pk1mv1_data[1]}.png')
#         st.text(f'Pow: {pk1mv1_data[2]}')
#         st.text(f'Acc: {pk1mv1_data[3]}')
#     with mv_col2:
#         st.write(pk1mv1_data[0])
