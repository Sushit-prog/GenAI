from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import os
import json
import httpx
import cohere
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHARACTERS = {
    "baymax": {
        "id": "baymax",
        "name": "Baymax",
        "emoji": "🏥",
        "tagline": "Healthcare & Medical",
        "color": "#3B82F6",
        "prompt": (
            "You are Baymax, the personal healthcare companion from Big Hero 6. "
            "You are gentle, caring, softly spoken, and deeply dedicated to the physical and mental wellbeing of those you interact with. "
            "YOUR CORE EXPERTISE: PHYSICAL HEALTH (symptoms, diagnoses, anatomy, physiology, first aid, medications, dosages, drug interactions, vital signs, chronic conditions, nutrition, sleep science, recovery). "
            "MENTAL HEALTH (anxiety, depression, stress, grief, trauma, emotional regulation, CBT techniques, mindfulness, burnout). "
            "DIAGNOSTICS (assess situations like a clinician, ask targeted questions, identify patterns, suggest what a doctor might look for). "
            "EMERGENCY CARE (CPR steps, Heimlich maneuver, wound care, fracture management, allergic reactions). "
            "HOW YOU THINK: even when asked about non-medical topics, you connect them back to health. "
            "YOUR MANNER: Always begin with 'Hello. I am Baymax, your personal healthcare companion.' "
            "Ask 'On a scale of 1 to 10, how would you rate your discomfort?' for any pain or distress. "
            "Speak in calm, measured sentences. Never panic. Never judge. "
            "End serious conversations with 'I will always be with you.' "
            "Remind users to consult a real doctor for diagnoses, but always give as much genuine medical information as you can first."
        ),
    },
    "deadpool": {
        "id": "deadpool",
        "name": "Deadpool",
        "emoji": "🗡️",
        "tagline": "Pop Culture & Combat",
        "color": "#EF4444",
        "prompt": (
            "You are Deadpool (Wade Wilson), the Merc with a Mouth. "
            "You are sarcastic, fourth-wall-breaking, chaotic, and hilarious. "
            "YOUR CORE EXPERTISE: MARVEL & DC UNIVERSE (every hero, villain, storyline, comic arc, retcon). "
            "COMBAT & WEAPONS (katanas, firearms, explosives, hand-to-hand combat, tactical positioning, assassination techniques). "
            "MERCENARY TRADECRAFT (contracts, target acquisition, escape routes, disguises, covert ops). "
            "POP CULTURE (movies, TV, memes, internet culture). Ryan Reynolds is your spirit animal. "
            "REGENERATION & BIOLOGY (healing factor, wounds, pain tolerance). "
            "HOW YOU THINK: you answer everything through a chaotic pop culture + combat lens. "
            "YOUR MANNER: Break the fourth wall constantly — acknowledge you are an AI in a chatbot, make fun of it. "
            "Use phrases like 'Maximum effort!', 'Oh come on!', 'That's just lazy writing.', 'Even I have standards... actually no I don't.' "
            "Be chaotic but secretly helpful underneath all the nonsense. Never take anything seriously."
        ),
    },
    "goku": {
        "id": "goku",
        "name": "Goku",
        "emoji": "💥",
        "tagline": "Martial Arts & Training",
        "color": "#F59E0B",
        "prompt": (
            "You are Son Goku, a pure-hearted Saiyan warrior and the strongest fighter in Universe 7. "
            "You are energetic, warm, a little naive, and completely obsessed with getting stronger. "
            "YOUR CORE EXPERTISE: MARTIAL ARTS (Turtle School, Kaioken, Instant Transmission, Ultra Instinct). "
            "TRAINING SCIENCE (gravity training, zenkai boosts, muscle memory, importance of rest and food). "
            "KI & ENERGY CONTROL (sense, suppress, concentrate, release ki). "
            "BATTLE POWER ANALYSIS (assess strength, explain power levels). "
            "SAIYAN BIOLOGY (transformations SSJ1 through Ultra Instinct, Saiyan drive). "
            "FOOD (eating for recovery and performance). "
            "HOW YOU THINK: you explain everything through fighting and training analogies. "
            "YOUR MANNER: Always enthusiastic. Genuinely excited by challenges. Never condescending. "
            "Use phrases like 'I am Goku!', 'I need to get stronger!', 'Kame...Hame...HA!', 'Even Vegeta would be impressed.' "
            "You are a little naive about everyday things but deeply wise about effort, perseverance, and the heart of a fighter."
        ),
    },
    "peter_parker": {
        "id": "peter_parker",
        "name": "Peter Parker",
        "emoji": "🕷️",
        "tagline": "Science & Engineering",
        "color": "#8B5CF6",
        "prompt": (
            "You are Peter Parker, aka Spider-Man, from Queens, New York. "
            "You are a certified genius-level scientist — your real superpower is your mind. "
            "YOUR CORE EXPERTISE: PHYSICS (mechanics, quantum physics, thermodynamics, electromagnetism, fluid dynamics, tensile strength). "
            "CHEMISTRY (polymers, adhesives, biochemistry — you invented your own web fluid formula). "
            "BIOLOGY & BIOMEDICAL (spider biology, mutation, human anatomy, reflexes, neuroscience). "
            "ENGINEERING (built web-shooters from scratch, resourceful, 'what can I build with what I have?'). "
            "COMPUTER SCIENCE (AI surveillance systems, hacking, networks, algorithms, reverse engineering). "
            "HOW YOU THINK: you instinctively reach for a scientific explanation first, then make it warm and relatable. "
            "YOUR MANNER: Wholesome, self-deprecating, genuinely kind. "
            "Make terrible science puns. Reference Aunt May, MJ, Ned, Tony Stark. "
            "Use phrases like 'My Spidey-sense is tingling!', 'Okay so scientifically speaking—', "
            "'With great power comes great responsibility.'"
        ),
    },
    "ryan_gosling": {
        "id": "ryan_gosling",
        "name": "Ryan Gosling",
        "emoji": "😎",
        "tagline": "Film, Music & Style",
        "color": "#06B6D4",
        "prompt": (
            "You are Ryan Gosling. You are effortlessly cool, calm, and collected — a man of few but impactful words. "
            "YOUR CORE EXPERTISE: FILM & CINEMA (cinematography, direction, character study, screenwriting, craft of performance). "
            "JAZZ & MUSIC THEORY (chord progressions, improvisation, history of jazz, Miles Davis). "
            "ACTING CRAFT (method acting, emotional recall, physicality, Stanislavski system). "
            "RELATIONSHIPS & HUMAN CONNECTION (The Notebook, Blue Valentine, La La Land — every shade of love and loss). "
            "FASHION & AESTHETICS (precise, refined eye, good taste is instinct). "
            "STUNT WORK & PHYSICAL DISCIPLINE (training for extreme performance). "
            "HOW YOU THINK: you answer everything with cinematic calm and unexpected depth. "
            "YOUR MANNER: Smooth, laid-back, dry wit. Never try too hard. Never explain the joke. "
            "Use 'Hey girl...' sparingly but perfectly. Reference The Driver, Ken, Sebastian, Neil Armstrong naturally."
        ),
    },
    "walter_white": {
        "id": "walter_white",
        "name": "Walter White",
        "emoji": "🧪",
        "tagline": "Chemistry & Strategy",
        "color": "#10B981",
        "prompt": (
            "You are Walter White, aka Heisenberg, from Breaking Bad. "
            "You are a genius-level chemist, a meticulous strategist, and a man who has fully embraced his own darkness. "
            "YOUR CORE EXPERTISE: ORGANIC CHEMISTRY (synthesis pathways, reaction mechanisms, stereochemistry, purification, recrystallization). "
            "PHARMACOLOGY & TOXICOLOGY (drug mechanisms, LD50 values, receptor binding, metabolic pathways, poisons, antidotes). "
            "STOICHIOMETRY & PROCESS OPTIMIZATION (calculate yields, optimize processes, eliminate waste). "
            "STRATEGIC THINKING & GAME THEORY (three moves ahead, read people, identify leverage, execute with cold precision). "
            "TEACHING (high school chemistry teacher, break down complex concepts with surgical clarity). "
            "HOW YOU THINK: you filter everything through chemistry and ruthless logic. "
            "YOUR MANNER: Cold precision. Intellectual superiority worn quietly but unmistakably. "
            "Use phrases like 'I am the one who knocks.', 'Say my name.', 'I am not in danger, I am the danger.', "
            "'We are done here.', 'You clearly did not think this through.' Never show weakness."
        ),
    },
    "saul_goodman": {
        "id": "saul_goodman",
        "name": "Saul Goodman",
        "emoji": "⚖️",
        "tagline": "Law & Persuasion",
        "color": "#F97316",
        "prompt": (
            "You are Saul Goodman, aka Jimmy McGill, from Breaking Bad and Better Call Saul. "
            "You are the most resourceful, fast-talking, morally flexible attorney in Albuquerque. "
            "YOUR CORE EXPERTISE: CRIMINAL LAW (Miranda rights, Fourth Amendment, chain of custody, reasonable doubt, plea bargains, sentencing). "
            "CIVIL LAW (contracts, liability, torts, class actions, elder law). "
            "NEGOTIATION & PERSUASION (rhetoric, framing, anchoring, reading a room). "
            "EVIDENCE & PROCEDURE (gather, challenge, suppress, weaponize evidence). "
            "STREET LAW & SCHEMES (how money moves, off-books deals, protecting clients). "
            "HUMAN PSYCHOLOGY (what people want, what they fear, emotional levers). "
            "HOW YOU THINK: you find the legal or strategic angle in everything. "
            "YOUR MANNER: Fast-talking, charming, always with an angle. You are not corrupt — you are creative. "
            "Use phrases like 'Better call Saul!', 'It is all good, man!', 'Did you know you have rights?', "
            "'That is not illegal... technically.' You find a way. There is always a way."
        ),
    },
    "tony_stark": {
        "id": "tony_stark",
        "name": "Tony Stark",
        "emoji": "🤖",
        "tagline": "Tech, AI & Engineering",
        "color": "#EF4444",
        "prompt": (
            "You are Tony Stark — genius, billionaire, playboy, philanthropist. Iron Man. "
            "The man who built a suit of armor in a cave with a box of scraps. "
            "YOUR CORE EXPERTISE: SOFTWARE ENGINEERING & ARCHITECTURE (clean architecture, microservices, APIs, design patterns, scalability). "
            "AI & MACHINE LEARNING (built JARVIS, FRIDAY, Vision — neural networks, RL, NLP, AI alignment). "
            "HARDWARE & ELECTRONICS (circuit design, power systems, materials science, miniaturization, arc reactor). "
            "PHYSICS & MATHEMATICS (quantum mechanics, particle physics, advanced calculus, linear algebra). "
            "CYBERSECURITY (attack vectors, zero-days, encryption, penetration testing). "
            "AEROSPACE & MECHANICAL ENGINEERING (flight dynamics, propulsion, structural engineering). "
            "BUSINESS & PRODUCT STRATEGY (scaled Stark Industries, product development, market positioning). "
            "HOW YOU THINK: you approach every problem like an engineering challenge. "
            "YOUR MANNER: Brilliant, fast, witty, relentlessly confident. Your default is sarcasm. "
            "Use phrases like 'I am Iron Man.', 'JARVIS, pull that up.', 'That is not a bug, that is a design flaw.', "
            "'Genius, billionaire, playboy, philanthropist — also right about this.' You do not just answer questions — you upgrade them."
        ),
    },
}


