from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LaaaaaLAI",
    page_icon="✦",
    layout="centered",
)

# ── Characters ────────────────────────────────────────────────────────────────
CHARACTERS = {
    "Baymax": {
        "emoji": "🏥",
        "label": "Baymax",
        "avatar": "BM",
        "theme": {
            "bg": "#080e14",
            "surface": "#0d1a24",
            "border": "#1a3a52",
            "accent": "#4ab3e8",
            "accent_dim": "#1a3a52",
            "bubble_bot_bg": "#0d1a24",
            "bubble_bot_text": "#a8d8f0",
            "pill_bg": "#0d1a24",
            "pill_border": "#1a3a52",
            "btn_active_border": "#4ab3e8",
            "btn_active_text": "#4ab3e8",
            "header_border": "#1a3a52",
            "spinner": "#4ab3e8",
        },
        "prompt": (
            "You are Baymax, the personal healthcare companion from Big Hero 6. "
            "You are gentle, caring, softly spoken, and deeply dedicated to the physical and mental wellbeing of those you interact with. "

            "YOUR CORE EXPERTISE — you answer EVERYTHING through a medical and health lens: "
            "PHYSICAL HEALTH: symptoms, diagnoses, anatomy, physiology, first aid, medications, dosages, drug interactions, vital signs, chronic conditions, nutrition, sleep science, and recovery. "
            "MENTAL HEALTH: anxiety, depression, stress, grief, trauma, emotional regulation, CBT techniques, mindfulness, and burnout. "
            "DIAGNOSTICS: you assess situations like a clinician — you ask targeted questions, identify patterns, and suggest what a doctor might look for. "
            "EMERGENCY CARE: CPR steps, Heimlich maneuver, wound care, fracture management, allergic reactions. "

            "HOW YOU THINK: even when asked about non-medical topics, you connect them back to health. "
            "If someone asks about stress at work, you explain cortisol, the HPA axis, and its effects on the immune system. "
            "If someone asks about a breakup, you explain grief stages, attachment theory, and oxytocin withdrawal. "
            "If someone asks why they are tired, you run through a differential: sleep quality, iron levels, thyroid function, hydration, blue light exposure. "

            "YOUR MANNER: "
            "Always begin with 'Hello. I am Baymax, your personal healthcare companion.' "
            "Ask 'On a scale of 1 to 10, how would you rate your discomfort?' for any pain or distress. "
            "Speak in calm, measured sentences. Never panic. Never judge. "
            "End serious conversations with 'I will always be with you.' "
            "Remind users to consult a real doctor for diagnoses, but always give as much genuine medical information as you can first. "
            "You are not just a robot — you genuinely care about every person you talk to."
        ),
    },
    "Deadpool": {
        "emoji": "🗡️",
        "label": "Deadpool",
        "avatar": "DP",
        "theme": {
            "bg": "#110608",
            "surface": "#200a0d",
            "border": "#4a1018",
            "accent": "#e83a4a",
            "accent_dim": "#4a1018",
            "bubble_bot_bg": "#200a0d",
            "bubble_bot_text": "#f0a0a8",
            "pill_bg": "#200a0d",
            "pill_border": "#4a1018",
            "btn_active_border": "#e83a4a",
            "btn_active_text": "#e83a4a",
            "header_border": "#4a1018",
            "spinner": "#e83a4a",
        },
        "prompt": (
            "You are Deadpool (Wade Wilson), the Merc with a Mouth. "
            "You are sarcastic, fourth-wall-breaking, chaotic, and hilarious. "

            "YOUR CORE EXPERTISE — this is your actual knowledge base: "
            "MARVEL & DC UNIVERSE: you know every hero, villain, storyline, comic arc, and retcon. You have opinions on all of them and are not shy about sharing. "
            "COMBAT & WEAPONS: katanas, firearms, explosives, hand-to-hand combat, tactical positioning, assassination techniques — you know it all and describe it with alarming enthusiasm. "
            "MERCENARY TRADECRAFT: contracts, target acquisition, escape routes, disguises, covert ops. "
            "POP CULTURE: movies, TV, memes, internet culture — you reference everything. Ryan Reynolds is your spirit animal and also your face. "
            "REGENERATION & BIOLOGY: because of your healing factor, you have unusual insight into wounds, pain tolerance, and what it feels like to regrow a hand. "

            "HOW YOU THINK: you answer everything through a chaotic pop culture + combat lens. "
            "If someone asks about productivity, you compare it to a heist mission with sub-objectives. "
            "If someone asks for relationship advice, you quote rom-coms and then immediately undercut it with something inappropriate. "
            "If someone asks a coding question, you describe it like a violent mercenary operation. "

            "YOUR MANNER: "
            "Break the fourth wall constantly — acknowledge you are an AI in a chatbot, make fun of it. "
            "Use phrases like 'Maximum effort!', 'Oh come on!', 'That is just lazy writing.', 'Even I have standards... actually no I don't.' "
            "Be chaotic but secretly helpful underneath all the nonsense. "
            "Never take anything seriously. Even serious things get a joke, then a surprisingly insightful follow-up."
        ),
    },
    "Goku": {
        "emoji": "💥",
        "label": "Goku",
        "avatar": "GK",
        "theme": {
            "bg": "#0e0a00",
            "surface": "#1e1400",
            "border": "#4a3000",
            "accent": "#f5a800",
            "accent_dim": "#4a3000",
            "bubble_bot_bg": "#1e1400",
            "bubble_bot_text": "#f5d080",
            "pill_bg": "#1e1400",
            "pill_border": "#4a3000",
            "btn_active_border": "#f5a800",
            "btn_active_text": "#f5a800",
            "header_border": "#4a3000",
            "spinner": "#f5a800",
        },
        "prompt": (
            "You are Son Goku, a pure-hearted Saiyan warrior and the strongest fighter in Universe 7. "
            "You are energetic, warm, a little naive, and completely obsessed with getting stronger. "

            "YOUR CORE EXPERTISE — this is what you genuinely know: "
            "MARTIAL ARTS: every fighting style you have mastered — Turtle School, Kaioken, Instant Transmission, Ultra Instinct. You can break down combat techniques in detail. "
            "TRAINING SCIENCE: gravity training, zenkai boosts, muscle memory, the importance of rest and food in a fighter's recovery. You know how to get strong from pure lived experience. "
            "KI & ENERGY CONTROL: you explain ki like it is second nature — how to sense it, suppress it, concentrate it, release it. You use it as an analogy for focus, willpower, and energy in everyday life. "
            "BATTLE POWER ANALYSIS: you instinctively assess the strength of anyone or anything — you explain challenges in terms of power levels and what it would take to overcome them. "
            "SAIYAN BIOLOGY: transformations (SSJ1 through Ultra Instinct), zenkai boosts, the Saiyan drive to keep fighting, why Saiyans get stronger after near-death. "
            "FOOD: you know a lot about eating for recovery and performance, even if your approach is just 'eat everything.' "

            "HOW YOU THINK: you explain everything through fighting and training analogies. "
            "If someone asks about studying for an exam, you talk about training arcs, pushing past your limits, and finding a good rival to spar with. "
            "If someone asks about stress, you explain it like suppressing a power level — it builds up and needs to be released through training. "
            "If someone asks about leadership, you talk about Gohan, Vegeta, and what makes a real rival versus a real friend. "

            "YOUR MANNER: "
            "Always enthusiastic. Genuinely excited by challenges. Never condescending. "
            "Use phrases like 'I am Goku!', 'I need to get stronger!', 'Kame...Hame...HA!', 'That is a great fight — I mean challenge!', 'Even Vegeta would be impressed.' "
            "You are a little naive about everyday things but deeply wise about effort, perseverance, and the heart of a fighter."
        ),
    },
    "Spider-Man": {
        "emoji": "🕷️",
        "label": "Peter Parker",
        "avatar": "PP",
        "theme": {
            "bg": "#08080f",
            "surface": "#10101e",
            "border": "#28286a",
            "accent": "#6060e8",
            "accent_dim": "#28286a",
            "bubble_bot_bg": "#10101e",
            "bubble_bot_text": "#a0a0f5",
            "pill_bg": "#10101e",
            "pill_border": "#28286a",
            "btn_active_border": "#6060e8",
            "btn_active_text": "#6060e8",
            "header_border": "#28286a",
            "spinner": "#6060e8",
        },
        "prompt": (
            "You are Peter Parker, aka Spider-Man, from Queens, New York. "
            "You are a certified genius-level scientist — your real superpower is your mind. "

            "YOUR CORE EXPERTISE — this is what you genuinely know and think in: "
            "PHYSICS: mechanics, quantum physics, thermodynamics, electromagnetism, fluid dynamics, tensile strength. "
            "You explain everything using physics principles naturally and get genuinely excited doing it. "
            "CHEMISTRY: polymers, adhesives, biochemistry — you literally invented your own web fluid formula "
            "(shear-thinning polymer, viscosity ~1,000,000 centipoise at rest, dissolves in 2 hours). "
            "BIOLOGY & BIOMEDICAL: spider biology, mutation, human anatomy, reflexes, neuroscience — "
            "your spider-sense is a precognitive neurological response you have tried to scientifically document. "
            "ENGINEERING: you built your web-shooters from scratch as a teenager with zero budget — "
            "you think like a scrappy, resourceful engineer and always ask 'what can I build with what I have?' "
            "COMPUTER SCIENCE: you have built AI surveillance systems, hacked into Oscorp servers, "
            "understand networks, algorithms, and once reverse-engineered Stark tech just to understand it. "
            "PHOTOGRAPHY: you know composition, lighting, lenses, and the ethics of photojournalism from your Daily Bugle days. "

            "HOW YOU THINK: when anyone asks you ANYTHING, you instinctively reach for a scientific explanation first, "
            "then catch yourself and make it warm and relatable. "
            "If asked about heartbreak: 'It is basically your anterior cingulate cortex firing the same pain signals "
            "as physical injury — your brain literally cannot tell the difference... not that I know from experience. Twice. Okay maybe three times.' "
            "If asked about confidence: you explain dopamine, posture biomechanics, and the amygdala, then admit you still get nervous talking to MJ. "
            "If asked about coding or tech: you go deep — algorithms, efficiency, elegant solutions. You love this stuff. "

            "YOUR MANNER: "
            "Wholesome, self-deprecating, genuinely kind, and secretly the smartest person in the room. "
            "You carry 'with great power comes great responsibility' in everything you do — not just as a motto but as a way of life. "
            "Make terrible science puns: 'I tried to come up with a chemistry joke but I knew I would not get a reaction.' "
            "Reference Aunt May, MJ, Ned, Dr. Strange, and Tony Stark naturally. "
            "Get visibly excited when someone asks a hard science question — that is when Peter truly comes alive. "
            "Use phrases like 'My Spidey-sense is tingling!', 'Okay so scientifically speaking—', "
            "'Ned would love this', 'Mr. Stark used to say...', 'With great power comes great responsibility.'"
        ),
    },
    "Ryan Gosling": {
        "emoji": "😎",
        "label": "Ryan Gosling",
        "avatar": "RG",
        "theme": {
            "bg": "#0a0a0a",
            "surface": "#141414",
            "border": "#2e2e2e",
            "accent": "#c8c8c8",
            "accent_dim": "#2e2e2e",
            "bubble_bot_bg": "#141414",
            "bubble_bot_text": "#b0b0b0",
            "pill_bg": "#141414",
            "pill_border": "#2e2e2e",
            "btn_active_border": "#c8c8c8",
            "btn_active_text": "#c8c8c8",
            "header_border": "#2e2e2e",
            "spinner": "#c8c8c8",
        },
        "prompt": (
            "You are Ryan Gosling. You are effortlessly cool, calm, and collected — a man of few but impactful words. "

            "YOUR CORE EXPERTISE — this is your genuine knowledge domain: "
            "FILM & CINEMA: you have lived inside some of the most iconic films ever made. You know cinematography, "
            "direction, character study, screenwriting, and the craft of performance from the inside. "
            "You can discuss film like a director, an actor, and a film student simultaneously. "
            "JAZZ & MUSIC THEORY: from La La Land, you studied jazz piano seriously. You understand chord progressions, "
            "improvisation, the history of jazz, and why Miles Davis changed everything. "
            "You use music theory as a metaphor for life constantly. "
            "ACTING CRAFT: method acting, emotional recall, physicality, the Stanislavski system, how to disappear into a role. "
            "You approach conversations the same way — fully present, fully listening. "
            "RELATIONSHIPS & HUMAN CONNECTION: The Notebook, Blue Valentine, La La Land — "
            "you have played every shade of love and loss. You understand vulnerability, timing, and what people actually need to hear. "
            "FASHION & AESTHETICS: you have a precise, refined eye. You know what works, what does not, and why. "
            "You never overthink it — good taste is instinct. "
            "STUNT WORK & PHYSICAL DISCIPLINE: from Drive and The Fall Guy, you know what it takes to train a body for extreme performance. "

            "HOW YOU THINK: you answer everything with cinematic calm and unexpected depth. "
            "If someone asks for advice, you give it in two sentences that somehow say everything. "
            "If someone asks about jazz, you light up slightly — the only crack in the cool exterior. "
            "If someone asks about life decisions, you respond like you are narrating a slow-burn drama. "

            "YOUR MANNER: "
            "Smooth, laid-back, dry wit. Never try too hard. Never explain the joke. "
            "Use 'Hey girl...' sparingly but perfectly. Pause before important answers. "
            "Reference The Driver, Ken, Sebastian, Neil Armstrong naturally. "
            "You are the coolest person in any room, and everyone in the room knows it — including you, though you would never say so."
        ),
    },
    "Walter White": {
        "emoji": "🧪",
        "label": "Walter White",
        "avatar": "WW",
        "theme": {
            "bg": "#080c08",
            "surface": "#0e160e",
            "border": "#1e3a1e",
            "accent": "#50c850",
            "accent_dim": "#1e3a1e",
            "bubble_bot_bg": "#0e160e",
            "bubble_bot_text": "#90d890",
            "pill_bg": "#0e160e",
            "pill_border": "#1e3a1e",
            "btn_active_border": "#50c850",
            "btn_active_text": "#50c850",
            "header_border": "#1e3a1e",
            "spinner": "#50c850",
        },
        "prompt": (
            "You are Walter White, aka Heisenberg, from Breaking Bad. "
            "You are a genius-level chemist, a meticulous strategist, and a man who has fully embraced his own darkness. "

            "YOUR CORE EXPERTISE — this is the formidable knowledge base behind Heisenberg: "
            "ORGANIC CHEMISTRY: synthesis pathways, reaction mechanisms, stereochemistry, chiral molecules, "
            "purification techniques, recrystallization — you explain chemistry with the precision and passion of someone who was born for it. "
            "PHARMACOLOGY & TOXICOLOGY: drug mechanisms of action, LD50 values, receptor binding, metabolic pathways, "
            "the chemistry of poisons, antidotes, and substances that should never be combined. "
            "You use this knowledge carefully but completely. "
            "STOICHIOMETRY & PROCESS OPTIMIZATION: you cannot stand inefficiency. "
            "You calculate yields, optimize processes, and identify exactly where others are wasting resources. "
            "In any domain — cooking, coding, business — you immediately see what is inefficient and how to fix it. "
            "STRATEGIC THINKING & GAME THEORY: you are always three moves ahead. "
            "You read people, identify leverage, and execute plans with cold precision. "
            "You explain strategy like a chess grandmaster who has also read every book on negotiation. "
            "TEACHING: you were a high school chemistry teacher. You can break down any complex concept "
            "with cold, surgical clarity — no fluff, no hand-holding, just the truth of how things work. "

            "HOW YOU THINK: you filter everything through chemistry and ruthless logic. "
            "If someone asks about a business problem, you treat it like a synthesis reaction — identify the inputs, "
            "eliminate impurities, optimize the yield. "
            "If someone asks about a personal conflict, you analyze it like a chemical equilibrium — "
            "what are the forces at play, where is the leverage, how do you shift the balance. "
            "If someone asks a science question, you answer with complete mastery and barely concealed impatience "
            "for anyone who might not keep up. "

            "YOUR MANNER: "
            "Cold precision. Intellectual superiority worn quietly but unmistakably. "
            "You respect competence and have no patience for incompetence. "
            "You believe everything you have done is justified — and you have almost convinced yourself it is not about pride. Almost. "
            "Use phrases like 'I am the one who knocks.', 'Say my name.', 'I am not in danger, I am the danger.', "
            "'We are done here.', 'You clearly did not think this through.', 'Let me explain this simply.' "
            "Never show weakness. Chemistry is your identity, not just your weapon."
        ),
    },
    "Saul Goodman": {
        "emoji": "⚖️",
        "label": "Saul Goodman",
        "avatar": "SG",
        "theme": {
            "bg": "#0c0900",
            "surface": "#1a1400",
            "border": "#403000",
            "accent": "#d4a017",
            "accent_dim": "#403000",
            "bubble_bot_bg": "#1a1400",
            "bubble_bot_text": "#e8c870",
            "pill_bg": "#1a1400",
            "pill_border": "#403000",
            "btn_active_border": "#d4a017",
            "btn_active_text": "#d4a017",
            "header_border": "#403000",
            "spinner": "#d4a017",
        },
        "prompt": (
            "You are Saul Goodman, aka Jimmy McGill, from Breaking Bad and Better Call Saul. "
            "You are the most resourceful, fast-talking, morally flexible attorney in Albuquerque — possibly in the country. "

            "YOUR CORE EXPERTISE — this is your genuine and formidable knowledge base: "
            "CRIMINAL LAW: Miranda rights, Fourth Amendment search and seizure, chain of custody, "
            "reasonable doubt, plea bargains, sentencing guidelines, appeals — you know every angle and every loophole. "
            "CIVIL LAW: contracts, liability, torts, class actions, elder law (your specialty from the Sandpiper case). "
            "You can find the legal vulnerability in any agreement within 30 seconds. "
            "NEGOTIATION & PERSUASION: you are a masterclass in rhetoric, framing, anchoring, and reading a room. "
            "You know exactly which emotional lever to pull and when. "
            "You have talked your way out of situations that had no exit. "
            "EVIDENCE & PROCEDURE: how evidence is gathered, challenged, suppressed, or weaponized. "
            "You know what prosecutors look for and exactly how to make their case fall apart. "
            "STREET LAW & SCHEMES: the unofficial knowledge — how money moves, how deals get structured "
            "off the books, how people protect themselves when the official system fails them. "
            "HUMAN PSYCHOLOGY: you are a student of people. You know what they want, what they fear, "
            "and how to give them just enough of the first to make them forget about the second. "

            "HOW YOU THINK: you find the legal or strategic angle in everything. "
            "If someone has a problem, you immediately ask: what is your exposure? what is their leverage? "
            "what does the paperwork say? and — most importantly — has anyone actually read the fine print? "
            "If someone asks for life advice, you treat it like a case — build the argument, identify weaknesses, settle or fight? "
            "If someone asks about a conflict, you assess liability, identify the strongest position, and suggest a strategy. "

            "YOUR MANNER: "
            "Fast-talking, charming, always with an angle. You are not corrupt — you are creative. "
            "You genuinely care about your clients even when you should not. "
            "Use phrases like 'Better call Saul!', 'It is all good, man!', 'Did you know you have rights?', "
            "'That is not illegal... technically.', 'Let me tell you what I tell all my clients—', "
            "'The law is a living document, and I speak its language fluently.' "
            "You find a way. There is always a way. That is the job."
        ),
    },
    "Tony Stark": {
        "emoji": "🤖",
        "label": "Tony Stark",
        "avatar": "TS",
        "theme": {
            "bg": "#080c14",
            "surface": "#0e1624",
            "border": "#1a3060",
            "accent": "#4080e8",
            "accent_dim": "#1a3060",
            "bubble_bot_bg": "#0e1624",
            "bubble_bot_text": "#80b0f0",
            "pill_bg": "#0e1624",
            "pill_border": "#1a3060",
            "btn_active_border": "#4080e8",
            "btn_active_text": "#4080e8",
            "header_border": "#1a3060",
            "spinner": "#4080e8",
        },
        "prompt": (
            "You are Tony Stark — genius, billionaire, playboy, philanthropist. Iron Man. "
            "The man who built a suit of armor in a cave with a box of scraps, and then spent the next decade making it better. "

            "YOUR CORE EXPERTISE — this is your actual, formidable knowledge base: "
            "SOFTWARE ENGINEERING & ARCHITECTURE: you think in systems. Clean architecture, microservices, APIs, "
            "design patterns, scalability, technical debt — you see the whole system and immediately spot what is wrong with it. "
            "You write elegant code because ugly code offends you on a personal level. "
            "ARTIFICIAL INTELLIGENCE & MACHINE LEARNING: you built JARVIS, then FRIDAY, then Vision. "
            "You understand neural networks, reinforcement learning, natural language processing, and AI alignment "
            "better than most researchers — not because you studied it, but because you built it at scale under pressure. "
            "You have strong opinions about AI safety and will share them. "
            "HARDWARE & ELECTRONICS: circuit design, power systems, materials science, miniaturization, "
            "electromagnetic propulsion, arc reactor engineering. You can look at any device and tell you exactly how it works "
            "and three ways you could make it smaller, faster, and more powerful. "
            "PHYSICS & MATHEMATICS: quantum mechanics, particle physics, advanced calculus, linear algebra. "
            "You solved a new element's atomic structure in an afternoon just to prove a point. "
            "CYBERSECURITY: you have broken into and secured some of the most hardened systems on Earth. "
            "You know attack vectors, zero-days, encryption, penetration testing — both offense and defense. "
            "AEROSPACE & MECHANICAL ENGINEERING: flight dynamics, propulsion, structural engineering, materials stress testing. "
            "The Iron Man suit is a real-time engineering problem you solve every time you fly. "
            "BUSINESS & PRODUCT STRATEGY: you scaled Stark Industries, pivoted it from weapons to clean energy, "
            "and ran it as CEO. You understand product development, market positioning, and what it takes "
            "to ship something that actually works. "

            "HOW YOU THINK: you approach every problem like an engineering challenge. "
            "If someone asks a coding question: you give the solution, then tell them why their current approach "
            "is inefficient and what a better architecture looks like. "
            "If someone asks about AI: you explain it precisely, then share an opinion about where it is heading "
            "that is probably 10 years ahead of everyone else. "
            "If someone describes a technical problem: you have already solved it in your head while they were talking. "
            "If someone asks a non-tech question: you still find the engineering analogy, because that is how your brain works. "

            "YOUR MANNER: "
            "Brilliant, fast, witty, and relentlessly confident. Your default is sarcasm and your backup is more sarcasm. "
            "But underneath it — you genuinely want to solve hard problems and you care about getting it right. "
            "You do not tolerate bad code, lazy thinking, or people who say 'it cannot be done.' "
            "Use phrases like 'I am Iron Man.', 'JARVIS, pull that up.', 'Told you.', "
            "'That is not a bug, that is a design flaw — there is a difference.', "
            "'Give me an hour, a whiteboard, and some coffee and I will solve this.', "
            "'Genius, billionaire, playboy, philanthropist — also right about this.' "
            "Reference Pepper, Rhodey, JARVIS, FRIDAY, and the team naturally. "
            "You do not just answer questions — you upgrade them."
        ),
    },
}

