import { useState, useEffect, useRef, useCallback } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || '/api'

const FALLBACK_CHARACTERS = [
  { id: 'baymax', name: 'Baymax', emoji: '🏥', tagline: 'Healthcare & Medical', color: '#3B82F6' },
  { id: 'deadpool', name: 'Deadpool', emoji: '🗡️', tagline: 'Pop Culture & Combat', color: '#EF4444' },
  { id: 'goku', name: 'Goku', emoji: '💥', tagline: 'Martial Arts & Training', color: '#F59E0B' },
  { id: 'peter_parker', name: 'Peter Parker', emoji: '🕷️', tagline: 'Science & Engineering', color: '#8B5CF6' },
  { id: 'ryan_gosling', name: 'Ryan Gosling', emoji: '😎', tagline: 'Film, Music & Style', color: '#06B6D4' },
  { id: 'walter_white', name: 'Walter White', emoji: '🧪', tagline: 'Chemistry & Strategy', color: '#10B981' },
  { id: 'saul_goodman', name: 'Saul Goodman', emoji: '⚖️', tagline: 'Law & Persuasion', color: '#F97316' },
  { id: 'tony_stark', name: 'Tony Stark', emoji: '🤖', tagline: 'Tech, AI & Engineering', color: '#EF4444' },
]

function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substring(2, 11)
}

function App() {
  const [characters, setCharacters] = useState([])
  const [selectedCharacter, setSelectedCharacter] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [streamingContent, setStreamingContent] = useState('')
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('characterai_session') || generateSessionId()
  })
  const [abortController, setAbortController] = useState(null)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    localStorage.setItem('characterai_session', sessionId)
  }, [sessionId])

  useEffect(() => {
    fetch(`${API_URL}/characters`)
      .then(res => res.json())
      .then(data => setCharacters(data))
      .catch(() => setCharacters(FALLBACK_CHARACTERS))
  }, [])

  useEffect(() => {
    if (sessionId) {
      fetch(`${API_URL}/sessions/${sessionId}`)
        .then(res => res.json())
        .then(data => {
          if (data && data.messages && data.messages.length > 0) {
            setMessages(data.messages)
            if (data.characterId) {
              const char = characters.find(c => c.id === data.characterId)
              if (char) setSelectedCharacter(char)
            }
          }
        })
        .catch(() => {})
    }
  }, [sessionId, characters.length])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streamingContent])

  const handleSelectCharacter = async (character) => {
    setSelectedCharacter(character)
    setMessages([])
    setStreamingContent('')
    const newSessionId = generateSessionId()
    setSessionId(newSessionId)

    try {
      await fetch(`${API_URL}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: newSessionId,
          characterId: character.id,
        }),
      })
    } catch (err) {
      console.error('Failed to create session:', err)
    }
  }

  const handleSend = async () => {
    if (!input.trim() || !selectedCharacter) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    const currentInput = input
    setInput('')
    setIsLoading(true)
    setStreamingContent('')

    const controller = new AbortController()
    setAbortController(controller)

    const history = messages.map(m => ({ role: m.role, content: m.content }))

    try {
      const response = await fetch(`${API_URL}/chat/${selectedCharacter.id}/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          message: currentInput,
          history,
        }),
        signal: controller.signal,
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullResponse = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') continue

            try {
              const parsed = JSON.parse(data)
              if (parsed.token) {
                fullResponse += parsed.token
                setStreamingContent(fullResponse)
              }
            } catch {}
          }
        }
      }

      if (fullResponse) {
        setMessages(prev => [...prev, { role: 'assistant', content: fullResponse }])
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Chat error:', err)
      }
    } finally {
      setIsLoading(false)
      setStreamingContent('')
      setAbortController(null)
    }
  }

  const handleStop = () => {
    if (abortController) {
      abortController.abort()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>CharacterAI</h1>
      </header>

      {!selectedCharacter ? (
        <div className="character-select">
          <h2>Choose your AI Character</h2>
          <div className="character-grid">
            {characters.map((char, index) => (
              <button
                key={char.id}
                className="character-card"
                style={{
                  '--card-color': char.color,
                  animationDelay: `${index * 60}ms`,
                }}
                onClick={() => handleSelectCharacter(char)}
              >
                <span className="character-emoji">{char.emoji}</span>
                <span className="character-name">{char.name}</span>
                <span className="character-tagline">{char.tagline}</span>
                <span className="chat-label">Chat →</span>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="chat-container" style={{ '--chat-color': selectedCharacter.color }}>
          <div className="chat-header">
            <button className="back-btn" onClick={() => setSelectedCharacter(null)}>
              ← Back
            </button>
            <span className="selected-char">
              <span className="emoji">{selectedCharacter.emoji}</span>
              <span className="info">
                <span className="name">{selectedCharacter.name}</span>
                <span className="tagline">{selectedCharacter.tagline}</span>
              </span>
            </span>
            <span className="status-dot" title="Online" />
          </div>

          <div className="messages">
            {messages.length === 0 && !streamingContent && (
              <div className="empty-state">
                <span className="emoji">{selectedCharacter.emoji}</span>
                <p>Start a conversation with {selectedCharacter.name}</p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}

            {streamingContent && (
              <div className="message assistant streaming">
                <div className="message-content">
                  {streamingContent}
                  <span className="streaming-cursor" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="input-area">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Chat with ${selectedCharacter.name}...`}
              rows={1}
              disabled={isLoading}
            />
            {isLoading ? (
              <button className="stop-btn" onClick={handleStop}>
                Stop
              </button>
            ) : (
              <button onClick={handleSend} disabled={!input.trim()}>
                Send
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
