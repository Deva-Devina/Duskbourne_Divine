# Duskbourne Divine

*Last Updated: 2025-09-12*
*Version: 2.0 - Combined Documentation*

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Technical Architecture](#2-technical-architecture)
- [3. World & Environment](#3-world--environment)
- [4. Character Systems](#4-character-systems)
- [5. Clan Systems](#5-clan-systems)
- [6. Gameplay Mechanics](#6-gameplay-mechanics)
- [7. Magic & Addiction Systems](#7-magic--addiction-systems)
- [8. Incarnation & Progression](#8-incarnation--progression)
- [9. Economy & Trade](#9-economy--trade)
- [10. Crafting & Items](#10-crafting--items)
- [11. Development Framework](#11-development-framework)

---

## 1. Project Overview

### Core Vision

**Duskbourne Divine** is a **2D top-down pixel art tribe management RPG** that transcends genre boundaries. It's a masterful fusion of **life simulation, survival, tactical RPG mechanics, magic, addiction simulation, and procedural generation**, all orchestrated within a **generational simulation experience**.

This isn't just a game; it's a **digital mythos**, a **living world** where the echoes of past lives shape the destiny of future generations, where the player's journey is one of **mortal struggle, spiritual ascension, and the seductive pull of power and addiction**, culminating in the acquisition of **godlike influence**.

### Game Genre & Platform

- **Platform**: Mobile game written in Python, expanding to PC and consoles
- **Genre**: 2D pixel art top-down role-playing life simulation tribe management game
- **Art Style**: Procedurally generated pixel art for characters and wildlife
- **Future Vision**: Eventually expands to become an MMORPG on mobile devices

### Core Gameplay Loop

- **Generational Play**: Play through generations as the tribe leader's offspring
- **Survival Focus**: No linear storyline, focusing on survival and evolution
- **Dynamic Challenges**: Face challenges of diplomacy, violence, romance, and evolution
- **Unique Experiences**: Each playthrough is unique, with no two being alike
- **Progressive Difficulty**: Challenging gameplay without being impossible
- **Unlock System**: Unlock new features, survival mechanics, and genetic enhancements with each playthrough

### Key Features

- **2D Pixel Art**: Top-down perspective with procedurally generated character sprites
- **ECS Architecture**: Modular, data-oriented design for performance and extensibility
- **Dynamic Time**: 24-minute real days, 10-day weeks, 4 seasons per year
- **100+ Resources**: Complex resource gathering and crafting systems
- **Generational Play**: Play through multiple generations as tribe leaders' offspring
- **Living Ecosystem**: Background simulation of flora, fauna, and environmental changes
- **AI-Driven NPCs**: Advanced behavior trees and decision-making systems
- **Procedural Generation**: Unique worlds, characters, and content every playthrough

---

## 2. Technical Architecture

### Core Engine

- **Programming Language**: Python 3.12
- **Architecture**: Entity-Component-System (ECS)
- **Rendering**: 2D Pixel art with procedural generation
- **Physics**: Reverse kinematics for character animation
- **Data Management**: YAML-based data system for content, JSON-based save system with compression

### Entity-Component-System (ECS) Design

#### Core Pattern

- **Entities**: Lightweight identifiers (IDs) for every object in the game world (NPCs, trees, houses, spells, resources, UI elements)
- **Components**: Pure data containers holding specific information about an entity
  - Examples:
    - `Position(x: float, y: float)`
    - `Health(current: int, max: int)`
    - `Clan(type: ClanEnum)`
    - `Inventory(items: list[ItemID])`
    - `DNAStrand(seed: int)`
    - `Needs(hunger: float, thirst: float, sanity: float)`
    - `Skills(blacksmithing: int, herbalism: int, ...)`
    - `Relationships(map[NPCID, RelationshipData])`
    - `Renderable(sprite_id: str, animation_state: str)`
    - `Addiction(addictive_substance: str, level: int, withdrawal_timer: int)`
    - `Magic(mana_current: float, mana_max: float, known_spells: list[SpellID])`

- **Systems**: Independent processors that operate on entities possessing specific combinations of components
  - Examples:
    - `MovementSystem`: Updates position based on velocity
    - `RenderingSystem`: Draws entities to screen
    - `NeedsSystem`: Modifies needs based on environment
    - `CombatSystem`: Manages turn-based combat
    - `MagicSystem`: Handles spellcasting
    - `AddictionSystem`: Modifies behavior based on addiction

### Event-Driven Architecture (EDA)

- Systems communicate through events (data packets broadcast when significant events happen)
- Examples:
  - `EntityDamagedEvent(entity_id: int, damage: int, source_id: int)`
  - `ResourceDepletedEvent(resource_type: str, location: (x, y))`
  - `RelationshipChangedEvent(npc1_id: int, npc2_id: int, new_relationship_data: RelationshipData)`
  - `SpellCastEvent(caster_id: int, spell_id: SpellID, target_id: int)`

### Data Management System

#### YAML Data Architecture

- **Content Data**: Items, biomes, recipes, entities, factions stored in YAML files
- **Schema Validation**: Pydantic dataclasses ensure type safety and data integrity
- **Hot Reloading**: Development support for live data updates
- **Modular Design**: Separate files for different data types (items.yaml, biomes.yaml, etc.)

#### Data Types

- **Items**: Weapons, armor, tools, consumables, resources
- **Biomes**: Environmental data with temperature, moisture, altitude ranges
- **Recipes**: Crafting recipes with ingredients, stations, skill requirements
- **Entities**: NPC templates with stats, components, and behaviors
- **Factions**: Clan data with relationships and characteristics

#### Save System

- **Game State**: JSON-based serialization of ECS world state
- **Compression**: Efficient storage for large world states
- **Incremental Saves**: Autosave without interrupting gameplay
- **Cross-Platform**: Save compatibility across devices

### Performance Targets

- **Frame Rate**: 60 FPS (minimum 30 FPS on low-end systems)
- **Physics**: 60 updates per second
- **AI**: 10 updates per second
- **Memory**: < 2GB initial load, < 4GB peak
- **Save Files**: < 10MB per save

---

## 3. World & Environment

### Procedural World Generation

#### Generation Process

1. **Continent & Ocean Layout**: Base land/water mask using Voronoi diagrams
2. **Tectonic Simulation**: Plate interactions creating mountains, rifts, faults
3. **Coarse Terrain Shaping**: Multi-octave Perlin noise modulated by tectonics
4. **Polar Ice Cap Placement**: Ice caps with temperature and biome influence
5. **Hydraulic & Thermal Erosion**: Rivers, deltas, glacial movement
6. **Climate & Moisture Simulation**: Temperature/moisture based on geography
7. **Fine Terrain Shaping**: Minor noise perturbations for realism
8. **Biome Assignment**: Weighted blending of temperature, moisture, elevation

#### Input Parameters

- **Seed**: Random seed for deterministic generation
- **World Size**: Dimensions in tiles (width = 2 × height ratio enforced)
- **Continents**: Number of continents to generate (3-4 recommended)
- **Plate Count**: Number of tectonic plates (5-10)
- **Perlin Octaves**: Noise octaves for terrain (4-8)
- **Erosion Steps**: Hydraulic/thermal erosion iterations (1000)

### Biome System

Biomes are determined by Temperature, Moisture, and Altitude parameters:

#### Primary Biomes

- **Forest**: Rainforest, Deciduous Forest, Boreal Forest
- **Highland**: Tundra
- **Grassland**: Savanna, Steppe
- **Desert**: Polar, Semi-arid, Sand
- **Wetland**: Mangrove, Swamp
- **Rockland**: Badlands, Cliffside
- **Coastal**: Dunes, Beach, Ocean

### Weather System

Dynamic weather affects resource availability, character comfort, travel, and magical phenomena.

#### Weather Conditions

**Clear:**

- Light Level: 1.0, Temperature Effect: 0.0, Visibility: 1.0
- Movement: Speed 1.0, Stamina Drain 1.0, Perception Bonus 1.1
- Duration: 6-24 hours

**Rainy:**

- Light Level: 0.5, Temperature Effect: -3.0, Visibility: 0.4
- Movement: Speed 0.9, Stamina Drain 1.2, Perception Penalty 0.15
- Effects: Extinguishes Fires 0.8, Waters Plants 0.3, Erosion Rate 0.25

**Stormy:**

- Light Level: 0.3, Temperature Effect: -4.0, Visibility: 0.2
- Movement: Speed 0.8, Stamina Drain 1.5, Accuracy Penalty 0.25
- Effects: Lightning Strikes 0.05, Wind Effect 1.5

### Time System

#### Time Lengths

- **Hour**: 60 minutes
- **Day**: 24 hours (24 minutes real-time)
- **Week**: 10 days
- **Month**: 30 days
- **Year**: 10 months (300 days total)

#### Seasons (with day counts)

- **Thawborn**: 38 days
- **Seedwake**: 37 days
- **Bloomcrest**: 38 days
- **Sunreach**: 37 days
- **Amberwane**: 38 days
- **Leaffall**: 37 days
- **Frostfell**: 38 days
- **Voidgleam**: 37 days

---

## 4. Character Systems

### Core Stats (1-20 Scale)

- **Stamina**: Physical endurance and resilience
  - Affects: Fatigue resistance, physical task endurance
  - Key for: Prolonged activities, carrying capacity, resisting exhaustion

- **Strength**: Raw physical power, melee damage, carrying capacity
  - Affects: Melee damage, carrying capacity, physical tasks
  - Key for: Combat, construction, mining, logging

- **Dexterity**: Agility, reflexes, hand-eye coordination
  - Affects: Ranged accuracy, crafting precision, dodging
  - Key for: Ranged combat, crafting, fine manipulation tasks

- **Perception**: Awareness, sensory acuity, detection abilities
  - Affects: Detection range, accuracy, awareness
  - Key for: Ranged combat, foraging, tracking, spotting hidden objects

- **Willpower**: Mental fortitude, resistance to stress and magic
  - Affects: Mental resistance, spell power, focus
  - Key for: Magic use, resisting mental effects, maintaining concentration

### Advanced Stats (Derived)

- **Endurance**: (Stamina + Strength) / 2 - Physical resilience
  - Affects: Health pool, resistance to physical damage
  - Key for: Tanking damage, physical labor

- **Prowess**: (Strength + Dexterity) / 2 - Combat effectiveness
  - Affects: Melee and ranged attack power
  - Key for: All forms of combat

- **Finesse**: (Dexterity + Perception) / 2 - Precision and coordination
  - Affects: Critical hit chance, crafting quality
  - Key for: Crafting, precise actions, ranged attacks

- **Conviction**: (Willpower + Perception) / 2 - Mental resilience
  - Affects: Magic resistance, social influence
  - Key for: Resisting magic, persuasion, leadership

- **Vitality**: (Stamina + Willpower) / 2 - Overall life force
  - Affects: Health regeneration, resistance to status effects
  - Key for: General survivability, resistance to environmental effects

### Resource Pools

- **Health (HP)**: (Endurance + Vitality) × 10
  - Represents physical well-being and ability to withstand damage
  - Affected by: Injuries, diseases, exhaustion
  - Recovery: Rest, medical treatment, healing items

- **Mana (MP)**: (Conviction + Finesse) × 10
  - Represents magical energy for casting spells
  - Affected by: Willpower, magical aptitude, environmental factors
  - Recovery: Meditation, rest, magical sources

- **Stamina**: (Endurance + Willpower) × 10
  - Represents physical endurance for actions
  - Affected by: Physical exertion, health status, needs
  - Recovery: Rest, food, certain skills

- **Energy**: (Stamina + Vitality) × 5
  - Represents overall energy for daily activities
  - Affected by: All needs, especially sleep and nutrition
  - Recovery: Meeting needs, rest, certain skills

### Core Stat Effects on Needs

Each core stat influences how characters interact with their needs and the world around them:

**Stamina Effects:**
- **Hunger**: High stamina delays hunger onset and increases satisfaction duration
- **Thirst**: Similar to hunger, high stamina delays thirst or increases water efficiency
- **Energy**: Stamina directly impacts energy pool and decreases depletion rate
- **Sleep**: High stamina characters need less sleep for full energy recovery
- **Comfort**: Higher stamina provides resistance to discomfort during physical tasks
- **Stress**: Stamina helps manage stress better, allowing easier recovery from stressful situations

**Strength Effects:**
- **Health**: High strength improves health resistance and recovery from physical damage
- **Safety**: High strength improves self-defense and reduces safety risks
- **Stress**: High strength mitigates physical toll of stress
- **Motivation**: Strength influences drive to push through difficult tasks

**Dexterity Effects:**
- **Comfort**: Dexterity helps adapt to uncomfortable physical situations
- **Health**: High dexterity improves injury avoidance and reduces accident chances
- **Energy**: Dexterity allows more efficient energy use, reducing fatigue
- **Stress**: Dexterity reduces stress when navigating challenging tasks
- **Motivation**: Dexterous characters find intricate tasks easier, increasing accomplishment

**Perception Effects:**
- **Boredom**: High perception reduces boredom through environmental awareness
- **Social**: Perception improves social interactions by understanding others' moods
- **Morale**: Perceptive characters recognize opportunities, leading to higher morale
- **Enjoyment**: Higher perception finds enjoyment in small details

**Willpower Effects:**
- **Morale**: High willpower maintains morale in adverse conditions
- **Focus**: Willpower directly tied to focus and concentration
- **Stress**: High willpower helps manage stress and remain calm
- **Motivation**: Higher willpower provides greater drive to meet needs

### Character Needs System

Characters must manage multiple core survival needs that affect their performance and well-being:

#### Core Survival Needs

1. **Hunger** - Sustenance and nutrition
   - Depletion Rate: 1% per 10 minutes of active gameplay
   - Effects:
     - Below 50%: Reduces stamina regeneration
     - Below 25%: Movement penalty
     - At 0%: Health damage over time
   - Recovery: Eating food, certain skills reduce depletion

2. **Thirst** - Hydration requirements
   - Depletion Rate: 1.5% per 10 minutes of active gameplay
   - Effects:
     - Below 50%: Increases fatigue
     - Below 25%: Stamina penalty
     - At 0%: Health damage over time
   - Recovery: Drinking water, certain skills reduce depletion

3. **Fatigue** - Need for rest and sleep
   - Depletion Rate: 1% per 15 minutes of active gameplay
   - Effects:
     - Below 50%: Reduced action effectiveness
     - Below 25%: Chance of passing out
     - At 0%: Unconsciousness
   - Recovery: Sleeping in beds (best), makeshift beds, resting at campfires

4. **Temperature** - Body temperature regulation
   - Affected by: Weather conditions, clothing/armor, shelter, fire
   - Effects:
     - Too cold: Frostbite, reduced dexterity
     - Too hot: Heat stroke, increased water consumption
   - Management: Proper clothing, shelter, proximity to heat sources

#### Secondary Needs

5. **Hygiene** - Cleanliness affecting social interactions and health
   - Effects:
     - Poor hygiene: Negative social modifiers
     - Very poor: Increased disease risk
   - Management: Bathing, clean clothing, access to water

6. **Comfort** - Overall well-being and morale
   - Affected by: Quality of shelter, food variety, social interactions
   - Effects: Influences morale, stress reduction, rest quality

7. **Social** - Interaction and belonging
   - Affected by: Social interactions, relationships, group activities
   - Effects: Influences morale, mental health, certain skill bonuses

8. **Health** - Physical well-being
   - Affected by: Injuries, diseases, environmental factors
   - Management: Rest, medical treatment, potions

9. **Bladder** - Waste relief needs
   - Effects: Discomfort if ignored, potential health issues
   - Management: Access to appropriate facilities

10. **Stress** - Mental and emotional pressure
    - Effects: Reduces effectiveness, can lead to breakdowns
    - Management: Rest, relaxation, social support

11. **Morale** - Overall happiness and motivation
    - Affected by: Needs being met, social status, achievements
    - Effects: Influences productivity, learning speed, social interactions

12. **Motivation** - Drive to complete tasks
    - Affected by: Personal goals, needs, social dynamics
    - Effects: Task completion speed, success rates

13. **Focus** - Concentration and mental clarity
    - Affected by: Rest, stress, environment
    - Effects: Skill checks, learning speed, crafting quality

14. **Enjoyment** - Pleasure and entertainment
    - Affected by: Activities, social interactions, environment
    - Effects: Stress reduction, morale boost

15. **Mana** - Magical energy reserves
    - Depletion: Used for casting spells and magical abilities
    - Regeneration: Varies by time of day, location, and character traits

#### Secondary Needs

- **Hygiene**, **Comfort**, **Social**, **Health**, **Bladder**, **Stress**, **Morale**, **Motivation**, **Focus**, **Enjoyment**, **Mana**

### Personality & Traits System

#### Trait Evolution by Age
- **Infant**: Temperament
- **Toddler**: Temperament + Socialization
- **Child**: (Temperament→Emotional) + Socialization + Cognition
- **Teenager**: Emotional + (Socialization→Interaction) + Cognition + Identity
- **Young Adult**: Emotional + Interaction + (Cognition→Ambition) + Identity + Morals
- **Adult**: Emotional + Interaction + Ambition + (Identity→Perspective) + Morals
- **Elder**: Emotional + Interaction + (Ambition→Legacy) + Perspective + Morals

#### Trait Domains
Each domain contains 6 negative (🔥), 6 neutral (⚪), and 6 positive (🌟) traits:

- **Temperament**: Withdrawn→Affectionate spectrum
- **Emotional**: Detached→Resilient spectrum
- **Socialization**: Isolative→Affirming spectrum
- **Cognition**: Rigid→Astute spectrum
- **Interaction**: Aggressive→Charismatic spectrum
- **Identity**: Uncertain→Unique spectrum
- **Ambition**: Apathetic→Trailblazing spectrum
- **Perspective**: Narrow-minded→Expansive spectrum
- **Morals**: Unethical→Benevolent spectrum
- **Legacy**: Forgettable→Celebrated spectrum

### Skill-Need Relationships

- **Stamina Skills:**
  - **Farming**: Physical labor builds stamina, increases hunger tolerance
  - **Fishing**: Casting and reeling increases stamina, delays thirst effects
  - **Mining**: Physical exertion requires and builds stamina
  - **Logging**: Cutting trees and hauling logs increases stamina
  - **Foraging**: Traveling and searching boosts stamina
  - **Combat**: Physical exertion in battles requires stamina maintenance
  - **Smithing**: Continuous forge work demands stamina
  - **Baking/Cooking**: Long cooking sessions help increase stamina
  - **Healing**: Performing healing tasks over time builds stamina

- **Strength Skills:**
  - **Masonry**: Lifting heavy stones demands strength
  - **Carpentry**: Handling large tools and materials requires strength
  - **Earthwork**: Digging and moving earth demands strength
  - **Mining**: Extracting ore requires significant strength
  - **Logging**: Cutting trees and handling logs requires physical strength
  - **Combat**: Direct fighting relies heavily on strength
  - **Smithing**: Hammering metal requires considerable strength
  - **Tanning**: Physical work in tanning hides requires strength
  - **Tailoring**: Working with heavy fabrics may require strength
  - **Alchemy**: Handling heavy ingredients requires strength

- **Dexterity Skills:**
  - **Design**: Requires precision and fine motor control
  - **Carpentry**: Crafting detailed woodwork demands dexterity
  - **Engineering**: Fine motor control for assembling machines
  - **Taming**: Handling and training animals requires dexterity
  - **Fishing**: Reeling in fish and handling gear requires dexterity
  - **Logging**: Cutting trees with precision demands dexterity
  - **Smithing**: Creating intricate items requires dexterous control
  - **Tailoring**: Sewing and stitching require delicate movements
  - **Crafting**: Fine motor control for detailed items
  - **Marksmanship**: Aiming and shooting with precision demands dexterity
  - **Strategy**: Mental dexterity in planning and decision-making
  - **Spellcraft**: Fine manipulation of magic requires dexterous control
  - **Runesmithing**: Crafting intricate runes requires fine dexterity
  - **Navigation**: Dexterity in charting and movement
  - **Vigilance**: Quick reactions to stimuli require dexterity

- **Perception Skills:**
  - **Foraging**: Requires keen observation to locate resources
  - **Fishing**: Spotting fish and reacting to environmental changes
  - **Mining**: Identifying ore veins and detecting potential resources
  - **Logging**: Spotting the right trees and timber
  - **Tracking**: Finding and following animal tracks
  - **Navigation**: Understanding surroundings and directions
  - **Vigilance**: Being alert to surroundings and threats
  - **Charisma**: Interpreting others' feelings and adjusting interactions

- **Willpower Skills:**
  - **Masonry**: Mental focus and endurance for tough projects
  - **Carpentry**: Stamina and focus over long hours of work
  - **Mining**: Mental endurance to push through long, tough tasks
  - **Combat**: Staying determined in battle, pushing through fatigue
  - **Healing**: Persistence to help others in challenging conditions
  - **Alchemy**: Maintaining focus during complex processes
  - **Spellcraft**: Magical endeavors, particularly difficult spells
  - **Accounting**: Keeping focused on calculations and management
  - **Charisma**: Persuading and maintaining control in interactions System

### DNA-Based Character Creation

Every character is defined by DNA parameters controlling:

- Body shape and features
- Colors (hair, skin, eyes)
- Animations and behavior
- Gameplay stats
- Procedural sprite generation

#### DNA Parameter Types
- **Discrete (int)**: Variant categories (head shape: 0-5)
- **Scaled (int/float)**: Size ranges (leg length: 16-40px)
- **Boolean**: Feature toggles (has_tail: true/false)
- **Encoded**: Compact storage (4-bit hair color index)
- Beginning Gameplay stats
- Procedural sprite generation

#### DNA System (Component-Based)

- **`DNAStrand` Component**: Holds a unique `seed` integer for the NPC
- **Procedural Generation**: Seed creates all heritable traits deterministically
- **Procedural Sprites**: Advanced layered system constructing pixel art from DNA traits with the following features:

### Procedural Pixel Art Character System

#### Core Features

- **2D Skeleton Rigging**: Hierarchical bone system for natural movement
- **DNA-Based Variation**: Unique characters generated from genetic parameters
- **Directional Sprites**: 8-directional views with appropriate perspective
- **Layered Rendering**: Separate layers for body parts, clothing, and equipment

#### Visual Refinement

- **Symmetry Tightening**: Ensures balanced proportions while maintaining organic feel
- **Silhouette Smoothing**: Clean, readable outlines with anti-aliasing
- **Form Definition**: Clear shapes for heads (circular, square, bestial) and torsos
- **Connected Limbs**: Logical joint placement with smooth transitions
- **Polished Outlines**: Variable-weight outlines for depth and clarity

#### Facial Features (DNA-Controlled)

- **Mouth**:
  - Lip thickness (top/bottom)
  - Width
  - Expression parameters
- **Nose**:
  - Nostril size and shape
  - Tilt (up/down)
  - Dorsum protrusion
- **Eyes**:
  - Size and shape
  - Iris color and pattern
  - Angle and spacing
  - Eyelid coverage and shape

#### Body Structure

- **Head Shapes**: Circular, square, bestial variants
- **Torso Types**: Broad, narrow, muscular, lean
- **Limb Proportions**: Length, thickness, and muscle definition
- **Pose Variations**: Natural idle stances and movement patterns

#### Advanced Rendering

- **Cohesive Color Palettes**: Hue-shifted color schemes based on DNA
- **Directional Adaptation**:
  - Side-view adjustments (narrower profiles)
  - Head shifting for perspective
  - Limb scaling for depth
- **Lighting & Shading**:
  - Pseudo-3D depth with shadows
  - Ambient occlusion between body parts
  - Specular highlights on appropriate materials

#### Technical Implementation

- **Component-Based DNA**: Each visual trait controlled by genetic parameters
- **Procedural Animation**: Smooth transitions between poses
- **Pivot System**: Intelligent mirroring for symmetrical features
- **LOD Support**: Simplified sprites for distant characters
- **Cache System**: Optimized regeneration of character sprites

### Skills System

Skills are organized into categories and improve through use, with detailed relationships to core stats and needs:

#### Core Stat-Skill Relationships

**Stamina Skills:**
- **Farming**: Physical labor builds stamina, increases hunger tolerance
- **Fishing**: Casting and reeling increases stamina, delays thirst effects
- **Mining**: Physical exertion requires and builds stamina
- **Logging**: Cutting trees and hauling logs increases stamina
- **Foraging**: Traveling and searching boosts stamina
- **Combat**: Physical exertion in battles requires stamina maintenance
- **Smithing**: Continuous forge work demands stamina
- **Baking/Cooking**: Long cooking sessions help increase stamina
- **Healing**: Performing healing tasks over time builds stamina

**Strength Skills:**
- **Masonry**: Lifting heavy stones demands strength
- **Carpentry**: Handling large tools and materials requires strength
- **Earthwork**: Digging and moving earth demands strength
- **Mining**: Extracting ore requires significant strength
- **Logging**: Cutting trees and handling logs requires physical strength
- **Combat**: Direct fighting relies heavily on strength
- **Smithing**: Hammering metal requires considerable strength
- **Tanning**: Physical work in tanning hides requires strength
- **Tailoring**: Working with heavy fabrics may require strength
- **Alchemy**: Handling heavy ingredients requires strength

**Dexterity Skills:**
- **Design**: Requires precision and fine motor control
- **Carpentry**: Crafting detailed woodwork demands dexterity
- **Engineering**: Fine motor control for assembling machines
- **Taming**: Handling and training animals requires dexterity
- **Fishing**: Reeling in fish and handling gear requires dexterity
- **Logging**: Cutting trees with precision demands dexterity
- **Smithing**: Creating intricate items requires dexterous control
- **Tailoring**: Sewing and stitching require delicate movements
- **Crafting**: Fine motor control for detailed items
- **Marksmanship**: Aiming and shooting with precision demands dexterity
- **Strategy**: Mental dexterity in planning and decision-making
- **Spellcraft**: Fine manipulation of magic requires dexterous control
- **Runesmithing**: Crafting intricate runes requires fine dexterity
- **Navigation**: Dexterity in charting and movement
- **Vigilance**: Quick reactions to stimuli require dexterity

**Perception Skills:**
- **Foraging**: Requires keen observation to locate resources
- **Fishing**: Spotting fish and reacting to environmental changes
- **Mining**: Identifying ore veins and detecting potential resources
- **Logging**: Spotting the right trees and timber
- **Tracking**: Finding and following animal tracks
- **Navigation**: Understanding surroundings and directions
- **Vigilance**: Being alert to surroundings and threats
- **Charisma**: Interpreting others' feelings and adjusting interactions

**Willpower Skills:**
- **Masonry**: Mental focus and endurance for tough projects
- **Carpentry**: Stamina and focus over long hours of work
- **Mining**: Mental endurance to push through long, tough tasks
- **Combat**: Staying determined in battle, pushing through fatigue
- **Healing**: Persistence to help others in challenging conditions
- **Alchemy**: Maintaining focus during complex processes
- **Spellcraft**: Magical endeavors, particularly difficult spells
- **Accounting**: Keeping focused on calculations and management
- **Charisma**: Persuading and maintaining control in interactions System

Skills improve through use, with detailed relationships to core stats and needs.

#### Skill Categories

- **Survival Skills**: Foraging, Hunting, Fishing, Cooking, Shelter-building, Farming
- **Combat Skills**: Melee Combat, Archery, Defense, Tactics, Martial Arts
- **Crafting & Construction**: Woodworking, Stoneworking, Metalworking, Textile Crafting
- **Artisan Skills**: Painting, Writing, Sculpting, Music
- **Social & Communication**: Bartering, Leadership, Teaching, Diplomacy
- **Medical & Healing**: Herbalism, First Aid, Surgery, Midwifery
- **Mental & Spiritual**: Spiritual Healing, Meditation, Philosophy
- **Magical Skills**: Battle Magic, Divination, Alchemy, Enchanting

### Personality & Traits System

#### Trait Evolution by Age

- **Infant**: Temperament
- **Toddler**: Temperament + Socialization
- **Child**: (Temperament→Emotional) + Socialization + Cognition
- **Teenager**: Emotional + (Socialization→Interaction) + Cognition + Identity
- **Young Adult**: Emotional + Interaction + (Cognition→Ambition) + Identity + Morals
- **Adult**: Emotional + Interaction + Ambition + (Identity→Perspective) + Morals
- **Elder**: Emotional + Interaction + (Ambition→Legacy) + Perspective + Morals

### Job System

Characters can pursue various professions across categories, each requiring specific skills and providing unique benefits to the community:

#### 🏗️ Construction & Infrastructure

- **Architect**: Plans and surveys buildings and infrastructure
- **Stonemason**: Carves and lays stone for structures and roads
- **Woodworker**: Crafts and constructs buildings with wood
- **Earthworker**: Shapes mud, sand, and clay for construction and utilities
- **Engineer**: Constructs tunnels, roads, and other infrastructure

#### 🌾 Farming & Resource Gathering

- **Farmer**: Grows crops, manages food production, and tends orchards
- **Animal Trainer**: Tames and manages livestock, mounts, and working animals
- **Fisherman**: Catches and processes fish and other aquatic resources
- **Miner**: Extracts ores, gems, and minerals from the earth
- **Lumberjack**: Harvests trees and processes wood
- **Forager**: Gathers edible plants, mushrooms, herbs, and reeds

#### ⚒️ Crafting & Production

- **Blacksmith**: Forges metal tools, weapons, and armor
- **Glassmaker**: Creates glass goods from desert sand
- **Carpenter**: Builds boats and wooden equipment
- **Tanner**: Processes hides and crafts leather goods
- **Artisan**: Creates decorative and functional crafts like baskets, pottery, candles, soaps, and other related products
- **Tailor**: Creates clothing and textiles for the community

#### 🍞 Food & Drink

- **Brewer**: Makes alcoholic and non-alcoholic drinks like beer, wine, and juices
- **Baker**: Bakes bread, pastries, and other goods
- **Chef**: Prepares complex meals for individuals or groups

#### 🛡️ Defense & Warfare

- **Soldier**: Engages in combat, defense, and tactical operations
- **Scout**: Explores, tracks, and serves as an early warning system
- **Commander**: Leads troops, strategizes, and organizes defenses
- **Battle Mage**: Specializes in using destructive or protective spells in combat

#### 🛒 Trade & Communication

- **Merchant**: Sells goods within the settlement
- **Trader**: Facilitates trade, moving goods between settlements
- **Diplomat**: Negotiates alliances, peace, and trade agreements
- **Courier**: Delivers messages and goods across distances
- **Treasurer**: Manages and oversees the community's wealth and resources

#### 🧑‍⚕️ Medicine & Magic

- **Healer**: Uses medical and magical knowledge to treat injuries and diseases
- **Alchemist**: Mixes potions, poisons, and magical concoctions for various effects, including medicine
- **Medic Aide**: Supports healers with medical treatments and basic care
- **Shaman**: Uses spiritual and magical healing methods, guides rituals, and connects with the spirit world

#### 🎭 Arts & Culture

- **Bard**: Performs music, poetry, and storytelling to entertain and uplift
- **Performer**: Engages in theatrical performances, dances, and live shows
- **Scholar**: Studies and preserves knowledge, researching various disciplines
- **Librarian/Scribe**: Organizes and records knowledge, creates written records for future generations
- **Diviner**: Uses magic or spiritual practices to foresee the future or gain insight
- **Runesmith**: Crafts magical symbols and runes for enchantments and spells

#### 🌍 Exploration & Defense

- **Hunter**: Tracks and hunts animals for food and materials
- **Sailor/Navigator**: Manages ocean travel and shipbuilding
- **Watchman**: Monitors surroundings, provides security, and gathers intelligence

---

## 5. Clan Systems

### The Four Clans (from Division)

The world is organized into four major clans, each representing a broken virtue:

#### 🪨 Kharthis – The Earthbound Forge

Disciplined architects of the old world. They shape stone and steel with unmatched precision, and value order, legacy, and survival through structure. Their society is built on tradition, respect for lineage, and a relentless pursuit of durability—both physical and ideological.

- **Virtue**:
  - Discipline
  - Dominion
- **Core Roles**:
  - Toolmakers
  - Weaponeers
  - Builders
  - Engineers
  - Defenders
- **Stat Tendencies**:
  - Strength ++
  - Stamina +
  - Perception -
  - Dexterity --
- **Skill Focus**:
  - Smithing
  - Masonry
  - Carpentry
  - Earthwork
  - Melee Combat
  - Leadership
- **Trait Disposition**:
  - 🟡 Docile, Persistent, Grounded
  - 🌟 Consistent, Compassionate, Driven
  - 🔥 Rigid, Dogmatic under duress
- **Need Modifiers**:
  - Morale-dependant: productivity rises/falls with emotional state
  - Resistant to stress, enjoys routine
  - Emotionally brittle when ideals collapse
- **Philosophy**:
  - Order
  - Law
  - Permanence
  - Structure
- **Special**:
  - **Unyielding Ground** – Gains resilience bonuses when defending constructed areas or territory

#### 🌊 Olanthir – The Tide of Kindness

Soul-healers and green-fingered caretakers of the world. Their connection to nature and one another makes them gifted in medicine, agriculture, and interpersonal care. Pacifistic by nature, they wield empathy like others wield swords.

- **Virtue**:
  - Devotion
  - Dependency
- **Core Roles**:
  - Herbalists
  - Medics
  - Foragers
  - Animal Handlers
  - Counselors
- **Stat Tendencies**:
  - Willpower ++
  - Dexterity +
  - Strength -
  - Stamina --
- **Skill Focus**:
  - Healing
  - Spiritual Healing
  - Cooking
  - Foraging
  - Tailoring
  - Diplomacy
- **Trait Disposition**:
  - 🟡 Cooperative, Patient, Balanced
  - 🌟 Nurturing, Hopeful, Encouraging
  - 🔥 Insecure, Avoidant under conflict
- **Need Modifiers**:
  - Sensitive to social need decay
  - Natural morale and sanity regen in nature
  - Stress spikes in violent or chaotic environments
- **Philosophy**:
  - Harmony with nature
  - Cycles of life/death/rebirth
- **Special**:
  - **Circle of Grace** – Allies nearby recover health and morale faster when resting

#### 🔥 Draveth – The Ember Rebellion

Unstable geniuses with fire in their blood and drama in their souls. The Draveth thrive on chaos, creation, and catharsis. Artists, poets, and tactical madmen, they live fast, burn bright, and either build legends—or implode.

- **Virtue**:
  - Dreaming
  - Dissolution
- **Core Roles**:
  - Artists
  - Spellcasters
  - Guerrilla Warriors
  - Performers
  - Saboteurs
- **Stat Tendencies**:
  - Dexterity ++
  - Perception +
  - Willpower -
  - Stamina --
- **Skill Focus**:
  - Spellcraft
  - Performance
  - Crafting (Artistic)
  - Tactics
  - Deception
  - Persuasion
- **Trait Disposition**:
  - 🟡 Discerning, Strategic, Pragmatic
  - 🌟 Charismatic, Trailblazing, Visionary
  - 🔥 Manipulative, Overambitious, Envious
- **Need Modifiers**:
  - High morale swings (bonus or penalty)
  - Fast mana burn but rapid regen
  - Constant enjoyment drain when unstimulated
- **Philosophy**:
  - Chaos
  - Passion
  - Self-expression
  - Rebellion
- **Special**:
  - **Burning Brilliance** – Performance, combat, and spell bonuses scale with emotional intensity

#### 💨 Velunari – The Skyborne Thinkers

Detached, cerebral, and deeply spiritual, the Velunari commune with stars, numbers, and the invisible threads of fate. They are the world's diviners, mathematicians, and quiet prophets, often overlooked—until they predict your demise.

- **Virtue**:
  - Discernment
  - Desolation
- **Core Roles**:
  - Astrologers
  - Diviners
  - Scholars
  - Inventors
  - Spiritual Guides
- **Stat Tendencies**:
  - Perception ++
  - Willpower +
  - Strength -
  - Stamina --
- **Skill Focus**:
  - Alchemy
  - Spellcraft
  - Divination
  - Observation
  - Navigation
  - Accounting
- **Trait Disposition**:
  - 🟡 Evaluative, Methodical, Temperate
  - 🌟 Astute, Enlightened, Inclusive
  - 🔥 Cynical, Pessimistic, Inflexible
- **Need Modifiers**:
  - High focus regeneration
  - Extremely fragile to physical harm
  - Resistant to magical/sanity drain effects
- **Philosophy**:
  - Cosmic order
  - Knowledge
  - Precision
- **Special**:
  - **Astral Clarity** – Periodic insights grant tactical foresight or bonus outcomes during rituals

### Core Narrative

The Duskbourne daughter has delivered the dominion into discord, dividing the world into sacred schisms. Each clan bears a broken virtue, now twisted:

- **Devotion** → Dependency
- **Discipline** → Dominion
- **Dreaming** → Dissolution
- **Discernment** → Desolation

---

## 6. Gameplay Mechanics

# 🧮 Action Effect System Formulas

**1. Stat → Speed Modifier**
```python
ModifiedDuration = BaseDuration × (1 – floor(Stat ÷ 40) × 0.5)
```

- Stat 0–39 → no speed boost
- Stat 40–79 → 50% faster
- Stat 80+ → 100% faster

**2. Skill → Potency & Success**
```python
ModifiedChange = BaseChange × (1 + floor(Skill ÷ 40) × 0.25)
Roll = d20 + floor(Skill ÷ 20) vs DC 12
```

- Success → 100% effect
- Fail → 75%
- Crit Success → 150%
- Crit Fail → 50%

---

# About the Action Table

This section explains how to read and use the Action Table in your design document. The table captures every in-game action’s key attributes—stats, skills, descriptions, and their mechanical impact on character needs—so you can balance pacing and progression at a glance.

---

## 1. Table Columns

| Column            | What It Means                                                                                          |
|-------------------|---------------------------------------------------------------------------------------------------------|
| **Action**        | Name of the in-game activity (e.g. Cook, Run, Attack).                                                  |
| **Primary Stat(s)**  | The attribute(s) governing how fast the action completes (reduces Base Duration).                       |
| **Relevant Skill(s)**| The skill(s) determining how strong the effect is and the chance of success or failure.                |
| **Description**   | A short, human-readable summary of what the action does.                                                |
| **Needs Affected**| Which needs (Hunger, Fatigue, Mana, etc.) change when the action runs.                                   |
| **Base Change**   | The raw percentage each need gains or loses before modifiers.                                            |
| **Base Duration** | How many minutes it takes to apply the full Base Change.                                                 |
| **Rate per Tick** | The change per game tick (assuming 1 tick = 10 minutes) = Base Change ÷ (Base Duration ÷ 10).             |

---

## 2. How to Read a Row

1. **Locate the Action**
   Find “Cook” in the Action column.

2. **Check Stats & Skills**
   - Primary Stat: Focus (affects speed)
   - Relevant Skill: Cooking (affects potency & success)

3. **Understand the Description**
   “Prepare meals from ingredients.”

4. **See Mechanical Impact**
   - Needs Affected: Hunger +10%, Fatigue –2%
   - Base Duration: 10 min
   - Rate per Tick: +10% Hunger & –2% Fatigue per 10-minute tick

---

## 3. Example Walkthrough

Imagine a character (Focus 60, Cooking 80) uses **Cook**:

1. **Find Cook’s Row**
   - Base Change: +10% Hunger, –2% Fatigue
   - Base Duration: 10 min

2. **Apply Stat → Speed**
   ```python
   ModifiedDuration = 10 × (1 – floor(60÷40)×0.5)
                    = 10 × (1 – 1×0.5)
                    = 5 minutes
   ```

3. **Apply Skill → Potency**
   ```python
   ModifiedChange = 10% × (1 + floor(80÷40)×0.25)
                  = 10% × (1 + 2×0.25)
                  = 15% Hunger
   ```

4. **Resolve Success Roll**
   ```python
   Roll = d20 + floor(80÷20) = d20 + 4 vs DC 12
   • Success → +15% in 5 min
   • Fail    → 75% of 15% = +11.25%
   • Crit    → 150% or 50% of modified change
   ```

---

## 4. Why the Table Matters

- **Clarity:** All actions and their mechanical effects live in one place.
- **Balance:** Adjust Base Change and Duration to fine-tune pacing.
- **Progression:** Stats shorten durations; skills boost effects, giving players meaningful growth.
- **Transparency:** Designers and modders can immediately see how any action interacts with needs.

Use this guide alongside the full Action Table to quickly design, review, and balance every action in your simulation.

# 📊 Full Action Table by Category

## Movement

| Action | Primary Stat(s)        | Relevant Skill(s) | Description                                | Need(s) Affected          | Base Change     | Base Duration | Rate per Tick   |
|--------|------------------------|-------------------|--------------------------------------------|---------------------------|-----------------|---------------|-----------------|
| Walk   | Dexterity             | —                 | Move to a nearby tile.                     | Fatigue –2%, Thirst –1.5% | –2%, –1.5%      | 10 min        | –2%, –1.5%      |
| Run    | Stamina, Endurance    | —                 | Move quickly over longer distances.        | Fatigue –5%, Thirst –3%, Hunger –1.5% | –5%, –3%, –1.5% | 10 min        | –5%, –3%, –1.5% |
| Jump   | Dexterity, Stamina    | —                 | Traverse gaps or obstacles.                | Fatigue –3%               | –3%             | 5 min         | –6%             |
| Climb  | Endurance, Strength   | —                 | Ascend or descend elevated terrain.        | Fatigue –4%, Stress +2%   | –4%, +2%        | 10 min        | –4%, +2%        |
| Crouch | Dexterity             | Stealth           | Move stealthily or enter tight spaces.     | Fatigue –1%, Stress –2%   | –1%, –2%        | 5 min         | –2%, –4%        |
| Carry  | Strength              | —                 | Transport heavy objects.                   | Fatigue –6%, Hunger –2%   | –6%, –2%        | 10 min        | –6%, –2%        |

---

## Interaction

| Action  | Primary Stat(s)        | Relevant Skill(s)           | Description                                         | Need(s) Affected         | Base Change       | Base Duration | Rate per Tick   |
|---------|-------------------------|-----------------------------|-----------------------------------------------------|--------------------------|-------------------|---------------|-----------------|
| Inspect | Perception              | Foraging, Observation       | Examine terrain, objects, or creatures for details. | Focus –3%, Motivation +2% | –3%, +2%         | 10 min        | –3%, +2%        |
| Pick Up | Dexterity               | —                           | Collect or take an item.                            | Fatigue –1%               | –1%               | 2 min         | –5%             |
| Use     | Dexterity               | —                           | Interact with tools, levers, doors, etc.            | Contextual                | Varies            | Varies        | Varies          |
| Speak   | Willpower               | Conversation, Charisma      | Initiate dialogue with NPCs.                        | Social +5%, Morale +2%    | +5%, +2%          | 5 min         | +10%, +4%       |
| Trade   | Perception, Conviction  | Bartering, Negotiation      | Exchange goods with NPCs.                           | Social +3%, Morale +2%    | +3%, +2%          | 10 min        | +3%, +2%        |

---

## Combat

| Action           | Primary Stat(s)             | Relevant Skill(s)               | Description                                 | Need(s) Affected                   | Base Change           | Base Duration | Rate per Tick     |
|------------------|-----------------------------|---------------------------------|---------------------------------------------|------------------------------------|-----------------------|---------------|-------------------|
| Attack           | Strength, Dexterity, Power | Melee Combat, Archery, Martial Arts | Perform a melee or ranged offensive move. | Fatigue –8%, Stress +4%, Hunger –2% | –8%, +4%, –2%         | 10 min        | –8%, +4%, –2%     |
| Defend           | Strength, Tenacity         | Defense                         | Block or reduce incoming damage.           | Fatigue –4%, Stress +2%            | –4%, +2%              | 5 min         | –8%, +4%          |
| Dodge            | Dexterity, Perception      | Reflex, Martial Arts            | Evade an incoming attack.                  | Fatigue –3%, Stress +3%            | –3%, +3%              | 5 min         | –6%, +6%          |
| Special Ability  | Varies                     | Spellcraft, Tactics             | Use a unique power, spell, or technique.   | Mana –10%, Stress +5%              | –10%, +5%             | 5 min         | –10%, +5%         |
| Equip/Swap       | Dexterity                  | —                               | Change weapons or tools during an encounter. | Fatigue –1%                        | –1%                   | 2 min         | –5%               |

---

## Utility

| Action  | Primary Stat(s)         | Relevant Skill(s)                          | Description                              | Need(s) Affected         | Base Change       | Base Duration | Rate per Tick   |
|---------|--------------------------|--------------------------------------------|------------------------------------------|--------------------------|-------------------|---------------|-----------------|
| Craft   | Focus, Dexterity        | Crafting, Smithing, Tailoring, Alchemy     | Create items from materials.             | Fatigue –6%, Focus –4%    | –6%, –4%          | 15 min        | –4%, –2.67%     |
| Heal    | Vitality, Willpower     | First Aid, Spiritual Healing, Alchemy      | Restore health using medicine or magic.  | Health +10%, Fatigue –3%  | +10%, –3%         | 10 min        | +10%, –3%       |
| Rest    | Vitality                | —                                          | Recover stamina and health in safe areas. | Fatigue +15%, Health +5%  | +15%, +5%         | 30 min        | +5%, +1.67%     |
| Signal  | Willpower, Perception   | Tactics, Communication                     | Call allies or mark a location.          | Morale +3%, Focus +2%     | +3%, +2%          | 5 min         | +6%, +4%        |

---

## Social

| Action    | Primary Stat(s)           | Relevant Skill(s)         | Description                             | Need(s) Affected          | Base Change       | Base Duration | Rate per Tick   |
|-----------|---------------------------|---------------------------|-----------------------------------------|---------------------------|-------------------|---------------|-----------------|
| Befriend  | Willpower, Conviction    | Diplomacy, Empathy        | Build rapport and alliances.            | Social +10%, Morale +5%    | +10%, +5%         | 20 min        | +5%, +2.5%      |
| Intimidate| Strength, Conviction     | Leadership                | Influence others through fear or dominance. | Morale –5%, Stress +5%   | –5%, +5%          | 10 min        | –5%, +5%        |
| Persuade  | Willpower, Conviction    | Negotiation, Bartering    | Convince someone to act or agree.       | Motivation +5%, Morale +3% | +5%, +3%          | 10 min        | +5%, +3%        |
| Lie       | Willpower, Perception    | Deception                 | Deceive someone to manipulate a situation. | Morale –2%, Stress +4%  | –2%, +4%          | 5 min         | –4%, +8%        |
| Form Bond | Willpower, Conviction    | Empathy, Charisma         | Establish a close relationship or alliance. | Social +15%, Motivation +10% | +15%, +10%      | 30 min        | +5%, +3.33%     |

---

## Tactical

| Action     | Primary Stat(s)          | Relevant Skill(s)       | Description                             | Need(s) Affected          | Base Change       | Base Duration | Rate per Tick   |
|------------|--------------------------|-------------------------|-----------------------------------------|---------------------------|-------------------|---------------|-----------------|
| Wait       | Willpower                | —                       | Delay action until a strategic moment.  | Stress –2%                | –2%               | 5 min         | –4%             |
| Prepare    | Focus, Insight           | Tactics                 | Ready a weapon, item, or stance.        | Focus +5%, Motivation +2% | +5%, +2%          | 10 min        | +5%, +2%        |
| Distract   | Dexterity, Perception    | Stealth, Performance    | Divert enemy attention or confuse others. | Stress –3%, Morale +2%  | –3%, +2%          | 5 min         | –6%, +4%        |
| Camouflage | Dexterity, Insight       | Stealth                 | Blend in to avoid detection.            | Stress –4%, Focus +2%     | –4%, +2%          | 10 min        | –4%, +2%        |

---

## Construction

| Action   | Primary Stat(s)         | Relevant Skill(s)                   | Description                              | Need(s) Affected          | Base Change       | Base Duration | Rate per Tick   |
|----------|-------------------------|-------------------------------------|------------------------------------------|---------------------------|-------------------|---------------|-----------------|
| Build    | Strength, Endurance     | Masonry, Carpentry, Engineering     | Construct structures using materials.    | Fatigue –7%, Hunger –3%    | –7%, –3%          | 10 min        | –7%, –3%        |
| Repair   | Dexterity, Strength     | Engineering, Masonry                | Fix damaged structures or equipment.     | Fatigue –5%, Focus –2%     | –5%, –2%          | 10 min        | –5%, –2%        |
| Survey   | Insight, Perception     | Design, Architecture                | Plan layouts and improvements.           | Focus –3%, Motivation +2%  | –3%, +2%          | 10 min        | –3%, +2%        |
| Excavate | Strength, Stamina       | Earthwork                           | Dig terrain or tunnels.                  | Fatigue –6%, Hunger –2%    | –6%, –2%          | 10 min        | –6%, –2%        |

---

## Resource

| Action  | Primary Stat(s)          | Relevant Skill(s)             | Description                           | Need(s) Affected           | Base Change       | Base Duration | Rate per Tick   |
|---------|--------------------------|-------------------------------|---------------------------------------|----------------------------|-------------------|---------------|-----------------|
| Plant   | Dexterity, Focus         | Farming                       | Grow crops, trees, or herbs.          | Motivation +3%, Hunger –2%  | +3%, –2%          | 10 min        | +3%, –2%        |
| Harvest | Dexterity, Perception    | Farming, Foraging             | Collect crops or plants.              | Hunger +5%, Fatigue –2%     | +5%, –2%          | 10 min        | +5%, –2%        |
| Tame    | Willpower, Dexterity     | Taming                        | Train and domesticate animals.        | Motivation +5%, Social +5%  | +5%, +5%          | 15 min        | +3.33%, +3.33%  |
| Hunt    | Perception, Dexterity    | Tracking, Archery, Combat     | Track and kill wild animals.          | Hunger +10%, Fatigue –5%, Stress +3% | +10%, –5%, +3% | 15 min        | +6.67%, –3.33%, +2% |
| Fish    | Dexterity, Perception    | Fishing                       | Catch aquatic resources.              | Hunger +8%, Fatigue –3%     | +8%, –3%          | 15 min        | +5.33%, –2%     |
| Mine    | Strength, Endurance      | Mining                        | Extract minerals or stone.            | Fatigue –6%, Hunger –3%     | –6%, –3%          | 10 min        | –6%, –3%        |
| Chop    | Strength, Dexterity      | Logging                       | Cut down trees.                       | Fatigue –5%, Hunger –2%     | –5%, –2%          | 10 min        | –5%, –2%        |
| Gather  | Dexterity, Perception    | Foraging                      | Collect herbs or mushrooms.           | Hunger +5%, Fatigue –2%     | +5%, –2%          | 10 min        | +5%, –2%        |

---

## Crafting

| Action    | Primary Stat(s)         | Relevant Skill(s)                   | Description                             | Need(s) Affected         | Base Change       | Base Duration | Rate per Tick   |
|-----------|-------------------------|-------------------------------------|-----------------------------------------|--------------------------|-------------------|---------------|-----------------|
| Forge     | Strength, Focus         | Smithing                            | Create tools, weapons, and armor.       | Fatigue –6%, Focus –3%    | –6%, –3%          | 15 min        | –4%, –2%        |
| Carve     | Dexterity, Focus        | Carpentry, Crafting                 | Shape wood into tools or art.           | Fatigue –5%, Enjoyment +3% | –5%, +3%          | 15 min        | –3.33%, +2%     |
| Weave     | Dexterity, Focus        | Tailoring, Weaving                  | Create textiles and clothing.           | Fatigue –4%, Comfort +3%  | –4%, +3%          | 15 min        | –2.67%, +2%     |
| Tinker    | Dexterity, Insight      | Crafting, Tinkering                 | Improve or repair items.                | Focus –3%, Motivation +2% | –3%, +2%          | 10 min        | –3%, +2%        |
| Refine    | Focus, Dexterity        | Tanning, Glasswork, Metallurgy      | Process raw materials.                  | Fatigue –5%, Hunger –2%   | –5%, –2%          | 15 min        | –3.33%, –1.33%  |
| Assemble  | Dexterity, Focus        | Engineering, Crafting               | Fit components together to create a whole. | Fatigue –4%, Focus –2%  | –4%, –2%          | 10 min        | –4%, –2%        |

---

## Consumable

| Action | Primary Stat(s)         | Relevant Skill(s)       | Description                                      | Need(s) Affected           | Base Change       | Base Duration | Rate per Tick   |
|--------|-------------------------|-------------------------|--------------------------------------------------|----------------------------|-------------------|---------------|-----------------|
| Cook   | Focus, Dexterity        | Cooking                 | Prepare meals from ingredients.                  | Hunger +10%, Fatigue –2%   | +10%, –2%         | 10 min        | +10%, –2%       |
| Bake   | Focus, Dexterity        | Baking                  | Make baked goods.                                | Hunger +10%, Fatigue –2%   | +10%, –2%         | 10 min        | +10%, –2%       |
| Brew   | Focus, Willpower        | Brewing, Alchemy        | Create drinks (alcoholic or magical).            | Mana +10%, Hunger +5%      | +10%, +5%         | 15 min        | +6.67%, +3.33%  |

---

## Daily Life

| Action    | Primary Stat(s)          | Relevant Skill(s)      | Description                                        | Need(s) Affected         | Base Change       | Base Duration | Rate per Tick   |
|-----------|--------------------------|------------------------|----------------------------------------------------|--------------------------|-------------------|---------------|-----------------|
| Clean     | Dexterity, Willpower     | —                      | Maintain hygiene and order.                        | Hygiene +15%, Comfort +5% | +15%, +5%        | 15 min        | +10%, +3.33%    |
| Organize  | Insight, Dexterity       | Logistics              | Manage and sort inventory.                         | Motivation +5%, Focus –2% | +5%, –2%         | 10 min        | +5%, –2%        |
| Care      | Vitality, Willpower      | Healing, Nurturing     | Tend to others’ well-being.                        | Health +10%, Social +5%   | +10%, +5%        | 15 min        | +6.67%, +3.33%  |
| Socialize | Willpower, Conviction    | Charisma, Conversation | Casual interaction.                                | Social +10%, Morale +5%   | +10%, +5%        | 20 min        | +5%, +2.5%      |
| Teach     | Insight, Willpower       | Mentorship, Instruction | Instruct or mentor another.                        | Motivation +5%, Focus –2% | +5%, –2%         | 15 min        | +3.33%, –1.33%  |
| Work      | Varies                   | Varies (job-dependent)  | Perform job-related tasks based on profession.     | Fatigue –6%, Motivation +4% | –6%, +4%        | 15 min        | –4%, +2.67%     |

---

## Warfare

| Action      | Primary Stat(s)          | Relevant Skill(s)      | Description                                  | Need(s) Affected      | Base Change       | Base Duration | Rate per Tick   |
|-------------|--------------------------|------------------------|----------------------------------------------|-----------------------|-------------------|---------------|-----------------|
| Strategize  | Insight, Willpower       | Tactics, Strategy      | Plan battles or defenses.                    | Stress –5%, Focus –3% | –5%, –3%          | 20 min        | –2.5%, –1.5%    |
| Scout       | Perception, Dexterity    | Navigation, Tracking   | Survey areas or track targets.               | Fatigue –4%, Focus –2% | –4%, –2%         | 10 min        | –4%, –2%        |

---

## Trade

| Action   | Primary Stat(s)         | Relevant Skill(s)         | Description                                            | Need(s) Affected        | Base Change       | Base Duration | Rate per Tick   |
|----------|-------------------------|---------------------------|--------------------------------------------------------|-------------------------|-------------------|---------------|-----------------|
| Haggle   | Conviction, Perception  | Bartering, Negotiation    | Negotiate better deals.                                | Social +5%, Morale +3%  | +5%, +3%          | 10 min        | +5%, +3%        |
| Deliver  | Endurance, Dexterity    | Logistics                 | Transport items or messages.                           | Fatigue –5%, Hunger –2% | –5%, –2%         | 10 min        | –5%, –2%        |
| Manage   | Insight, Conviction     | Accounting, Leadership    | Oversee economic or settlement resources.              | Motivation +5%, Stress –2% | +5%, –2%      | 15 min        | +3.33%, –1.33%  |

---

## Magic

| Action      | Primary Stat(s)     | Relevant Skill(s)       | Description                                            | Need(s) Affected        | Base Change     | Base Duration | Rate per Tick     |
|-------------|---------------------|-------------------------|--------------------------------------------------------|-------------------------|-----------------|---------------|-------------------|
| Cast Spell  | Willpower, Focus    | Spellcraft              | Use magic to influence events and characters.          | Mana –10%, Stress +2%   | –10%, +2%       | 5 min         | –10%, +2%         |
| Mix         | Focus, Dexterity    | Alchemy, Herbalism      | Brew potions or magical concoctions.                   | Mana +10%, Hunger +5%   | +10%, +5%       | 15 min        | +6.67%, +3.33%    |
| Enchant     | Focus, Willpower    | Spellcraft, Runesmithing| Imbue objects with magical power.                      | Mana –5%, Motivation +5%| –5%, +5%        | 15 min        | –3.33%, +3.33%    |
| Divine      | Insight, Willpower  | Divination              | Seek insight through magical means.                    | Stress –5%, Focus +5%   | –5%, +5%        | 15 min        | –3.33%, +3.33%    |

---

## Arts & Culture

| Action  | Primary Stat(s)       | Relevant Skill(s)     | Description                        | Need(s) Affected         | Base Change     | Base Duration | Rate per Tick    |
|---------|-----------------------|-----------------------|------------------------------------|--------------------------|-----------------|---------------|------------------|
| Perform | Dexterity, Conviction | Performance           | Sing, dance, or entertain others.  | Enjoyment +15%, Morale +5%| +15%, +5%       | 30 min        | +5%, +1.67%      |
| Write   | Insight, Focus        | Writing, Curation     | Record knowledge or stories.       | Motivation +5%, Focus –2%| +5%, –2%        | 15 min        | +3.33%, –1.33%   |
| Study   | Insight, Willpower    | Scholarship           | Gain knowledge or improve skills.  | Motivation +5%, Focus –2%| +5%, –2%        | 15 min        | +3.33%, –1.33%   |

---

## Exploration

| Action    | Primary Stat(s)        | Relevant Skill(s)   | Description                         | Need(s) Affected         | Base Change     | Base Duration | Rate per Tick  |
|-----------|------------------------|---------------------|-------------------------------------|--------------------------|-----------------|---------------|----------------|
| Track     | Perception, Insight    | Tracking            | Follow signs of movement.           | Fatigue –4%, Focus –3%   | –4%, –3%        | 10 min        | –4%, –3%       |
| Navigate  | Insight, Dexterity     | Navigation          | Guide travel by land or sea.        | Fatigue –3%, Focus –2%   | –3%, –2%        | 10 min        | –3%, –2%       |
| Watch     | Perception, Willpower  | Vigilance           | Observe surroundings for threats.   | Stress –3%, Focus +2%    | –3%, +2%        | 10 min        | –3%, +2%       |

---

## Cognitive & Behavioral

| Action   | Primary Stat(s) | Relevant Skill(s)           | Description                                                                          |
|----------|-----------------|-----------------------------|--------------------------------------------------------------------------------------|
| Desire   | Willpower       | Motivation, Ambition        | (Internal) Generates needs and goals.                                                |
| Remember | Insight         | Introspection, Scholarship  | (Internal) Logs experiences to memory; influences future decisions.                  |
| Decide   | Insight         | Strategy, Tactics           | (Internal) Chooses an action based on Desire and Memory.                             |
| Plan     | Insight         | Strategy, Organization      | (Internal) Creates a sequence of actions to achieve a goal set by Decide.            |
| Forget   | Willpower       | Focus, Introspection        | (Internal) Purges low-value or traumatic memories to maintain mental stability.      |
| Learn    | Insight, Willpower | Scholarship, Socialization | (Internal) Acquires knowledge or skills from context or teaching.                    |

---

## Social (Advanced)

| Action     | Primary Stat(s)        | Relevant Skill(s)         | Description                                         | Need(s) Affected          | Base Change     | Base Duration | Rate per Tick   |
|------------|------------------------|---------------------------|-----------------------------------------------------|---------------------------|-----------------|---------------|-----------------|
| Reproduce  | Vitality, Willpower    | Nurturing, Empathy        | Create offspring with a bonded partner. Passes on DNA and some memories. | (Internal)               | —               | —             | —               |
| Flee       | Dexterity, Endurance   | Reflex, Survival          | Escape from danger or conflict.                     | Fatigue –5%, Stress +4%   | –5%, +4%        | 10 min        | –5%, +4%        |
| Steal      | Dexterity, Perception  | Stealth, Deception        | Take an item without permission.                    | Fatigue –2%, Stress +4%   | –2%, +4%        | 5 min         | –4%, +8%        |
| Give Item  | Willpower, Dexterity   | Empathy, Bartering        | Voluntarily hand over an object.                    | Social +5%, Morale +2%    | +5%, +2%        | 2 min         | +10%, +4%       |
| Observe    | Perception, Insight    | Observation, Vigilance    | Watch or listen to targets to gather info.          | Focus –3%, Motivation +2% | –3%, +2%        | 10 min        | –3%, +2%        |
| Hide Item  | Dexterity, Insight     | Stealth, Deception        | Conceal objects from others.                        | Stress –2%, Comfort +3%   | –2%, +3%        | 10 min        | –2%, +3%        |

### Action System

Characters can perform various actions across multiple categories with detailed stat-skill relationships.

| Category | Action | Primary Stat(s) | Relevant Skill(s) | Description / Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Movement** | Walk | Dexterity | — | Move to a nearby tile. |
| | Run | Stamina, Endurance | — | Move quickly over longer distances. |
| | Jump | Dexterity, Stamina | — | Traverse gaps or obstacles. |
| | Climb | Endurance, Strength | — | Ascend or descend elevated terrain. |
| | Crouch | Dexterity | Stealth | Move stealthily or enter tight spaces. |
| | Carry | Strength | — | Transport heavy objects. |
| **Interaction** | Inspect | Perception | Foraging, Observation | Examine terrain, objects, or creatures for details. |
| | Pick Up | Dexterity | — | Collect or take an item. |
| | Use | Dexterity | — | Interact with tools, levers, doors, etc. |
| | Speak | Willpower | Conversation, Charisma | Initiate dialogue with NPCs. |
| | Trade | Perception, Conviction | Bartering, Negotiation | Exchange goods with NPCs. |
| **Combat** | Attack | Strength, Dexterity, Power | Melee Combat, Archery, Martial Arts | Perform a melee or ranged offensive move. |
| | Defend | Strength, Tenacity | Defense | Block or reduce incoming damage. |
| | Dodge | Dexterity, Perception | Reflex, Martial Arts | Evade an incoming attack. |
| | Special Ability | Varies | Spellcraft, Tactics | Use a unique power, spell, or technique. |
| | Equip/Swap | Dexterity | — | Change weapons or tools during an encounter. |
| **Utility** | Craft | Focus, Dexterity | Crafting, Smithing, Tailoring, Alchemy | Create items from materials. |
| | Heal | Vitality, Willpower | First Aid, Spiritual Healing, Alchemy | Restore health using medicine or magic. |
| | Rest | Vitality | — | Recover stamina and health in safe areas. |
| | Signal | Willpower, Perception | Tactics, Communication | Call allies or mark a location. |
| **Social** | Befriend | Willpower, Conviction | Diplomacy, Empathy | Build rapport and alliances. |
| | Intimidate | Strength, Conviction | Leadership | Influence others through fear or dominance. |
| | Persuade | Willpower, Conviction | Negotiation, Bartering | Convince someone to act or agree. |
| | Lie | Willpower, Perception | Deception | Deceive someone to manipulate a situation. |
| | **Form Bond** | Willpower, Conviction | Empathy, Charisma | Establish a close relationship or alliance. |
| **Tactical** | Wait | Willpower | — | Delay action until a strategic moment. |
| | Prepare | Focus, Insight | Tactics | Ready a weapon, item, or stance. |
| | Distract | Dexterity, Perception | Stealth, Performance | Divert enemy attention or confuse others. |
| | Camouflage | Dexterity, Insight | Stealth | Blend in to avoid detection. |
| **Construction** | Build | Strength, Endurance | Masonry, Carpentry, Engineering | Construct structures using materials. |
| | Repair | Dexterity, Strength | Engineering, Masonry | Fix damaged structures or equipment. |
| | Survey | Insight, Perception | Design, Architecture | Plan layouts and improvements. |
| | Excavate | Strength, Stamina | Earthwork | Dig terrain or tunnels. |
| **Resource** | Plant | Dexterity, Focus | Farming | Grow crops, trees, or herbs. |
| | Harvest | Dexterity, Perception | Farming, Foraging | Collect crops or plants. |
| | Tame | Willpower, Dexterity | Taming | Train and domesticate animals. |
| | Hunt | Perception, Dexterity | Tracking, Archery, Combat | Track and kill wild animals. |
| | Fish | Dexterity, Perception | Fishing | Catch aquatic resources. |
| | Mine | Strength, Endurance | Mining | Extract minerals or stone. |
| | Chop | Strength, Dexterity | Logging | Cut down trees. |
| | Gather | Dexterity, Perception | Foraging | Collect herbs or mushrooms. |
| **Crafting** | Forge | Strength, Focus | Smithing | Create tools, weapons, and armor. |
| | Carve | Dexterity, Focus | Carpentry, Crafting | Shape wood into tools or art. |
| | Weave | Dexterity, Focus | Tailoring, Weaving | Create textiles and clothing. |
| | Tinker | Dexterity, Insight | Crafting, Tinkering | Improve or repair items. |
| | Refine | Focus, Dexterity | Tanning, Glasswork, Metallurgy | Process raw materials. |
| | Assemble | Dexterity, Focus | Engineering, Crafting | Fit components together to create a whole. |
| **Consumable** | Cook | Focus, Dexterity | Cooking | Prepare meals from ingredients. |
| | Bake | Focus, Dexterity | Baking | Make baked goods. |
| | Brew | Focus, Willpower | Brewing, Alchemy | Create drinks (alcoholic or magical). |
| **Daily Life** | Clean | Dexterity, Willpower | — | Maintain hygiene and order. |
| | Organize | Insight, Dexterity | Logistics | Manage and sort inventory. |
| | Care | Vitality, Willpower | Healing, Nurturing | Tend to others’ well-being. |
| | Socialize | Willpower, Conviction | Charisma, Conversation | Casual interaction. |
| | Teach | Insight, Willpower | Mentorship, Instruction | Instruct or mentor another. |
| | Work | Varies | Varies (job-dependent) | Perform job-related tasks based on profession. |
| **Warfare** | Strategize | Insight, Willpower | Tactics, Strategy | Plan battles or defenses. |
| | Scout | Perception, Dexterity | Navigation, Tracking | Survey areas or track targets. |
| **Trade** | Haggle | Conviction, Perception | Bartering, Negotiation | Negotiate better deals. |
| | Deliver | Endurance, Dexterity | Logistics | Transport items or messages. |
| | Manage | Insight, Conviction | Accounting, Leadership | Oversee economic or settlement resources. |
| **Magic** | Cast Spell | Willpower, Focus | Spellcraft | Use magic to influence events & characters. |
| | Mix | Focus, Dexterity | Alchemy, Herbalism | Brew potions or magical concoctions. |
| | Enchant | Focus, Willpower | Spellcraft, Runesmithing | Imbue objects with magical power. |
| | Divine | Insight, Willpower | Divination | Seek insight through magical means. |
| **Arts & Culture**| Perform | Dexterity, Conviction | Performance | Sing, dance, or entertain others. |
| | Write | Insight, Focus | Writing, Curation | Record knowledge or stories. |
| | Study | Insight, Willpower | Scholarship | Gain knowledge or improve skills. |
| **Exploration** | Track | Perception, Insight | Tracking | Follow signs of movement. |
| | Navigate | Insight, Dexterity | Navigation | Guide travel by land or sea. |
| | Watch | Perception, Willpower | Vigilance | Observe surroundings for threats. |
| **Cognitive & Behavioral** | **Desire** | Willpower | Motivation, Ambition | **(Internal)** The engine for all behavior. Generates needs and goals. |
| | **Remember** | Insight | Introspection, Scholarship | **(Internal)** Logs experiences to memory. Influences future decisions. |
| | **Decide** | Insight | Strategy, Tactics | **(Internal)** Chooses an action from available options based on Desire and Memory. |
| | **Plan** | Insight | Strategy, Organization | **(Internal)** Creates a sequence of actions to achieve a goal set by Decide. |
| | **Forget** | Willpower | Focus, Introspection | **(Internal)** Purges low-value or traumatic memories to maintain mental stability. |
| | **Learn** | Insight, Willpower | Scholarship, Socialization | Acquire knowledge or skills from context or teaching. |
| **Social (Advanced)** | **Reproduce** | Vitality, Willpower | Nurturing, Empathy | Create offspring with a bonded partner. Passes on DNA and some memories. |
| | Flee | Dexterity, Endurance | Reflex, Survival | Escape from danger or conflict. |
| | Steal | Dexterity, Perception | Stealth, Deception | Take an item without permission. |
| | Give Item | Willpower, Dexterity | Empathy, Bartering | Voluntarily hand over an object. |
| | Observe | Perception, Insight | Observation, Vigilance | Watch or listen to targets to gather info. |
| | Hide Item | Dexterity, Insight | Stealth, Deception | Conceal objects from others. |

### Combat System

- **Turn-based tactical combat**
- **Action point system** for movement and abilities
- **Environmental interactions** and hazards
- **Status effects** and conditions
- **Equipment-based** damage and defense

---

## 7. Magic & Addiction Systems

### Magic System

- **Integral**: Magic is scarce and valuable, and only the most powerful agents of the four clans are able to access it.
- **`Magic` Component**: Holds `mana_current`, `mana_max`, `known_spells`
- **Mana Systems**: Regenerating pool influenced by rest, meditation, clan bonuses
- **Spell Components**: Defined by element, type, mana cost, effects
- **Magical Progression**: Skills improve through use, unlocking powerful spells

### Potion Use & Addiction System

- **Powerful Effects**: Potions provide significant boosts (stats, healing, mana, resistance)
- **Addictive Risk**: Realistic addiction mechanics based on frequency and type
- **`Addiction` Component**: Tracks substance, level, withdrawal timer, craving intensity
- **Consequences**: Affects stats, behavior, relationships, and clan dynamics
- **Strategic Depth**: Risk-reward decisions for immediate benefits vs. long-term dependency
Mana Addiction System
Overview

In Duskbourne Divine, mana is both a divine gift and a corrupting force, a power that elevates and enslaves those who wield it. The Mana Addiction System models the psychological and physical dependency that emerges from repeated mana use, creating a gameplay loop of temptation and consequence. Characters progress through five escalating levels of addiction—Reliance, Habituation, Dependency, Subjugation, and Obsession—each tied to usage frequency and duration. This system balances fleeting benefits (mental clarity, physical vigor) during and briefly after mana use with severe, lasting penalties (magical strain, stat loss) during active dependency and withdrawal. The result is a ritual of risk: mana offers power and transcendence, but at the cost of body, mind, and autonomy.

Core Mechanics

Addiction Progression: Addiction level increases based on frequency and consecutive days of mana use (specific triggers TBD, e.g., X uses per week or Y consecutive days). Levels escalate from 1 (Reliance) to 5 (Obsession), with each level requiring more sustained use to advance.
Level Decay and Withdrawal: Addiction levels decay after periods of non-use (e.g., 10 days without mana use per level, cumulative), dropping the character to a lower level and triggering withdrawal penalties. At Level 5 (Obsession), missing a single day of use instantly drops the character to Level 4, initiating severe withdrawal.
Active Effects: Each level applies ongoing penalties while the character remains at that level, reflecting the strain of dependency.
Withdrawal Effects: Penalties apply upon level drop (via decay or Level 5 miss), lasting longer than active benefits and representing the crash of mana’s absence.
Usage Benefits: Mana use provides immediate and short-term general bonuses (non-magical stats) during and after use (excluding withdrawal periods), creating a seductive high that tempts repeated engagement.
Recovery: Full recovery from withdrawal penalties requires consecutive days of non-use (scaling by level) or interventions (e.g., clan rituals, rare items), offering strategic paths to mitigate consequences.
Design Philosophy

The Mana Addiction System is built on a push-pull dynamic: mana’s benefits are fleeting and subtle, while its costs are enduring and brutal. This mirrors real-world addiction cycles—use feels rewarding in the moment, but absence or over-reliance exacts a heavier toll. Penalties focus on magical resource strain (regeneration, cost) and stat degradation (mental, physical), ensuring mana’s core utility suffers even as general stats gain temporary boosts. The system is universal for balance and clarity, applying consistent effects across all characters, though future iterations may explore class- or clan-specific modifiers. The narrative tone weaves divine mysticism with dark corruption, portraying mana as both god and chains.

Addiction Levels, Benefits, and Penalties

Below are the five levels of mana addiction, detailing active penalties (ongoing at each level), withdrawal penalties (upon level drop or during recovery), during-use benefits (immediate boosts on day of use), and after-use benefits (lingering effects post-use, non-withdrawal only). Durations and magnitudes scale with level, ensuring higher dependency carries greater risk and reward. All percentages are placeholders and subject to balance testing.

Level 1 - Reliance

Description: Early exposure to mana creates a subtle need; its absence is an inconvenience, not yet a torment.
Active Penalty: -10% Mana Regeneration Rate.
Narrative: “Your hands tremble faintly after casting; mana feels heavier.”
Withdrawal Penalty (Dropping to Level 0): -5% Mana Regeneration Rate for 5 days.
Narrative: “Mana’s absence leaves a dull ache, but it’s fading.”
Recovery: 5 consecutive days of no use, or minor intervention (e.g., herbal remedy).
During Use Benefit: +5% Focus/Willpower Stat.
Narrative: “Mana sharpens your mind; the world feels vivid for a fleeting moment.”
After Use Benefit (Non-Withdrawal): +3% Focus/Willpower Stat for 2 days post-use.
Narrative: “A faint echo of mana lingers; your thoughts are keener.”

Level 2 - Habituation

Description: Mana becomes a habit, a crutch for power; its pull strengthens, and withdrawal bites deeper.
Active Penalty: -15% Mana Regeneration Rate, +5% Mana Cost for Spells.
Narrative: “Mana courses through you, but it burns at the edges of your mind.”
Withdrawal Penalty (Dropping to Level 1 or 0): -10% Mana Regeneration Rate, +3% Mana Cost for Spells, both for 10 days.
Narrative: “Without mana, your focus frays; you crave its hum.”
Recovery: 10 consecutive days of no use, or moderate intervention (e.g., meditation ritual).
During Use Benefit: +7% Focus/Willpower Stat, +3% Physical Vitality/Endurance.
Narrative: “Mana surges through you, mind and body alight with fleeting strength.”
After Use Benefit (Non-Withdrawal): +4% Focus/Willpower Stat, +2% Physical Vitality/Endurance, both for 3 days post-use.
Narrative: “Mana’s warmth lingers; you feel a subtle edge.”

Level 3 - Dependency

Description: Mana is a necessity; mind and body bend under its weight, yet its power sustains you.
Active Penalty: -20% Mana Regeneration Rate, +10% Mana Cost for Spells, -5% Focus/Willpower Stat.
Narrative: “Mana is your tether; without it, thoughts scatter like ash.”
Withdrawal Penalty (Dropping to Level 2 or below): -15% Mana Regeneration Rate, +5% Mana Cost for Spells, -3% Focus/Willpower, all for 20 days.
Narrative: “Mana’s void gnaws at you; every thought begs for its return.”
Recovery: 20 consecutive days of no use, or significant intervention (e.g., clan cleansing rite).
During Use Benefit: +10% Focus/Willpower Stat, +5% Physical Vitality/Endurance, +3% Resistance to Mental Effects.
Narrative: “Mana is your shield; mind and body hum with defiant power.”
After Use Benefit (Non-Withdrawal): +6% Focus/Willpower Stat, +3% Physical Vitality/Endurance, +2% Resistance to Mental Effects, all for 4 days post-use.
Narrative: “Mana’s echo guards you; its strength fades slowly.”

Level 4 - Subjugation

Description: Mana chains you utterly; it fuels your existence, but at ruinous cost to body and soul.
Active Penalty: -30% Mana Regeneration Rate, +15% Mana Cost for Spells, -10% Focus/Willpower Stat, -5% Physical Vitality/Endurance.
Narrative: “Mana chains you; every breath aches for its power.”
Withdrawal Penalty (Dropping to Level 3 or below): -20% Mana Regeneration Rate, +10% Mana Cost for Spells, -5% Focus/Willpower, -3% Physical Vitality, all for 30 days.
Narrative: “Mana’s absence is torment; your body and mind rebel.”
Recovery: 30 consecutive days of no use, or major intervention (e.g., rare artifact).
During Use Benefit: +12% Focus/Willpower Stat, +7% Physical Vitality/Endurance, +5% Resistance to Mental Effects.
Narrative: “Mana enslaves, yet empowers; you are invincible in its grasp, if only for now.”
After Use Benefit (Non-Withdrawal): +8% Focus/Willpower Stat, +4% Physical Vitality/Endurance, +3% Resistance to Mental Effects, all for 5 days post-use.
Narrative: “Mana’s chains linger as strength; you dread its absence.”

Level 5 - Obsession

Description: Mana is your god; total surrender grants divine power, but a single day without it shatters you.
Active Penalty: -50% Mana Regeneration Rate, +25% Mana Cost for Spells, -15% Focus/Willpower Stat, -10% Physical Vitality/Endurance, 5% Chance of Spell Failure per Cast.
Narrative: “Mana is your god; you are nothing without it. It consumes all.”
Withdrawal Penalty (Dropping to Level 4 or below, triggered instantly by missing a day): -30% Mana Regeneration Rate, +15% Mana Cost for Spells, -10% Focus/Willpower, -5% Physical Vitality, 3% Chance of Spell Failure per Cast, all for 50 days; additional “Shattered Will” debuff (cannot use high-tier spells) for first 10 days of withdrawal.
Narrative: “A day without mana shatters you; you are a husk, clawing for its return.”
Recovery: 50 consecutive days of no use, or extraordinary intervention (e.g., divine ritual).
During Use Benefit: +15% Focus/Willpower Stat, +10% Physical Vitality/Endurance, +7% Resistance to Mental Effects, +3% Critical Chance.
Narrative: “Mana is your divinity; in its embrace, you transcend mortal limits.”
After Use Benefit (Non-Withdrawal): +10% Focus/Willpower Stat, +6% Physical Vitality/Endurance, +4% Resistance to Mental Effects, +2% Critical Chance, all for 6 days post-use.
Narrative: “Mana’s godlike touch lingers; you are more than human, for now.”

Balance Considerations

Push-Pull Dynamic: Benefits are minor and short-lived (2-6 days for after-use effects) compared to penalties (5-50 days for withdrawal, ongoing active penalties). Even at peak obsession, mana use barely sustains baseline stats (net 0% Focus/Vitality during use at Level 5), while non-use or withdrawal results in catastrophic loss.
Magical Strain: Penalties primarily target mana resources (regeneration, cost, spell failure), ensuring magical utility suffers regardless of general stat boosts (Focus, Vitality, etc.), preserving the system’s punishing core.
Addiction Cycle: Temporary highs during and after use create temptation, overcompensating active penalties briefly (e.g., net +5% Focus during use at Level 3 despite -5% active penalty), but withdrawal drops stats far below baseline for extended periods, mirroring the crash of dependency.
Future Testing: Magnitudes (e.g., -50% regen, +15% Focus) and durations (e.g., 50-day withdrawal) are placeholders pending gameplay simulation to ensure balance. Focus will be on ensuring penalties outweigh benefits long-term without alienating players.

Narrative and UI Integration (TBD)

Narrative Feedback: Each level and effect includes flavor text to immerse players in mana’s dual nature—divine power and corrupting chains. Future development will expand on in-game dialogue or journal entries reflecting addiction state (e.g., NPC concern at higher levels).
Visual Cues: Potential UI elements include aura effects during mana highs (e.g., glowing veins on character model), degrading to ashen or trembling visuals in withdrawal. HUD indicators may track addiction level and days until decay/withdrawal.
Audio Design: Soundscapes could shift with addiction—harmonic hums during mana use, dissonant echoes in withdrawal—to reinforce the psychological toll.
Future Iterations

Progression Triggers: Define exact usage thresholds for level advancement (e.g., X mana uses per week, Y consecutive days) and decay timers (e.g., cumulative 10 days no-use per level).
Recovery Options: Expand on intervention mechanics (e.g., clan rituals, artifacts) with costs and risks to balance accessibility.
Variation: Explore optional class- or clan-based modifiers for penalties/benefits (e.g., mages lose more spell power, warriors gain more Vitality) while maintaining a universal baseline for clarity.
Simulation: Conduct 30-day in-game cycle tests to evaluate high-low dynamics, adjusting magnitudes or durations for optimal risk-reward tension.
Design Intent

The Mana Addiction System is a ritual that teaches—a beautiful, brutal mechanic where every choice stings with consequence. It architects a world where power is never free, and transcendence comes with torment. Mana is a god to worship and a chain to bear; players must navigate its allure with strategy, lest they fall to obsession and shatter under its weight. This system sings like code, inevitable and dangerous, ensuring no victory lacks a scar
---

## 8. Incarnation & Progression

### Incarnation & Reincarnation System

- **Player Incarnates**: Control specific NPC entity through full lifespan
- **Full Lifespan**: Manage needs, skills, relationships, addiction, magic from birth to death
- **Death & Reincarnation**: Soul released, options for reincarnation presented
- **Skill Legacy**: Persistent record of mastered skills carries forward
- **Messiah Incarnation**: Special life with enhanced control over character creation
- **Ascension**: Maxing all skills in single life triggers path to demigodhood

### Skill Legacy & Learning System

#### Variables

- \( L \) = max skill level reached in a life (0 to 100)
- \( M \) = number of times the skill has been maxed out (reached 100)
- \( S \) = skill legacy score for that skill (accumulated across lives)
- \( k \) = learning speed scaling constant (tunable, e.g., 0.01)
- \( \alpha \) = weight for partial mastery (e.g., 1.0)
- \( \beta \) = weight for full mastery bonus (e.g., 5.0)

#### Skill Legacy Score Update on Life End

When a life ends, update the skill legacy score \( S \) for each skill as:

\[
S_{\text{new}} = S_{\text{old}} + \alpha \times \left(\frac{L}{100}\right) + \beta \times M
\]

*Example:*
If a skill reached level 75 and was maxed 2 times before, then:

\[
S_{\text{new}} = S_{\text{old}} + 1.0 \times 0.75 + 5.0 \times 2 = S_{\text{old}} + 0.75 + 10 = S_{\text{old}} + 10.75
\]

#### Learning Speed Modifier on New Life

The player's XP gain rate for a skill is modified by:

\[
\text{XP Gain Modifier} = 1 + k \times S
\]

Where \(k\) controls how much legacy affects learning speed. For example, if \(k=0.01\) and \(S=50\), XP gain is increased by 50%.

#### Starting Skill Level Bonus

Players start with a base skill level bonus proportional to legacy:

\[
\text{Starting Skill Level} = \min\left( \left\lfloor \frac{S}{10} \right\rfloor, 50 \right)
\]

This caps the starting skill level bonus at 50 to keep progression meaningful.

#### Data Structures

```python
# Skill legacy data per skill
class SkillLegacy:
    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.legacy_score = 0.0  # Accumulated legacy points
        self.maxed_count = 0     # Number of times skill reached 100

# Player reincarnation data
class ReincarnationData:
    def __init__(self):
        self.skill_legacies = {}  # Dict[str, SkillLegacy]
        self.lives_lived = 0
        self.has_ascended_to_demigod = False
```

- Store `ReincarnationData` persistently across lives
- Update `skill_legacies` at life end
- Use `skill_legacies` to calculate XP modifiers and starting skill levels on new incarnations

### Worship & Divine Influence System

- **Unlock Condition**: Achieved after Ascension
- **Player Becomes**: Demigod observing from higher perspective
- **Worship Mechanic**: NPCs generate worship based on Ascended One's legacy
- **Divine Powers**: Spend Devotion Points for miracles, blessings, prophetic visions
- **Impact**: Influence clan fortunes, world events, future incarnations

---

## 9. Economy & Trade

### Currency System

- **Standard Coinage**: Gold, silver, copper for general trade
- **Barter Economy**: Items substitute for currency in coin-scarce regions
- **Specialized Tokens**: Faction-specific scrips and guild notes
- **Dynamic Pricing**: Supply, demand, scarcity, and faction control affect prices

### Trade Mechanics

- **NPC Traders**: Personal inventories, preferences, haggling skills
- **Regional Markets**: Specialized goods based on local resources
- **Trade Routes**: Physical transport of goods across regions
- **Market Disruption**: Bandits, war, weather, or player intervention

---

## 10. Crafting & Items

### Resource Categories

#### Environment

- Air, Water, Grass, Dirt, Mud, Sand, Snow, Lava

#### Valuables

- Currency (Copper Ore + Iron Ore)
- Gem (Gemstone + Flint)
- Crystal (Glass + Essence)

#### Botanical Resources

- Tree, Flower, Bush, Sap, Vine, Fruit, Seed, Stick, Herb, Moss, Mushroom

#### Geological Resources

- Rock, Stone, Clay, Coal, Salt, Ash, Ice

### Comprehensive Crafting System

#### Crafting Categories

**Tools:**

- Required Skill: Crafting, Level 1
- Workstation: Workbench
- Base Crafting Time: 30.0 minutes
- XP Gain: 10.0
- Durability Factor: 1.0
- Quality Variance: 0.15
- Material Efficiency: 0.9

**Weapons:**

- Required Skill: Weaponsmithing, Level 5
- Workstation: Forge
- Base Crafting Time: 90.0 minutes
- XP Gain: 25.0
- Durability Factor: 1.2
- Quality Variance: 0.2
- Material Efficiency: 0.8
- Damage Modifier: 1.0

**Armor:**

- Required Skill: Armorsmithing, Level 5
- Workstation: Tailoring Bench
- Base Crafting Time: 75.0 minutes
- XP Gain: 20.0
- Durability Factor: 1.3
- Quality Variance: 0.18
- Material Efficiency: 0.85
- Protection Modifier: 1.0

**Structures:**

- Required Skill: Carpentry, Level 3
- Workstation: Carpentry Bench
- Base Crafting Time: 120.0 minutes
- XP Gain: 30.0
- Durability Factor: 1.1
- Quality Variance: 0.1
- Material Efficiency: 0.95
- Stability Factor: 1.0
- Weather Resistance: 0.8
- Build Time Multiplier: 1.5

**Consumables:**

- Required Skill: Cooking, Level 1
- Workstation: Cooking Pot
- Base Crafting Time: 20.0 minutes
- XP Gain: 15.0
- Quality Variance: 0.12
- Material Efficiency: 1.1
- Batch Size: 4
- Spoilage Rate: 0.05
- Effect Potency: 1.0

**Materials:**

- Required Skill: Crafting, Level 1
- Workstation: Workbench
- Base Crafting Time: 15.0 minutes
- XP Gain: 8.0
- Quality Variance: 0.1
- Material Efficiency: 1.0
- Batch Size: 1
- Refinement Quality: 1.0

**Jewelry:**

- Required Skill: Jewelry, Level 10
- Workstation: Jewelers Bench
- Base Crafting Time: 60.0 minutes
- XP Gain: 35.0
- Quality Variance: 0.25
- Material Efficiency: 0.7
- Beauty Factor: 1.5
- Enchantment Slots: 2
- Value Multiplier: 2.5

**Magic Items:**

- Required Skill: Enchanting, Level 15
- Workstation: Enchanting Table
- Base Crafting Time: 180.0 minutes
- XP Gain: 50.0
- Quality Variance: 0.3
- Material Efficiency: 0.6
- Magic Potency: 1.0
- Enchantment Slots: 3
- Soul Gem Requirement: 1
- Mana Cost Multiplier: 1.2

#### Crafting Stations

**Workbench:**

- Crafting Speed: 1.0
- Quality Bonus: 0.0
- Material Efficiency: 1.0
- Durability: 100.0
- Durability Loss Per Use: 0.1
- Repair Cost Multiplier: 1.0
- Unlocks Categories: Tools, Materials
- Required Tools: Hammer, Saw
- Tool Durability Loss: 0.05
- Upgrade Slots: 2
- Base Energy Cost: 5.0
- Unlock Level: 1
- Build Cost: Wood 20, Nails 10, Metal Ingot 2
- Interaction Radius: 2.0

**Forge:**

- Crafting Speed: 0.8
- Quality Bonus: 0.1
- Material Efficiency: 0.9
- Durability: 150.0
- Durability Loss Per Use: 0.2
- Repair Cost Multiplier: 1.2
- Unlocks Categories: Weapons, Armor
- Required Tools: Tongs, Hammer, Anvil
- Tool Durability Loss: 0.1
- Fuel Consumption Rate: 1.5
- Heat Retention: 0.8
- Upgrade Slots: 3
- Base Energy Cost: 10.0
- Unlock Level: 5
- Build Cost: Stone 30, Metal Ingot 15, Clay 20, Wood 10
- Interaction Radius: 2.5

**Tailoring Bench:**

- Crafting Speed: 1.2
- Quality Bonus: 0.15
- Material Efficiency: 1.1
- Durability: 90.0
- Durability Loss Per Use: 0.08
- Repair Cost Multiplier: 0.9
- Unlocks Categories: Armor
- Required Tools: Scissors, Needle
- Tool Durability Loss: 0.03
- Stitching Quality: 1.2
- Upgrade Slots: 2
- Base Energy Cost: 4.0
- Unlock Level: 3
- Build Cost: Wood 15, Cloth 5, Nails 5, Thread 10
- Interaction Radius: 1.8

**Cooking Pot:**

- Crafting Speed: 1.5
- Quality Bonus: 0.2
- Material Efficiency: 1.2
- Durability: 80.0
- Durability Loss Per Use: 0.05
- Repair Cost Multiplier: 0.8
- Unlocks Categories: Consumables
- Required Tools: Ladle, Knife
- Tool Durability Loss: 0.02
- Fuel Consumption Rate: 0.8
- Heat Retention: 0.7
- Upgrade Slots: 1
- Base Energy Cost: 3.0
- Unlock Level: 2
- Build Cost: Metal Ingot 5, Wood 5, Clay 3
- Interaction Radius: 1.5

**Alchemy Lab:**

- Crafting Speed: 0.7
- Unlocks Categories: Consumables
- Required Tools: Mortar and Pestle, Flask
- Mana Requirement: 10
- Upgrade Slots: 2

#### Quality Levels

**Crude:**

- Multiplier: 0.5
- Durability Modifier: 0.5
- Effectiveness Modifier: 0.7
- Chance: 0.2

**Standard:**

- Multiplier: 1.0
- Durability Modifier: 1.0
- Effectiveness Modifier: 1.0
- Chance: 0.6

**Fine:**

- Multiplier: 1.3
- Durability Modifier: 1.2
- Effectiveness Modifier: 1.1
- Chance: 0.15
- Required Skill Bonus: 1

**Masterwork:**

- Multiplier: 2.0
- Durability Modifier: 1.5
- Effectiveness Modifier: 1.3
- Chance: 0.05
- Required Skill Bonus: 2
- Special Effects: true

**Legendary:**

- Multiplier: 3.0
- Durability Modifier: 2.0
- Effectiveness Modifier: 1.5
- Chance: 0.001
- Required Skill Bonus: 5
- Special Effects: true
- Unique Effects: true

---

## 11. Development Framework

### Project Structure

```
project/
├── src/                  # Source code
│   ├── core/             # ECS framework (Cortex)
│   ├── components/       # Game components
│   ├── systems/          # Game systems
│   └── utils/            # Utilities and constants
├── data/                 # Game data manifests
│   ├── biology/          # DNA manifests
│   ├── biomes/           # Biome definitions
│   ├── entities/         # Entity manifests
│   ├── resources/        # Materials, metals, stones
│   └── world/            # Weather and world configs
├── docs/                 # Documentation
├── tests/                # Test suite
└── notes/                # Development notes
```

### Development Phases

1. **Pre-production**: Design and prototyping
2. **Vertical slice**: Core gameplay implementation
3. **Alpha**: Feature complete implementation
4. **Beta**: Content complete, polish and balance
5. **Release**: Launch and post-launch support

### Python Packages

Core packages include: numpy, scipy, pygame-ce, pymunk, simpy, noise, esper, pydantic, rich, pytest, and many others for scientific computing, AI, graphics, and development tools.

### Performance Optimization

- **Tick-based simulation** with priority scheduling
- **Lazy loading** for regions outside player awareness
- **Parallel processing** for AI, physics, and rendering
- **Incremental autosave** without interrupting gameplay flow

### Game Constants and Configuration

#### Core Constants

- **NEEDS**: ['Hunger', 'Thirst', 'Energy', 'Social', 'Health', 'Hygiene', 'Bladder', 'Stress', 'Morale', 'Motivation', 'Focus', 'Enjoyment', 'Mana']
- **AGES**: ['Infant', 'Toddler', 'Child', 'Teen', 'Young Adult', 'Adult', 'Elder']
- **TRAIT_GROUPS**: ['Temperament', 'Socialization', 'Emotional', 'Cognition', 'Interaction', 'Identity', 'Ambition', 'Morals', 'Legacy']
- **TRAIT_POLARITY**: ['Positive', 'Neutral', 'Negative']
- **BODY_TYPES**: ['Ecomorph', 'Mesomorph', 'Endomorph']
- **BODY_SHAPES**: ['Pear', 'Inverted Triangle', 'Apple', 'Rectangle', 'Hourglass']

#### Physical Characteristics

- **EYE_SHAPES**: ['Almond', 'Round', 'Monolid', 'Downturned', 'Upturned']
- **EYE_SPACING**: ['Close', 'Wide', 'Normal']
- **EYE_DEPTH**: ['Deep', 'Protruding', 'Normal']
- **HEAD_SHAPES**: ['Oval', 'Round', 'Square', 'Oblong', 'Heart', 'Triangle', 'Diamond', 'Base-Down Diamond', 'Pentagon']

#### World Parameters

- **BIOMES**: ['Forest', 'Grassland', 'Desert', 'Wetland', 'Highland', 'Coastal', 'Rockland']
- **TERRAIN_TYPES**: ['soil', 'water', 'grass', 'stone', 'sand']
- **ALTITUDE**: ['low', 'sea level', 'high']
- **TEMPS**: ['hot', 'mild', 'cold', 'frozen']
- **HUMIDITY**: ['wet', 'average', 'dry']

#### Item Properties

- **RARITY**: ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
- **DURABILITY**: ['shoddy', 'fragile', 'sturdy', 'hardened', 'reinforced', 'indestructible']
- **CONDITION**: ['ruined', 'damaged', 'functional', 'maintained', 'excellent', 'mint']
- **QUALITY**: ['crude', 'ordinary', 'refined', 'skilled', 'exceptional', 'masterpiece']
- **VALUE**: ['junk', 'cheap', 'standard', 'priceless', 'relic', 'legendary']
- **WEIGHT**: ['featherlight', 'light', 'medium', 'heavy', 'cumbersome', 'massive']

#### Technical Constants

- **TILE_SIZE**: 32 pixels
- **WORLD_WIDTH**: 40 tiles
- **WORLD_HEIGHT**: 30 tiles
- **SCREEN_WIDTH**: 1280 pixels (40 × 32)
- **SCREEN_HEIGHT**: 960 pixels (30 × 32)
- **FPS**: 60 frames per second
- **VISIBLE_RADIUS**: Maximum of world dimensions

---

## 6. Magic System

### 6.1 Core Magic Mechanics

#### Magic Attributes

- **Conviction**: Determines the power of magical spells
- **Finesse**: Determines the precision and control of magical spells
- **Willpower**: Determines the ability to maintain concentration and focus

#### Mana System

- **Mana Pool**: (Conviction + Finesse) × 10
- **Mana Regeneration**: Base rate of 1 MP per minute, modified by Willpower and environmental factors
- **Magical Aptitude**: Determines maximum potential in different schools of magic
- **Spell Slots**: Limited by character level and magical training

#### Spell Components

- **Verbal**: Incantations and words of power
- **Somatic**: Hand gestures and body movements
- **Material**: Physical components consumed or focused through
- **Focus**: Magical items that channel or enhance spells

### 6.2 Schools of Magic

Spells are woven from the union of elemental force and the guiding hand of arcane or divine magic. Each incantation is shaped by two parts: the element forms the foundation, while the theme dictates the purpose. The element defines how the spell manifests in the world, while the theme, in turn, gives the spell its nature—whether destruction, healing, illusion, summoning, binding, or countless other intents. When these two threads entwine, they create unique and powerful sorceries. The same theme may take on entirely different forms depending on the element. In this way, spellcraft becomes a lattice of infinite combinations, each one a new expression of will made manifest.

#### Elemental Magic

- **Fire**: governs flame, heat, and light. Its nature is passion, destruction, and unrelenting hunger. Fire manifests in blazing attacks, burning wards, and radiant bursts of illumination.
- **Water**: embodies healing, change, and the flow of life. It bends to transformation, soothing wounds, reshaping form, and carrying both purity and corruption in its currents.
- **Earth**: is strength, stability, and endurance. It shields, fortifies, and shapes the terrain itself, giving rise to walls of stone, armored flesh, and the weight of mountains.
- **Air**: is movement, perception, and freedom. It commands the winds, alters the senses, and weaves currents that carry speed, flight, or storms.
- **Spirit**: binds essence, will, and memory. It is the tether between life and death, a power of communion, binding, and unraveling the unseen threads of the soul.

#### Arcane Magic

- **Abjuration**: defends, wards, and banishes. It is the art of repelling harm, sealing rifts, and shielding the fragile from chaos.
- **Conjuration**: summons and calls forth. It opens doors to distant realms, draws creatures into the caster’s service, and brings forth objects from nothing.
- **Divination**: reveals hidden truths. It pierces veils, uncovers secrets, and shows glimpses of what has been, what is, and what may yet come.
- **Enchantment**: bends the will. It charms, beguiles, and enthralls, shaping thoughts and emotions like clay in the hands of the cunning.
- **Evocation**: unleashes raw force. It channels elemental energy in violent bursts—fireballs, lightning strikes, shattering thunder, and rays of searing power.
- **Illusion**: deceives the senses. It creates false visions, illusions, and mirages, bending reality to the caster’s will.
- **Necromancy**: manipulates life and death. It commands the fallen, siphons vitality, and binds spirits, delving into the forbidden essence of mortality.
- **Transmutation**: alters form and nature. It reshapes matter, transforms creatures, and bends reality into new and wondrous shapes.

#### Divine Magic

- **Healing**: restores body and spirit. It mends wounds, cures afflictions, and rekindles life’s flame where it wanes.
- **Warding**: shields against corruption. It sanctifies places, bars evil, and weaves protective blessings over the faithful.
- **Judgment**: strikes with divine authority. It punishes the wicked, smites foes, and channels the wrath of higher powers through mortal hands.
- **Communion**: bridges mortal and divine. It calls upon gods, saints, and spirits, seeking guidance, miracles, or the power of sacred bonds.

---

### 6.3 Spellcasting Systems

Magic is not only divided by schools of thought, but also by the manner in which a caster draws upon it. Three systems govern the use of spells, each with its own strengths and costs.

#### Prepared Spells

These feel scholarly and priestly, demanding forethought and ritual sacrifice. They must be inscribed into memory after rest, with costly components and a ritual focus. The caster may only hold a limited number of these spells each day, yet their effects are stronger and broader in scope. Where spontaneous casting is swift, prepared casting is deliberate—and for this reason, wizards and clerics favor it, wielding magic that feels sacred, intentional, and heavy with consequence.

#### Spontaneous Spells

These are raw instinct, like lightning striking where it pleases. The caster does not bind the spell in advance but shapes the lattice of element and theme in the moment. Only a few such combinations can be held in the mind, but they can be cast freely so long as mana remains to fuel them. Components are minimal, casting is immediate, and the caster may improvise within their chosen themes. Sorcerers and bards thrive in this style, versatile in the moment but less encyclopedic in scope.

#### Hybrid Spells

Here lies the most intriguing path, a marriage of foresight and passion. Hybrid casters prepare some spells in advance while shaping others on instinct. Their component demands fall between the extremes, yet their true strength is adaptability. In dire moments, a hybrid may unbind a prepared spell and hurl it forth spontaneously, paying both components and mana at once to achieve devastating power. This duality makes hybrids the most strategic of casters, walking the knife-edge between order and chaos.

### 6.4 Magical Progression

#### Learning Magic

- **Training**: Study under mentors or at magical academies
- **Discovery**: Experimentation and research
- **Inheritance**: Magical bloodlines and legacies
- **Boon**: Divine or otherworldly gifts

#### Magical Specialization

- Focus on specific schools or types of magic
- Bonus spells and abilities in chosen field
- Potential penalties or restrictions in opposed schools
- Unlocks advanced spells and techniques

#### Magical Artifacts

- **Weapons**: Enhanced with magical properties
- **Armor**: Magical protection and enhancements
- **Jewelry**: Rings, amulets, and other wearables
- **Relics**: Powerful items with unique abilities
- **Grimoires**: Spellbooks containing lost or powerful magic

### 6.5 Magic in Combat

#### Spellcasting in Battle

- **Casting Time**: Varies by spell complexity
- **Concentration**: Maintaining spells over time
- **Counterspelling**: Disrupting enemy magic
- **Spell Resistance**: Natural or magical defenses

#### Magical Combat Styles

- **Battlemage**: Mixing magic with martial prowess
- **Arcane Archer**: Enchanted ranged attacks
- **Spellblade**: Weapon-enhancing magic
- **Summoner**: Calling forth magical allies

### 6.6 Magic and the World

#### Magical Phenomena

- **Ley Lines**: Natural flows of magical energy
- **Dead Magic Zones**: Areas where magic doesn't function
- **Wild Magic**: Unpredictable magical effects
- **Mana Storms**: Violent outbursts of raw magic

#### Magical Creatures

- **Elementals**: Beings of pure elemental energy
- **Undead**: Animated by necromantic energies
- **Demons**: Malevolent entities
- **Angels**: Divine beings

#### Magical Professions

- **Alchemist**: Brewing potions and elixirs
- **Enchanter**: Creating magical items
- **Ritualist**: Performing complex magical ceremonies
- **Scholar**: Researching lost or forbidden magic

### 6.7 Advanced Magical Concepts

#### Spell Research

- Developing new spells
- Modifying existing spells
- Creating magical items
- Discovering ancient magical knowledge

#### Magical Ethics

- Responsible use of magic
- Magical laws and regulations
- Consequences of magical meddling
- Balance between magical and non-magical beings

### 6.8 Magic UI and Feedback

#### Spell Management

- **Spellbook Interface**: Organizing known spells
- **Quick Cast**: Favorite spells for quick access
- **Spell Combos**: Visualizing spell interactions

#### Casting Feedback

- **Visual Effects**: Distinct looks for different spells
- **Audio Cues**: Unique sounds for spellcasting
- **Haptic Feedback**: Controller vibrations for spell effects
- **Screen Effects**: Visual indicators of magical influence

---

## Conclusion

Duskbourne Divine represents a comprehensive vision for a deep, living simulation that combines survival mechanics, tactical combat, magic systems, addiction mechanics, social dynamics, and generational progression. The modular ECS architecture provides a solid foundation for complex systems while maintaining performance and extensibility.

The game's unique blend of procedural generation, AI-driven NPCs, persistent world changes, and the journey from mortal survival to divine influence creates emergent storytelling opportunities that ensure no two playthroughs are alike. The clan systems, reputation mechanics, and addiction dynamics provide meaningful choices with lasting consequences, while the crafting and economy systems offer deep strategic gameplay.

This documentation serves as the definitive reference for all aspects of the project, combining the technical depth of the ECS architecture with the rich world-building and systems design, providing a roadmap for development and a foundation for future expansion.

---

*This document combines information from division.md and first.md as of September 12, 2025.*
