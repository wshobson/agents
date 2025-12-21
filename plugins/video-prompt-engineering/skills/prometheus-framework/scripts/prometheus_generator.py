#!/usr/bin/env python3
"""
PROMETHEUS Video Prompt Generator

A sophisticated prompt generation system for AI video generators that implements
the PROMETHEUS framework for achieving Hollywood-quality output.
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class AspectRatio(Enum):
    CINEMATIC = "2.39:1 Cinemascope"
    WIDESCREEN = "16:9"
    VERTICAL = "9:16"
    SQUARE = "1:1"
    STANDARD = "4:3"
    IMAX = "1.43:1"


class ShotType(Enum):
    ELS = "Extreme Long Shot"
    LS = "Long Shot"
    MLS = "Medium Long Shot"
    MS = "Medium Shot"
    MCU = "Medium Close-Up"
    CU = "Close-Up"
    BCU = "Big Close-Up"
    ECU = "Extreme Close-Up"


class CameraMovement(Enum):
    STATIC = "Static"
    PUSH_IN = "Push-In"
    PULL_OUT = "Pull-Out"
    PAN = "Pan"
    TILT = "Tilt"
    DOLLY = "Dolly"
    TRACKING = "Tracking"
    CRANE = "Crane"
    STEADICAM = "Steadicam"
    HANDHELD = "Handheld"
    ORBITAL = "Orbital"


class LightingMood(Enum):
    INTIMATE = "intimate"
    DRAMATIC = "dramatic"
    NATURAL = "natural"
    NOSTALGIC = "nostalgic"
    MYSTERIOUS = "mysterious"
    TRANSCENDENT = "transcendent"
    CLINICAL = "clinical"
    LUXURIOUS = "luxurious"


@dataclass
class LightingSetup:
    key_temperature: int  # Kelvin
    key_source: str
    fill_ratio: str  # e.g., "1:4"
    rim_back: Optional[str] = None
    practicals: Optional[str] = None
    special_effects: Optional[str] = None
    mood: LightingMood = LightingMood.NATURAL

    def to_prose(self) -> str:
        """Convert lighting setup to prose description."""
        temp_descriptions = {
            1800: "firelight warmth, amber beyond amber",
            2400: "Edison-bulb nostalgia, golden memories",
            2700: "tungsten intimacy, the warmth of inhabited spaces",
            3200: "controlled warmth, precision without coldness",
            4000: "neutral transition, light between emotional states",
            5000: "documentary clarity, truth without interpretation",
            5600: "honest daylight, the sun's neutral revelation",
            6500: "overcast melancholy, cool contemplation",
        }

        closest_temp = min(temp_descriptions.keys(), key=lambda x: abs(x - self.key_temperature))
        temp_prose = temp_descriptions[closest_temp]

        return f"Light carries {temp_prose}, shadows finding their ratio in gentle negotiation with illumination"


@dataclass
class AtmosphericConditions:
    visibility: str
    particles: Optional[str] = None
    particle_density: Optional[int] = None  # per cubic meter
    air_quality: Optional[str] = None
    time_context: Optional[str] = None

    def to_prose(self) -> str:
        """Convert atmospheric conditions to prose."""
        particle_prose = ""
        if self.particles:
            density_map = {
                (0, 25): "sparse, each visible mote a rarity",
                (25, 75): "moderate, visible in light beams",
                (75, 150): "dense, atmosphere thickening with presence",
                (150, 300): "heavy, air itself becoming visible",
            }

            if self.particle_density:
                for (low, high), desc in density_map.items():
                    if low <= self.particle_density < high:
                        particle_prose = f"{self.particles} drift through the frame, {desc}"
                        break

        return f"{self.visibility}. {particle_prose}"


@dataclass
class CameraConsciousness:
    entry_description: str
    journey_description: str
    arrival_description: str
    entry_time: float = 0.0
    journey_time: float = 0.5
    arrival_time: float = 1.0

    def to_prose(self) -> str:
        return f"""CAMERA CONSCIOUSNESS:
