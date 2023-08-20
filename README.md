# Project Millstone

### Description
Who doesn't like a good 'ole mill deck? Not me!

Welcome to my take on the Magic the Gathering booster pack generator. While there are many like it, this one stands out in its unique offering: instead of being tied down to a singular MTG set, you have the freedom to generate packs from your own assorted collection.

So, what sparked this project? Simple. I have an eclectic mix of cards — from  Ice Age to Shadows over Innistrad, and even Commander Masters. Despite the richness of my collection, many of these cards just gather dust. I reckon they might find a more loving home with another enthusiast.

Sure, there are platforms like eBay where folks sell cards in heaps, often in hundreds or thousands. But where's the thrill in that? Imagine getting your hands on a bespoke booster pack, priced at a mere $10-$12. It could be a gold mine, packed with cards valued at $50+ or, let's be honest, it might just be a pack that's worth $6. Either way, it's the excitement of the unknown that makes it worth the draw.


## Quick Start

### Prerequisites
- **Python**: Make sure you have Python installed.
- **Poetry**: If you haven’t installed poetry, do so with:

    ```bash
    curl -sSL https://install.python-poetry.org | python3
    ```
    Or refer to Poetry's documentation for more installation options.

- **Data Input**: Have a CSV file with your card details ready. The required format is:

    ```mathematica
    Quantity, Card Name, Set, Est. Price, Scryfall ID
    ```
### Getting Started

1. Clone the Repository:
   
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install Dependencies:

    ```bash
    poetry install
    ```
3. Run the Program:

    ```bash
    poetry run python main.py

    ```
4. **Input CSV Path**: Provide the path to your CSV file when prompted.
   
5. **Anticipate the Magic**: Depending on your card list and internet connection (rarity data is fetched from Scryfall), a brief wait may be necessary.
   
6. **Behold the Packs**: Once processing completes, the generated booster packs and associated metadata will be displayed.

## Noteworthy Features

- **Authentic Rarity Distribution**: Experience packs with 10 commons, 3 uncommons, and 1 rare (or a 1/8 chance of a mythic rare).
- **Unique Card Selection**: Cards are chosen based on availability, ensuring no duplicates beyond actual quantities.
- **Pack Insight**: Review each pack's metadata, like total card value and card count.