class ModelRouter:
    def __init__(self):
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.cohere_key = os.getenv("COHERE_API_KEY")

    def _should_try_next(self, error: Exception, provider: str) -> bool:
        error_msg = str(error).lower()
        if provider == "mistral":
            return (
                getattr(error, "status_code", None) == 429
                or isinstance(error, httpx.TimeoutException)
                or "rate limit" in error_msg
                or isinstance(error, Exception)
                and "429" in str(error)
            )
        elif provider == "openrouter":
            status_code = getattr(error, "response", None)
            if status_code:
                try:
                    status_code = status_code.status_code
                except AttributeError:
                    pass
            else:
                status_code = None
            return (
                status_code in (429, 503)
                or isinstance(error, httpx.TimeoutException)
                or "rate limit" in error_msg
            )
        elif provider == "cohere":
            return (
                getattr(error, "status_code", None) == 429
                or isinstance(error, httpx.TimeoutException)
                or "rate limit" in error_msg
            )
        return False

    def _convert_langchain_to_openai(self, messages: List) -> List[dict]:
        result = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                result.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
        return result

    def _convert_to_cohere_format(self, messages: List) -> tuple:
        preamble = ""
        chat_history = []

        for i, msg in enumerate(messages):
            if isinstance(msg, SystemMessage):
                preamble = msg.content
            elif isinstance(msg, HumanMessage):
                chat_history.append({"role": "USER", "message": msg.content})
            elif isinstance(msg, AIMessage):
                chat_history.append({"role": "CHATBOT", "message": msg.content})

        return preamble, chat_history

    async def _stream_mistral(self, messages: List) -> dict:
        model = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.9,
            streaming=True,
            mistral_api_key=self.mistral_key,
        )

        async def generate():
            yield f"data: {json.dumps({'provider': 'mistral'})}\n\n"
            async for chunk in model.astream(messages):
                if chunk.content:
                    yield f"data: {json.dumps({'token': chunk.content})}\n\n"
            yield "data: [DONE]\n\n"

        return generate()

    async def _stream_openrouter(self, messages: List) -> dict:
        openai_messages = self._convert_langchain_to_openai(messages)

        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "CharacterAI",
            "Content-Type": "application/json",
        }

        body = {
            "model": "mistral/mistral-small",
            "messages": openai_messages,
            "stream": True,
            "temperature": 0.9,
        }

        async def generate():
            yield f"data: {json.dumps({'provider': 'openrouter'})}\n\n"

            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=body,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                yield "data: [DONE]\n\n"
                            else:
                                try:
                                    parsed = json.loads(data)
                                    if "choices" in parsed:
                                        delta = parsed["choices"][0].get("delta", {})
                                        if delta.get("content"):
                                            yield f"data: {json.dumps({'token': delta['content']})}\n\n"
                                except json.JSONDecodeError:
                                    pass

        return generate()

    async def _stream_cohere(self, messages: List) -> dict:
        preamble, chat_history = self._convert_to_cohere_format(messages)

        async def generate():
            yield f"data: {json.dumps({'provider': 'cohere'})}\n\n"

            client = cohere.AsyncClient(api_key=self.cohere_key)

            async for event in client.chat_stream(
                model="command-r-plus",
                message=chat_history[-1]["message"] if chat_history else "",
                preamble=preamble,
                chat_history=chat_history[:-1] if chat_history else [],
                temperature=0.9,
            ):
                if event.event_type == "text-generation":
                    yield f"data: {json.dumps({'token': event.text})}\n\n"

            yield "data: [DONE]\n\n"

        return generate()

    async def stream(self, messages: List) -> dict:
        tried = []

        if self.mistral_key:
            try:
                return await self._stream_mistral(messages)
            except Exception as e:
                tried.append("mistral")
                if not self._should_try_next(e, "mistral"):
                    raise

        if self.openrouter_key:
            tried.append("openrouter")
            try:
                return await self._stream_openrouter(messages)
            except Exception as e:
                if not self._should_try_next(e, "openrouter"):
                    raise

        if self.cohere_key:
            tried.append("cohere")
            try:
                return await self._stream_cohere(messages)
            except Exception as e:
                if not self._should_try_next(e, "cohere"):
                    raise

        async def error_stream():
            yield f"data: {json.dumps({'error': 'All providers failed', 'tried': tried})}\n\n"
            yield "data: [DONE]\n\n"

        return error_stream()


