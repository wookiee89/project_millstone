import csv
import random
import json
import uuid
import requests
import asyncio
import aiohttp
from diskcache import Cache


cache = Cache("scryfall_cache")

async def get_card_rarity(scryfall_id):
    # Check in cache first
    rarity = cache.get(scryfall_id)
    if rarity:
        return rarity

    url = f"https://api.scryfall.com/cards/{scryfall_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to fetch card with Scryfall ID {scryfall_id}")
                return None
            data = await response.json()
            cache[scryfall_id] = data.get("rarity")  # Save to cache
            print(f"Fetched card with Scryfall ID {scryfall_id} from Scryfall API with rarity {data.get('rarity')} ")
            return data.get("rarity")

async def read_cards_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        card_futures = [
            {
                "quantity": int(row[0]),
                "name": row[1],
                "set": row[2],
                "est_price": float(row[4]),
                "scryfall_id": row[5],
                "rarity_future": get_card_rarity(row[5])
            } for row in reader
        ]
    
    # Resolve all async operations
    cards = []
    for card_future in card_futures:
        card_future["rarity"] = await card_future["rarity_future"]
        del card_future["rarity_future"]  # remove the future object
        cards.append(card_future)
    
    print (f"Read {len(cards)} cards from CSV")
    
    return cards

def get_max_packs(cards):
    num_commons = sum(card["quantity"] for card in cards if card["rarity"] == "common")
    num_uncommons = sum(card["quantity"] for card in cards if card["rarity"] == "uncommon")
    num_rares = sum(card["quantity"] for card in cards if card["rarity"] == "rare") + \
                int(1/8 * sum(card["quantity"] for card in cards if card["rarity"] == "mythic"))
    
    print(f'Commons: {num_commons}')
    print(f'Uncommons: {num_uncommons}')
    print(f'Rares: {num_rares}')

    return min(num_commons // 10, num_uncommons // 3, num_rares)

def pick_cards(card_pool, num):
    chosen_cards = []
    for _ in range(num):
        if not card_pool:  # Check if the pool is empty before picking a card
            break
        card = random.choice(card_pool)
        chosen_cards.append(card)
        
        # Decrease the card's quantity and remove if depleted
        card["quantity"] -= 1
        if card["quantity"] <= 0:
            card_pool.remove(card)
    return chosen_cards

    
def generate_pack(cards):
    commons = [card for card in cards if card["rarity"].lower() == "common" and card["quantity"] > 0]
    uncommons = [card for card in cards if card["rarity"].lower() == "uncommon" and card["quantity"] > 0]
    rares_and_mythics = [card for card in cards if card["rarity"].lower() in ["rare", "mythic"] and card["quantity"] > 0]
    
    if len(commons) < 10 or len(uncommons) < 3 or len(rares_and_mythics) < 1:
        # Not enough cards of a specific rarity to form a pack
        return []
    
    pack = []
    pack.extend(pick_cards(commons, 10))
    pack.extend(pick_cards(uncommons, 3))
    if random.random() < (1/8):
        mythics = [card for card in rares_and_mythics if card["rarity"].lower() == "mythic"]
        if mythics:  # Only choose a mythic if there are any left
            pack.extend(pick_cards(mythics, 1))
        else:
            pack.extend(pick_cards(rares_and_mythics, 1))
    else:
        rares = [card for card in rares_and_mythics if card["rarity"].lower() == "rare"]
        pack.extend(pick_cards(rares, 1))
    return pack

def generate_packs(cards):
    max_packs = get_max_packs(cards)
    packs = []

    for _ in range(max_packs):
        booster_pack = generate_pack(cards)
        if not booster_pack:  # If the pack is empty or incomplete
            break

        # Create the pack dictionary with its metadata
        pack_data = {
            "pack_id": uuid.uuid4().hex,
            "cards": booster_pack,
            "total_value": sum(card["est_price"] for card in booster_pack),
            "num_cards": len(booster_pack)  # Number of cards in the pack
        }
        packs.append(pack_data)

    return packs

async def main():
    cards = await read_cards_from_csv("cards.csv")
    booster_packs = generate_packs(cards)
    with open("booster_packs.json", "w") as outfile:
        json.dump(booster_packs, outfile, indent=4)
    print(f"Generated {len(booster_packs)} booster packs")
    
    # Print the min and max value of the packs
    print(f"Min value: {min(pack['total_value'] for pack in booster_packs)}")
    print(f"Max value: {max(pack['total_value'] for pack in booster_packs)}")   
    
    # Print the average value of the packs
    print(f"Average value: {sum(pack['total_value'] for pack in booster_packs) / len(booster_packs)}") 
    
    # Print the price ranges of packs, $0-10, $10-20, $20-30, $30-40, $40-50, $50+
    print(f"Price range $0-10: {len([pack for pack in booster_packs if pack['total_value'] < 10])}")
    print(f"Price range $10-20: {len([pack for pack in booster_packs if 10 <= pack['total_value'] < 20])}")
    print(f"Price range $20-30: {len([pack for pack in booster_packs if 20 <= pack['total_value'] < 30])}") 
    print(f"Price range $30-40: {len([pack for pack in booster_packs if 30 <= pack['total_value'] < 40])}") 
    print(f"Price range $40-50: {len([pack for pack in booster_packs if 40 <= pack['total_value'] < 50])}") 
    print(f"Price range $50+: {len([pack for pack in booster_packs if 50 <= pack['total_value']])}")
    
        
if __name__ == "__main__":
    asyncio.run(main())