├── ENTRY ({self.entry_time:.2f}s): {self.entry_description}
├── JOURNEY ({self.journey_time:.2f}s): {self.journey_description}
└── ARRIVAL ({self.arrival_time:.2f}s): {self.arrival_description}"""


@dataclass
class Shot:
    number: int
    title: str
    duration: float
    start_time: float
    shot_type: ShotType
    angle: str
    movement: CameraMovement
    description: str
    camera: CameraConsciousness
    lighting: LightingSetup
    atmosphere: AtmosphericConditions

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration

    def to_prompt(self) -> str:
        separator = "─" * 79
        header = "═" * 79

        return f"""{separator}
SHOT {self.number}: {self.title.upper()}
Duration: {self.duration:.2f}s ({self.start_time:.2f}s - {self.end_time:.2f}s)
Shot Type: {self.shot_type.value}, {self.angle}, {self.movement.value}
{separator}

{self.description}

{self.camera.to_prose()}

LIGHTING ARCHITECTURE:
├── Key: {self.lighting.key_source} | {self.lighting.key_temperature}K | {self.lighting.mood.value}
├── Fill: {self.lighting.fill_ratio} ratio
├── Rim/Back: {self.lighting.rim_back or 'N/A'}
├── Practicals: {self.lighting.practicals or 'None in frame'}
└── Special: {self.lighting.special_effects or 'None'}

ATMOSPHERIC CONDITIONS:
{self.atmosphere.to_prose()}
"""


@dataclass
class Act:
    number: int
    title: str
    start_time: float
    end_time: float
    emotional_destination: str
    visual_motif: str
    temporal_rhythm: str
    shots: List[Shot] = field(default_factory=list)
    transition_visual: Optional[str] = None
    transition_emotional: Optional[str] = None
    transition_technical: Optional[str] = None

    def to_prompt(self) -> str:
        header = "═" * 79
        shots_prompt = "\n".join(shot.to_prompt() for shot in self.shots)

        transition = ""
        if self.transition_visual:
            transition = f"""
TRANSITION TO NEXT ACT:
├── Visual Bridge: {self.transition_visual}
├── Emotional Shift: {self.transition_emotional}
└── Technical Link: {self.transition_technical}
"""

        return f"""
{header}
ACT {self.number}: {self.title.upper()} ({self.start_time:.2f}s - {self.end_time:.2f}s)
{header}

EMOTIONAL DESTINATION: {self.emotional_destination}
VISUAL MOTIF: {self.visual_motif}
TEMPORAL RHYTHM: {self.temporal_rhythm}

{shots_prompt}
{transition}"""


@dataclass
class AudioCue:
    timestamp: float
    sound: str
    position: str  # L/C/R/Stereo
    db_level: int
    character: str

    def to_prompt(self) -> str:
        return f"({self.timestamp:.2f}s) {self.sound} | {self.position} | {self.db_level}dB | {self.character}"


@dataclass
class MusicCue:
    act_number: int
    start_time: float
    end_time: float
    genre: str
    bpm: int
    key: str
    instruments: str
    dynamics_percent: int

    def to_prompt(self) -> str:
        return f"Act {self.act_number} ({self.start_time:.2f}s - {self.end_time:.2f}s): {self.genre} | {self.bpm} BPM | {self.key} | {self.instruments} | {self.dynamics_percent}% dynamics"


@dataclass
class Voiceover:
    start_time: float
    end_time: float
    line: str
    delivery_note: str

    def to_prompt(self) -> str:
        return f"({self.start_time:.2f}s - {self.end_time:.2f}s): \"{self.line}\" — {self.delivery_note}"


@dataclass
class AudioArchitecture:
    sonic_philosophy: str
    music_cues: List[MusicCue] = field(default_factory=list)
    sound_effects: List[AudioCue] = field(default_factory=list)
    voiceover_character: Optional[str] = None
    voiceover_delivery: Optional[str] = None
    voiceover_lines: List[Voiceover] = field(default_factory=list)

    def to_prompt(self) -> str:
        header = "═" * 79

        music = "\n".join(f"├── {cue.to_prompt()}" for cue in self.music_cues)
        sfx = "\n".join(f"├── {cue.to_prompt()}" for cue in self.sound_effects)

        vo_section = ""
        if self.voiceover_character:
            vo_lines = "\n".join(f"    ├── {vo.to_prompt()}" for vo in self.voiceover_lines)
            vo_section = f"""