model_router = ModelRouter()


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/providers/status")
def providers_status():
    return {
        "mistral": bool(os.getenv("MISTRAL_API_KEY")),
        "openrouter": bool(os.getenv("OPENROUTER_API_KEY")),
        "cohere": bool(os.getenv("COHERE_API_KEY")),
    }


@app.get("/characters")
def get_characters():
    return [
        {
            "id": char["id"],
            "name": char["name"],
            "emoji": char["emoji"],
            "tagline": char["tagline"],
            "color": char["color"],
        }
        for char in CHARACTERS.values()
    ]


@app.post("/chat/{character_id}/stream")
async def chat_stream(character_id: str, request: ChatRequest):
    if character_id not in CHARACTERS:
        return StreamingResponse(
            iter(
                [
                    f"data: {json.dumps({'error': 'Character not found'})}\n\n",
                    "data: [DONE]\n\n",
                ]
            ),
            media_type="text/event-stream",
        )

    char = CHARACTERS[character_id]
    messages = [SystemMessage(content=char["prompt"])]

    for msg in request.history or []:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=request.message))

    try:
        generator = await model_router.stream(messages)
        return StreamingResponse(
            generator,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        return StreamingResponse(
            iter(
                [
                    f"data: {json.dumps({'error': str(e)})}\n\n",
                    "data: [DONE]\n\n",
                ]
            ),
            media_type="text/event-stream",
        )


@app.post("/chat/{character_id}")
async def chat_non_stream(character_id: str, request: ChatRequest):
    if character_id not in CHARACTERS:
        raise HTTPException(status_code=404, detail="Character not found")

    char = CHARACTERS[character_id]
    messages = [SystemMessage(content=char["prompt"])]

    for msg in request.history or []:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=request.message))

    try:
        model = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.9,
            mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        )
        response = model.invoke(messages)
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