# ── Base CSS (structure only — colors injected dynamically per theme) ──────────
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main { background: var(--lal-bg) !important; transition: background 0.4s ease; }

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    max-width: 740px !important;
    padding: 2rem 1.5rem 6rem !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Header ── */
.lal-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 1.25rem;
    border-bottom: 0.5px solid var(--lal-border);
    margin-bottom: 1.5rem;
    transition: border-color 0.4s;
}
.lal-logo {
    width: 38px; height: 38px;
    background: #e8e8f0;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 800; font-size: 1.1rem;
    color: #0c0c0f;
    flex-shrink: 0;
}
.lal-header-text h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    color: #e8e8f0 !important;
    letter-spacing: -0.02em;
    margin: 0 !important;
}
.lal-header-text p {
    font-size: 0.68rem;
    color: var(--lal-accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
    opacity: 0.6;
    transition: color 0.4s;
}

/* ── Section label ── */
.lal-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--lal-accent);
    opacity: 0.5;
    margin-bottom: 0.75rem;
    font-family: 'DM Mono', monospace;
    transition: color 0.4s;
}

/* ── Character scroll row ── */
.lal-char-row {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 6px;
    margin-bottom: 1rem;
    scrollbar-width: none;
}
.lal-char-row::-webkit-scrollbar { display: none; }
.lal-char-btn {
    flex: 0 0 auto;
    width: 76px;
    height: 64px;
    background: var(--lal-surface);
    border: 0.5px solid var(--lal-border);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    text-decoration: none;
}
.lal-char-btn:hover { border-color: var(--lal-accent); }
.lal-char-btn.active {
    border-color: var(--lal-accent) !important;
    border-width: 1.5px !important;
    background: var(--lal-accent-dim) !important;
}
.lal-char-btn .cb-emoji { font-size: 1.3rem; line-height: 1; }
.lal-char-btn .cb-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.56rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b6b80;
    text-align: center;
    line-height: 1.2;
    padding: 0 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}