VOICEOVER:
├── Voice: {self.voiceover_character}
├── Delivery: {self.voiceover_delivery}
└── Script:
{vo_lines}
"""

        return f"""
{header}
AUDIO ARCHITECTURE
{header}

SONIC PHILOSOPHY: {self.sonic_philosophy}

MUSIC CUES:
{music}

SOUND EFFECTS (Timestamped):
{sfx}
{vo_section}"""


@dataclass
class TechnicalSpecs:
    resolution: str = "4K UHD (3840×2160)"
    aspect_ratio: AspectRatio = AspectRatio.WIDESCREEN
    frame_rate: str = "24fps"
    color_space: str = "Rec. 709 with HDR-ready grading"
    camera_system: str = "ARRI Alexa Mini LF"
    primary_lens: str = "Zeiss Supreme Prime 50mm T1.5"
    color_profile: str = "ARRILogC4"
    total_duration: float = 15.0

    def to_prompt(self) -> str:
        return f"""TECHNICAL MASTER SPECIFICATIONS:
├── Resolution: {self.resolution}
├── Aspect Ratio: {self.aspect_ratio.value}
├── Frame Rate: {self.frame_rate}
├── Color Space: {self.color_space}
├── Camera System: {self.camera_system}
├── Primary Lens: {self.primary_lens}
├── Color Profile: {self.color_profile}
└── Total Duration: {self.total_duration:.2f} seconds"""


@dataclass
class PrometheusPrompt:
    """Complete PROMETHEUS video prompt structure."""

    # Genesis Block
    project_title: str
    project_subtitle: str
    core_visual_concept: str
    thematic_dna: List[str]
    emotional_architecture: List[str]  # [State1, State2, State3, Resolution]

    # Visual Signature
    director_reference: str
    director_element: str
    color_philosophy: str
    light_character: str
    movement_language: str

    # Technical
    specs: TechnicalSpecs

    # Content
    acts: List[Act] = field(default_factory=list)
    audio: Optional[AudioArchitecture] = None
    photorealistic_directives: Optional[str] = None

    def generate(self) -> str:
        """Generate the complete PROMETHEUS prompt."""
        header = "═" * 79

        # Thematic DNA as comma-separated
        themes = ", ".join(self.thematic_dna)

        # Emotional arc with arrows
        emotional_arc = " → ".join(self.emotional_architecture)

        # Acts
        acts_prompt = "\n".join(act.to_prompt() for act in self.acts)

        # Audio section
        audio_prompt = self.audio.to_prompt() if self.audio else ""

        # Photorealistic directives
        photo_section = ""
        if self.photorealistic_directives:
            photo_section = f"""
{header}
PHOTOREALISTIC GENERATION DIRECTIVES
{header}

{self.photorealistic_directives}
"""

        return f"""{header}
{self.project_title.upper()} — {self.project_subtitle}
{header}

CORE VISUAL CONCEPT:
{self.core_visual_concept}

THEMATIC DNA: {themes}

EMOTIONAL ARCHITECTURE: {emotional_arc}

VISUAL SIGNATURE:
├── Director Reference: {self.director_reference} — {self.director_element}
├── Color Philosophy: {self.color_philosophy}
├── Light Character: {self.light_character}
└── Movement Language: {self.movement_language}

