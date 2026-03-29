# backend/prompts.py

AVC_CATEGORIES = [
    {
        "label": "Tidningar",
        "prompt": (
            "an item that belongs in newspapers at a Swedish recycling center, "
            "such as newspapers, printed paper, magazines, advertising paper, catalogs, paper reading materials, "
            "stacked newspapers, folded paper publications, or similar clean recyclable newsprint"
        ),
    },
    {
        "label": "Textil",
        "prompt": (
            "an item that belongs in textiles at a Swedish recycling center, "
            "such as clothes, fabric, garments, shirts, pants, jackets, towels, curtains, bedding, soft textiles, "
            "worn textiles, reusable textiles, folded clothing, or household fabric items"
        ),
    },
    {
        "label": "Farligt avfall",
        "prompt": (
            "an item that belongs in hazardous waste at a Swedish recycling center, "
            "such as chemicals, paint, varnish, solvents, glue, strong cleaning chemicals, pesticides, "
            "oil containers with residue, spray cans, toxic liquids, corrosive products, batteries with leakage, "
            "or other dangerous chemical household waste"
        ),
    },
    {
        "label": "Elavfall",
        "prompt": (
            "an item that belongs in electronic waste at a Swedish recycling center, "
            "such as lamps, desk lamps, screens, televisions, monitors, computers, laptops, keyboards, chargers, cables, "
            "electronic devices, household electronics, broken appliances, or anything with electrical or electronic components"
        ),
    },
    {
        "label": "Vitvaror (Kyl och frys)",
        "prompt": (
            "a large white goods appliance for a Swedish recycling center, "
            "such as a refrigerator, freezer, dishwasher, washing machine, dryer, stove, oven, or similar large kitchen or laundry appliance"
        ),
    },
    {
        "label": "Trädgårdsavfall",
        "prompt": (
            "garden waste for a Swedish recycling center, "
            "such as leaves, grass, weeds, plants, flowers, garden cuttings, soil-covered organic yard waste, "
            "or similar soft garden debris"
        ),
    },
    {
        "label": "Trä",
        "prompt": (
            "wood waste for a Swedish recycling center, "
            "such as wooden boards, untreated timber, shelves, plain wood furniture parts, wooden planks, "
            "or broken untreated wood items"
        ),
    },
    {
        "label": "Ej återvinningsbart",
        "prompt": (
            "waste that does not clearly fit a recyclable material stream at a Swedish recycling center, "
            "mixed waste, unusable broken household waste, contaminated mixed objects, or non sortable waste"
        ),
    },
    {
        "label": "Energiåtervinning",
        "prompt": (
            "burnable waste for energy recovery at a Swedish recycling center, "
            "such as combustible mixed waste, non recyclable but burnable household waste, or used objects suitable for incineration"
        ),
    },
    {
        "label": "Metall",
        "prompt": (
            "metal waste or scrap metal for a Swedish recycling center, "
            "such as metal tools, metal parts, metal frames, metal household objects, aluminum items, steel objects, "
            "scrap metal, or heavy metallic waste"
        ),
    },
    {
        "label": "Tegel",
        "prompt": (
            "brick waste for a Swedish recycling center, "
            "such as bricks, brick rubble, masonry bricks, broken red bricks, or ceramic building bricks"
        ),
    },
    {
        "label": "Betong",
        "prompt": (
            "concrete waste for a Swedish recycling center, "
            "such as concrete pieces, cement blocks, broken concrete, construction rubble, or heavy mineral concrete material"
        ),
    },
    {
        "label": "Wellpapp",
        "prompt": (
            "corrugated cardboard for a Swedish recycling center, "
            "such as shipping boxes, moving boxes, delivery boxes, folded corrugated cardboard cartons, "
            "or thick cardboard packaging material"
        ),
    },
    {
        "label": "Ris och grenar",
        "prompt": (
            "branches and twigs for a Swedish recycling center, "
            "such as tree branches, sticks, woody bush cuttings, hedge cuttings, twigs, or dry woody garden trimmings"
        ),
    },
    {
        "label": "Impregnerat trä",
        "prompt": (
            "treated or impregnated wood for a Swedish recycling center, "
            "such as pressure-treated wood, outdoor decking wood, chemically treated timber, preserved wood, painted treated wood, "
            "or toxic treated wood materials"
        ),
    },
    {
        "label": "Gips",
        "prompt": (
            "gypsum or drywall waste for a Swedish recycling center, "
            "such as plasterboard, drywall sheets, gypsum wall material, broken drywall pieces, or chalky wallboard material"
        ),
    },
    {
        "label": "Däck",
        "prompt": (
            "tires for a Swedish recycling center, "
            "such as car tires, bicycle tires, rubber wheels, loose used tires, or tire-like circular rubber objects"
        ),
    },
    {
        "label": "Planglas",
        "prompt": (
            "flat glass for a Swedish recycling center, "
            "such as window glass, mirror-like flat glass sheets, transparent panes, broken window panels, or sheet glass"
        ),
    },
    {
        "label": "Stoppade möbler",
        "prompt": (
            "upholstered furniture for a Swedish recycling center, "
            "such as sofas, armchairs, padded chairs, mattresses, cushions attached to furniture, "
            "or furniture with stuffing and textile covering"
        ),
    },
    {
        "label": "Hårdplast",
        "prompt": (
            "hard plastic objects for a Swedish recycling center, "
            "such as buckets, rigid plastic containers, plastic crates, plastic toys, hard plastic furniture parts, "
            "or durable molded plastic items"
        ),
    },
    {
        "label": "Mjukplast",
        "prompt": (
            "soft plastic for a Swedish recycling center, "
            "such as plastic bags, wrapping film, soft packaging plastic, shrink wrap, bubble wrap, "
            "flexible plastic sheets, or thin soft plastic material"
        ),
    },
    {
        "label": "Fallfrukt",
        "prompt": (
            "fallen fruit for a Swedish recycling center, "
            "such as apples, pears, rotten fruit, bruised fruit, collected fruit from the ground, or fruit garden waste"
        ),
    },
    {
        "label": "Böcker",
        "prompt": (
            "books for a Swedish recycling center, "
            "such as hardcover books, paperbacks, textbooks, novels, bound printed materials, or stacks of books"
        ),
    },
    {
        "label": "Lastpallar",
        "prompt": (
            "wooden pallets for a Swedish recycling center, "
            "such as transport pallets, warehouse pallets, shipping pallets, pallet boards assembled into pallet form, "
            "or stackable wooden pallets"
        ),
    },
]