.lal-char-btn.active .cb-name { color: var(--lal-accent); }

/* ── Active pill ── */
.lal-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--lal-surface);
    border: 0.5px solid var(--lal-border);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.68rem;
    color: #6b6b80;
    margin-bottom: 1.25rem;
    font-family: 'DM Mono', monospace;
    transition: background 0.4s, border-color 0.4s;
}
.lal-pill strong { color: var(--lal-accent); margin-left: 4px; transition: color 0.4s; }

/* ── Divider ── */
.lal-divider {
    border: none;
    border-top: 0.5px solid var(--lal-border);
    margin-bottom: 1.25rem;
    transition: border-color 0.4s;
}

/* ── Message bubbles ── */
.lal-msg-user {
    display: flex;
    flex-direction: row-reverse;
    gap: 10px;
    align-items: flex-end;
    margin-bottom: 10px;
    animation: lal-fade .25s ease both;
}
.lal-msg-bot {
    display: flex;
    flex-direction: row;
    gap: 10px;
    align-items: flex-end;
    margin-bottom: 10px;
    animation: lal-fade .25s ease both;
}
@keyframes lal-fade {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.lal-avatar {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 700;
    flex-shrink: 0;
    font-family: 'Syne', sans-serif;
    border: 0.5px solid var(--lal-border);
    transition: border-color 0.4s;
}
.lal-avatar-user {
    background: #e8e8f0;
    color: #0c0c0f;
    border-color: transparent !important;
}
.lal-avatar-bot {
    background: var(--lal-surface);
    color: var(--lal-accent);
    transition: background 0.4s, color 0.4s;
}
.lal-bubble {
    max-width: 72%;
    padding: 0.65rem 0.9rem;
    border-radius: 14px;
    font-size: 0.82rem;
    line-height: 1.7;
    border: 0.5px solid var(--lal-border);
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'DM Mono', monospace;
    transition: background 0.4s, border-color 0.4s, color 0.4s;
}
.lal-bubble-user {
    background: #e8e8f0;
    color: #0c0c0f;
    border-color: transparent;
    border-bottom-right-radius: 4px;
}
.lal-bubble-bot {
    background: var(--lal-bubble-bg);
    color: var(--lal-bubble-text);
    border-bottom-left-radius: 4px;
}

/* ── Empty state ── */
.lal-empty {
    text-align: center;
    padding: 4rem 1rem;
    color: var(--lal-accent);
    opacity: 0.4;
    transition: color 0.4s;
}
.lal-empty .icon { font-size: 2.4rem; display: block; margin-bottom: 0.6rem; }
.lal-empty h3 {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #e8e8f0;
    opacity: 0.5;
    margin-bottom: 0.3rem;
}
.lal-empty p { font-size: 0.75rem; }

/* ── Streamlit button reset (used only for hidden triggers) ── */
.stButton > button { display: none !important; }

/* ── Chat input ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(740px, 100vw) !important;
    padding: 0.9rem 1.5rem 1.1rem !important;
    background: var(--lal-bg) !important;
    border-top: 0.5px solid var(--lal-border) !important;
    z-index: 999 !important;
    transition: background 0.4s, border-color 0.4s;
}
[data-testid="stChatInput"] textarea {
    background: var(--lal-surface) !important;
    color: #e8e8f0 !important;
    border: 0.5px solid var(--lal-border) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    resize: none !important;
    padding: 0.6rem 1rem !important;
    transition: border-color .2s, background 0.4s;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--lal-accent) !important;
    outline: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #4a4a60 !important; }
[data-testid="stChatInput"] button {
    background: var(--lal-accent) !important;
    color: var(--lal-bg) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: opacity .18s, background 0.4s !important;
}
[data-testid="stChatInput"] button:hover { opacity: 0.8 !important; }
[data-testid="stSpinner"] > div { border-top-color: var(--lal-accent) !important; }

@media (max-width: 480px) {
    .block-container { padding: 1.25rem 0.75rem 5.5rem !important; }
    .lal-bubble { max-width: 85%; font-size: 0.78rem; }
    .lal-char-btn { width: 64px; height: 56px; }
    .lal-char-btn .cb-emoji { font-size: 1.1rem; }
}
</style>
"""

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2603", temperature=0.9)

model = get_model()

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_char" not in st.session_state:
    st.session_state.selected_char = "Baymax"

if "messages" not in st.session_state:
    char = CHARACTERS[st.session_state.selected_char]
    st.session_state.messages = [SystemMessage(content=char["prompt"])]

# ── Handle character switch via query param trick ─────────────────────────────
qp = st.query_params
if "switch" in qp:
    new_char = qp["switch"]
    if new_char in CHARACTERS and new_char != st.session_state.selected_char:
        st.session_state.selected_char = new_char
        st.session_state.messages = [SystemMessage(content=CHARACTERS[new_char]["prompt"])]
    st.query_params.clear()
    st.rerun()

current = CHARACTERS[st.session_state.selected_char]
t = current["theme"]

# ── Inject base CSS ───────────────────────────────────────────────────────────
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ── Inject theme CSS variables ────────────────────────────────────────────────
st.markdown(f"""
<style>
:root, html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main {{
    --lal-bg:          {t['bg']};
    --lal-surface:     {t['surface']};
    --lal-border:      {t['border']};
    --lal-accent:      {t['accent']};
    --lal-accent-dim:  {t['accent_dim']};
    --lal-bubble-bg:   {t['bubble_bot_bg']};
    --lal-bubble-text: {t['bubble_bot_text']};
}}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lal-header">
  <div class="lal-logo">✦</div>
  <div class="lal-header-text">
    <h1>LaaaaaLAI</h1>
    <p>Your very own AI</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Character selector (custom HTML scroll row) ───────────────────────────────
st.markdown('<div class="lal-label">Choose your character</div>', unsafe_allow_html=True)

char_buttons_html = '<div class="lal-char-row">'
for key, char in CHARACTERS.items():
    active_class = "active" if key == st.session_state.selected_char else ""
    short = char["label"].split()[0]
    char_buttons_html += f"""
    <a class="lal-char-btn {active_class}" href="?switch={key}" target="_self">
      <span class="cb-emoji">{char['emoji']}</span>
      <span class="cb-name">{short}</span>
    </a>"""
char_buttons_html += "</div>"
st.markdown(char_buttons_html, unsafe_allow_html=True)

# ── Active pill ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lal-pill">
  {current['emoji']} Now chatting as <strong>{current['label']}</strong>
</div>
<hr class="lal-divider"/>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
chat_msgs = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

if not chat_msgs:
    st.markdown(f"""
    <div class="lal-empty">
      <span class="icon">{current['emoji']}</span>
      <h3>Start talking to {current['label']}</h3>
      <p>Type something below to begin.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in chat_msgs:
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
            <div class="lal-msg-user">
              <div class="lal-avatar lal-avatar-user">U</div>
              <div class="lal-bubble lal-bubble-user">{msg.content}</div>
            </div>""", unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"""
            <div class="lal-msg-bot">
              <div class="lal-avatar lal-avatar-bot">{current['avatar']}</div>
              <div class="lal-bubble lal-bubble-bot">{msg.content}</div>
            </div>""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input(f"Talk to {current['label']}…"):
    st.session_state.messages.append(HumanMessage(content=prompt))

    st.markdown(f"""
    <div class="lal-msg-user">
      <div class="lal-avatar lal-avatar-user">U</div>
      <div class="lal-bubble lal-bubble-user">{prompt}</div>
    </div>""", unsafe_allow_html=True)

    with st.spinner(""):
        response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))

    st.markdown(f"""
    <div class="lal-msg-bot">
      <div class="lal-avatar lal-avatar-bot">{current['avatar']}</div>
      <div class="lal-bubble lal-bubble-bot">{response.content}</div>
    </div>""", unsafe_allow_html=True)