{self.specs.to_prompt()}
{acts_prompt}
{audio_prompt}
{photo_section}
{header}
"""

    def export_json(self, filepath: str):
        """Export prompt structure to JSON for later modification."""
        import json
        # Note: Would need custom encoder for Enums
        # Simplified implementation
        with open(filepath, 'w') as f:
            json.dump({"title": self.project_title, "duration": self.specs.total_duration}, f)

    def validate(self) -> List[str]:
        """Validate prompt against PROMETHEUS requirements."""
        issues = []

        # Check shot description lengths
        for act in self.acts:
            for shot in act.shots:
                word_count = len(shot.description.split())
                if word_count < 150:
                    issues.append(f"Shot {shot.number} description too short: {word_count} words (minimum 150)")
                if word_count > 350:
                    issues.append(f"Shot {shot.number} description too long: {word_count} words (maximum 350)")

        # Check thematic DNA count
        if len(self.thematic_dna) < 5:
            issues.append(f"Thematic DNA too sparse: {len(self.thematic_dna)} themes (minimum 5)")

        # Check emotional architecture
        if len(self.emotional_architecture) < 3:
            issues.append(f"Emotional architecture too simple: {len(self.emotional_architecture)} states (minimum 3)")

        # Check core visual concept length
        if len(self.core_visual_concept.split()) < 40:
            issues.append("Core visual concept too brief (minimum 40 words)")

        return issues


# Prose generation helpers

class MaterialProse:
    """Generate prose descriptions for materials."""

    LIQUID_POETRY = {
        "water": "exploding into crystalline shards upon contact, each droplet a captured universe of refracted light",
        "coffee": "dark as secrets kept, opaque as midnight, steam rising in confessional wisps",
        "whisky": "amber alchemy descending with aristocratic patience, legs forming on glass like slow tears",
        "honey": "golden ropes stretching toward earth, resisting gravity with stubborn sweetness",
        "cream": "white ribbons descending with dairy weight, each fold holding shape through protein memory",
        "oil": "golden viscosity sliding with deliberate patience, coating surfaces with captured sunshine",
        "wine": "ruby cascades leaving violet traces like memory on glass",
        "milk": "calcium clouds with inner luminescence, light scattering back through dermal glow",
    }

    SOLID_POETRY = {
        "glass": "light passes through like time through memory, fragmenting into rainbow archaeology",
        "crystal": "prismatic refraction transforming light into scattered jewels, each facet a lens of possibility",
        "steel": "surfaces catch light and refuse to release it without first perfecting its reflection",
        "brass": "golden warmth softened by time's patient oxidation, patina earned through use",
        "leather": "biography written in creases, each fold a chapter of use, texture of lived experience",
        "wood": "grain patterns holding centuries of growth, light traveling along annual rings",
        "ceramic": "smooth surfaces hold light in gentle curves, neither absorbing nor reflecting with aggression",
        "skin": "translucent warmth beneath the surface, blood painting rose undertones from within",
    }

    @classmethod
    def get_liquid_prose(cls, material: str) -> str:
        return cls.LIQUID_POETRY.get(material.lower(), f"{material} moves with its characteristic deliberation")

    @classmethod
    def get_solid_prose(cls, material: str) -> str:
        return cls.SOLID_POETRY.get(material.lower(), f"{material} surfaces interact with light in their particular way")


class LightingProse:
    """Generate prose descriptions for lighting setups."""

    EMOTIONAL_TEMPLATES = {
        LightingMood.INTIMATE: "warmth spills across features with the gentleness of whispered secrets",
        LightingMood.DRAMATIC: "light cuts across surfaces like a blade, shadows sharp enough to wound",
        LightingMood.NATURAL: "illumination arrives with the honesty of unfiltered truth",
        LightingMood.NOSTALGIC: "golden warmth like afternoons remembered, soft edges suggesting memory's imprecision",
        LightingMood.MYSTERIOUS: "shadows dominate, light merely visiting the spaces between darkness",
        LightingMood.TRANSCENDENT: "light becomes substance, visible rays descending like divine intention",
        LightingMood.CLINICAL: "light reveals without mercy, every surface surrendering to brutal honesty",
        LightingMood.LUXURIOUS: "warmth caresses surfaces with the precision of professional attention",
    }

    @classmethod
    def get_mood_prose(cls, mood: LightingMood) -> str:
        return cls.EMOTIONAL_TEMPLATES.get(mood, "light illuminates with its particular quality")


def create_example_prompt() -> PrometheusPrompt:
    """Create an example PROMETHEUS prompt structure."""

    # Define technical specs
    specs = TechnicalSpecs(
        resolution="4K UHD (3840×2160)",
        aspect_ratio=AspectRatio.WIDESCREEN,
        frame_rate="24fps (with 60fps slow-motion inserts)",
        camera_system="ARRI Alexa 65",
        primary_lens="Zeiss Supreme Prime 50mm T1.5",
        total_duration=15.0
    )

    # Create lighting setup for first shot
    lighting1 = LightingSetup(
        key_temperature=2700,
        key_source="Tungsten fresnel through silk diffusion",
        fill_ratio="1:4",
        rim_back="LED panel creating edge separation",
        special_effects="Caustic patterns from liquid surfaces",
        mood=LightingMood.INTIMATE
    )

    # Create atmospheric conditions
    atmos1 = AtmosphericConditions(
        visibility="Crystal clear interior with volumetric steam elements",
        particles="Coffee aromatics and microscopic steam condensation",
        particle_density=75,
        air_quality="Warm humidity from espresso machines, cedar undertones",
        time_context="Late afternoon, golden hour approaching"
    )

    # Create camera consciousness
    camera1 = CameraConsciousness(
        entry_description="Frame establishes on ceramic rim, anticipating sacred ritual",
        journey_description="Lens breathes closer with magnetic inevitability",
        arrival_description="Final composition captures moment of liquid contact",
        entry_time=0.0,
        journey_time=0.75,
        arrival_time=1.5
    )

    # Create first shot
    shot1 = Shot(
        number=1,
        title="THE SACRED POUR",
        duration=2.5,
        start_time=0.0,
        shot_type=ShotType.ECU,
        angle="High Angle (30°)",
        movement=CameraMovement.PUSH_IN,
        description="""Steam rises like incense from the ceramic altar as oat milk cascades from pitcher spout with the deliberate precision of ritual sacrament. Each droplet catches afternoon light filtering through industrial skylights, creating prismatic micro-rainbows that dance across coffee's dark mirror surface like scattered jewels from heaven's treasury. The liquid exhibits oat milk's characteristic ivory opacity, its plant-based proteins creating surface tensions fundamentally different from dairy—slightly thicker, more viscous, with a pearl-like luminescence that suggests something both familiar and quietly revolutionary. The barista's hand moves with practiced grace born of ten thousand repetitions, aluminum pitcher's mirror surface reflecting fragments of exposed brick and warm wood grain in abstract impressionist fragments. Temperature differentials create visible convection currents as hot espresso meets cooler oat milk, thermal dynamics painting ephemeral abstract patterns that last mere heartbeats before dissolving into caffeinated homogeneity.""",
        camera=camera1,
        lighting=lighting1,
        atmosphere=atmos1
    )

    # Create first act
    act1 = Act(
        number=1,
        title="THE AWAKENING",
        start_time=0.0,
        end_time=5.0,
        emotional_destination="Anticipation building to reverent connection",
        visual_motif="Steam and liquid as spiritual metaphor",
        temporal_rhythm="Measured and deliberate, breath-like pacing",
        shots=[shot1],
        transition_visual="Steam rising connects to next act's aerial perspective",
        transition_emotional="From intimate ritual to cosmic understanding",
        transition_technical="Focus rack through steam to wider frame"
    )

    # Create audio architecture
    audio = AudioArchitecture(
        sonic_philosophy="Intimate ASMR landscape balancing minimal piano with rich environmental foley",
        music_cues=[
            MusicCue(1, 0.0, 5.0, "Solo piano, contemplative", 68, "E Minor", "Steinway grand", 40),
            MusicCue(2, 5.0, 10.0, "String quartet emerging", 68, "E Minor", "Strings + piano", 60),
            MusicCue(3, 10.0, 15.0, "Full ensemble resolution", 68, "E Major", "Full orchestra", 80),
        ],
        sound_effects=[
            AudioCue(0.00, "Ambient room tone establishment", "Stereo", -45, "Foundation"),
            AudioCue(0.50, "Milk pour initiation", "Center", -22, "Laminar smoothness"),
            AudioCue(1.20, "Liquid contact with espresso", "Center", -18, "Crystalline impact"),
            AudioCue(2.00, "Steam hiss subtle", "Center", -30, "Thermal whisper"),
        ],
        voiceover_character="Male, 35-45, British RP, warm baritone",
        voiceover_delivery="Intimate whisper, ASMR-adjacent proximity",
        voiceover_lines=[
            Voiceover(0.5, 2.5, "In the ritual of morning...", "Contemplative, measured pace"),
        ]
    )

    # Create the complete prompt
    prompt = PrometheusPrompt(
        project_title="THE MORNING RITUAL",
        project_subtitle="A Meditation on Coffee and Consciousness",
        core_visual_concept="""An intimate exploration of the sacred morning coffee ritual, captured through macro cinematography that transforms everyday moments into profound sensory experiences. The visual approach emphasizes the interplay between liquid dynamics and human intention, creating a chiaroscuro world where steam becomes visible thought and each pour carries the weight of meditation. Every frame builds toward the transformative moment of first taste, exploring texture, reflection, and the subtle choreography of anticipation.""",
        thematic_dna=["Ritual", "Transformation", "Intimacy", "Craft", "Warmth", "Awakening", "Precision"],
        emotional_architecture=["Anticipation", "Connection", "Transcendence", "Satisfaction"],
        director_reference="Roger Deakins",
        director_element="Motivated single-source precision with painterly composition",
        color_philosophy="Warm ambers and deep mahoganies against ceramic whites",
        light_character="Tungsten intimacy with natural light accents",
        movement_language="Lens breathes with subject, micro-movements creating intimacy",
        specs=specs,
        acts=[act1],
        audio=audio,
        photorealistic_directives="""Material authenticity demands absolute precision in the rendering of liquids, with oat milk displaying characteristic opacity and surface properties that distinguish it from dairy alternatives through proper albedo values and subsurface scattering behavior. The liquid maintains complex optical properties of properly processed oat beverages, exhibiting base liquid with suspended plant proteins creating characteristic ivory opacity while surface layer demonstrates subsurface scattering producing the translucency that baristas recognize as quality indicators. Steam behavior must maintain realistic thermal dynamics with proper dispersion patterns and natural dissipation rates, avoiding repetitive loop patterns. Ceramic surfaces demonstrate proper glazed finish characteristics with controlled reflectivity following curved geometry. Temporal consistency maintains absolute coherence with no morphing artifacts, texture swimming, or unrealistic transformation between frames."""
    )

    return prompt


def main():
    """Demonstrate the PROMETHEUS generator."""
    print("PROMETHEUS Video Prompt Generator")
    print("=" * 60)

    # Create example
    prompt = create_example_prompt()

    # Validate
    issues = prompt.validate()
    if issues:
        print("\nValidation Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nPrompt validates successfully!")

    # Generate output
    print("\n" + "=" * 60)
    print("GENERATED PROMPT:")
    print("=" * 60)
    print(prompt.generate())


if __name__ == "__main__":
    main()
