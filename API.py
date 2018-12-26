# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 23:06:51 2018

@author: tnguy
"""
"""
For this project, we will import data from opendota.com, 
which is a website that collects data from dota2 matches."""
"import necessary libraries for our data mining task."
import pandas as pd
import certifi
import json
import urllib3
""" we'll use url request to get our data """
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
api_key='2eb6fef1-70cd-47ae-bda3-f5a78f8beb03'
#url = http.request('GET', 'https://api.opendota.com/api/matches/{}?api_key=2eb6fef1-70cd-47ae-bda3-f5a78f8beb03')
urllib3.disable_warnings()
url1 = 'https://api.opendota.com/api/matches/{}?api_key=2eb6fef1-70cd-47ae-bda3-f5a78f8beb03'
#url2 = 'https://api.opendota.com/api/matches/3907772517?api_key=2eb6fef1-70cd-47ae-bda3-f5a78f8beb03'
#meta_data = json.loads(url.data)

"getting my match ids from a file I gathered beforehand and put them in listIDs"
matchIDs=pd.read_csv('matchIDs.csv')
listIDs = []
for i in matchIDs.columns:
    listIDs.append(int(i))
"Using API calls to get match_data and append those in match_info list"
match_info = []
for i in listIDs:
   url = http.request('GET', url1.format(i))
   match_info.append(json.loads(url.data))
""" let's save our data to a csv file for later use"""

with open('match_info.txt', 'w') as my_file:
    json.dump(match_info, my_file)

"""The most important data is the players list inside each match data. let's see what it contains
Firstly, let's get the players' list from each match data into a list for easy manipulation."""
player_dict_list = []
for i in match_info:
    player_dict_list.append(i['players'])
""" Now, let's check out what information is contained in players"""
print(match_info[0]['players'][0].keys())
#(['match_id', 'player_slot', 'ability_targets', 'ability_upgrades_arr', 'ability_uses', 
#'account_id', 'actions', 'additional_units', 'assists', 'backpack_0', 'backpack_1', 
#'backpack_2', 'buyback_log', 'camps_stacked', 'creeps_stacked', 'damage', 
#'damage_inflictor', 'damage_inflictor_received', 'damage_taken', 'damage_targets', 
#'deaths', 'denies', 'dn_t', 'firstblood_claimed', 'gold', 'gold_per_min', 'gold_reasons', 
#'gold_spent', 'gold_t', 'hero_damage', 'hero_healing', 'hero_hits', 'hero_id', 'item_0', 
#'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'item_uses', 'kill_streaks', 'killed', 
#'killed_by', 'kills', 'kills_log', 'lane_pos', 'last_hits', 'leaver_status', 'level', 
#'lh_t', 'life_state', 'max_hero_hit', 'multi_kills', 'obs', 'obs_left_log', 'obs_log', 
#'obs_placed', 'party_id', 'party_size', 'performance_others', 'permanent_buffs', 'pings', 
#'pred_vict', 'purchase', 'purchase_log', 'randomed', 'repicked', 'roshans_killed', 
#'rune_pickups', 'runes', 'runes_log', 'sen', 'sen_left_log', 'sen_log', 'sen_placed', 
#'stuns', 'teamfight_participation', 'times', 'tower_damage', 'towers_killed', 
#'xp_per_min', 'xp_reasons', 'xp_t', 'personaname', 'name', 'last_login', 'radiant_win', 
#'start_time', 'duration', 'cluster', 'lobby_type', 'game_mode', 'is_contributor', 'patch', 
#'region', 'isRadiant', 'win', 'lose', 'total_gold', 'total_xp', 'kills_per_min', 'kda', 
#'abandons', 'neutral_kills', 'tower_kills', 'courier_kills', 'lane_kills', 'hero_kills', 
#'observer_kills', 'sentry_kills', 'roshan_kills', 'necronomicon_kills', 'ancient_kills',
# 'buyback_count', 'observer_uses', 'sentry_uses', 'lane_efficiency', 'lane_efficiency_pct',
# 'lane', 'lane_role', 'is_roaming', 'purchase_time', 'first_purchase_time', 'item_win', 
#'item_usage', 'purchase_tpscroll', 'actions_per_min', 'life_state_dead', 'rank_tier', 
#'cosmetics', 'benchmarks'])

'''
According to opendota schema, the players list has within in itself 40 other objects. As
we are looking to put these data into a Dataframe for easy manipulation, we need to set aside
the objects within the players list. The object keys' names are:
    
objects = ['ability_targets','ability_uses','actions','additional_units','buyback_log','damage_targets', 
'damage','damage_inflictor','damage_inflictor_received','damage_taken',damage_targets',
'gold_reasons','hero_hits','item_uses','kill_streaks','killed','kills_log', 'killed_by', 
'lane_pos','life_state','max_hero_hit','multi_kills','obs', 'obs_left_log', 'obs_log', 
'permanent_buffs','purchase', 'purchase_log','sen', 'xp_reasons', 'item_win', 'item_usage',
'runes', 'runes_log', 'sen_left_log', 'sen_log', 'purchase_time','first_purchase_time',
'purchase_tpscroll','benchmarks']

Because we want to later integrate these into our dataframe, let's also include 'match_id'
and 'player_slot'  
'''
objects = ['ability_targets','ability_uses','actions','additional_units','buyback_log','damage_targets', 
'damage','damage_inflictor','damage_inflictor_received','damage_taken','damage_targets',
'gold_reasons','hero_hits','item_uses','kill_streaks','killed','kills_log', 'killed_by', 
'lane_pos','life_state','max_hero_hit','multi_kills','obs', 'obs_left_log', 'obs_log', 
'permanent_buffs','purchase', 'purchase_log','sen', 'xp_reasons', 'item_win', 'item_usage',
'runes', 'runes_log', 'sen_left_log', 'sen_log', 'purchase_time','first_purchase_time',
'purchase_tpscroll','benchmarks', 'ability_upgrades_arr','cosmetics', 'dn_t', 'gold_t', 'lh_t', 'xp_t','times']
""" Now let's delete these keys from our list """
for x in objects:
    for i in range(2947):
        for j in range(10):
            player_dict_list[i][j].pop(x,None)

""" What do the numbers below represent? """
""" Some of the info here is not listed on opendota schema, 
so we'll have to contact them later to ask for explanation"""
player_dict_list[0][0]['gold_reasons']

""" what do the integers in 'life_state' represent'? """
player_dict_list[0][0]['life_state']
""" Now we can create our dataframe for our data analysis"""
df = pd.DataFrame()
for i in range(len(player_dict_list)):
    df = pd.concat([df, pd.DataFrame(player_dict_list[i])], ignore_index = True)

len(match_info[0]['players'][0].keys())
""" Here's how we reopen the file we previously save"""
import json

with open('match_info.txt') as json_file:  
    data1 = json.load(json_file)