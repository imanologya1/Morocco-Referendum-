import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Vote, Plus, CheckCircle, BarChart3, Shield, Lock, Globe } from 'lucide-react'
import './App.css'

const API_BASE = '/api'

function App() {
  const [activeTab, setActiveTab] = useState('vote')
  const [polls, setPolls] = useState([])
  const [selectedPoll, setSelectedPoll] = useState(null)
  const [voterIdentifier, setVoterIdentifier] = useState('')
  const [receipt, setReceipt] = useState('')
  const [blockchainStats, setBlockchainStats] = useState(null)

  // Create poll form
  const [newPoll, setNewPoll] = useState({
    title: '',
    question: '',
    options: ['', ''],
    duration_hours: 24,
    language: 'ar'
  })

  useEffect(() => {
    fetchPolls()
    fetchBlockchainStats()
  }, [])

  const fetchPolls = async () => {
    try {
      const response = await fetch(`${API_BASE}/polls?active=true`)
      const data = await response.json()
      if (data.success) {
        setPolls(data.polls)
      }
    } catch (error) {
      console.error('Error fetching polls:', error)
    }
  }

  const fetchBlockchainStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/blockchain/stats`)
      const data = await response.json()
      if (data.success) {
        setBlockchainStats(data.stats)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const createPoll = async () => {
    try {
      const response = await fetch(`${API_BASE}/polls`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPoll)
      })
      const data = await response.json()
      if (data.success) {
        alert(`Poll created successfully! Share this link: ${window.location.origin}${data.poll_url}`)
        setNewPoll({ title: '', question: '', options: ['', ''], duration_hours: 24, language: 'ar' })
        fetchPolls()
      } else {
        alert(`Error: ${data.error}`)
      }
    } catch (error) {
      alert(`Error creating poll: ${error.message}`)
    }
  }

  const submitVote = async (pollId, choice) => {
    if (!voterIdentifier) {
      alert('Please enter your email or phone number')
      return
    }

    try {
      const response = await fetch(`${API_BASE}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          poll_id: pollId,
          voter_identifier: voterIdentifier,
          vote_choice: choice
        })
      })
      const data = await response.json()
      if (data.success) {
        setReceipt(data.receipt)
        alert('Vote submitted successfully! Save your receipt for verification.')
        fetchPolls()
      } else {
        alert(`Error: ${data.error}`)
      }
    } catch (error) {
      alert(`Error submitting vote: ${error.message}`)
    }
  }

  const addOption = () => {
    if (newPoll.options.length < 10) {
      setNewPoll({ ...newPoll, options: [...newPoll.options, ''] })
    }
  }

  const updateOption = (index, value) => {
    const options = [...newPoll.options]
    options[index] = value
    setNewPoll({ ...newPoll, options })
  }

  const removeOption = (index) => {
    if (newPoll.options.length > 2) {
      const options = newPoll.options.filter((_, i) => i !== index)
      setNewPoll({ ...newPoll, options })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-red-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-green-600 to-red-600 rounded-lg">
                <Vote className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-red-600 bg-clip-text text-transparent">
                  VoteChain Morocco
                </h1>
                <p className="text-sm text-muted-foreground">Secure Blockchain Voting</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Badge variant="outline" className="gap-1">
                <Shield className="w-3 h-3" />
                Encrypted
              </Badge>
              <Badge variant="outline" className="gap-1">
                <Lock className="w-3 h-3" />
                Anonymous
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        {blockchainStats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Total Polls</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{blockchainStats.total_polls}</div>
              </CardContent>
            </Card>
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Total Votes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{blockchainStats.total_votes}</div>
              </CardContent>
            </Card>
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Blockchain Blocks</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{blockchainStats.total_blocks}</div>
              </CardContent>
            </Card>
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Chain Status</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <CheckCircle className={`w-6 h-6 ${blockchainStats.is_valid ? 'text-green-600' : 'text-red-600'}`} />
                  <span className="text-lg font-semibold">{blockchainStats.is_valid ? 'Valid' : 'Invalid'}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="vote" className="gap-2">
              <Vote className="w-4 h-4" />
              Vote on Polls
            </TabsTrigger>
            <TabsTrigger value="create" className="gap-2">
              <Plus className="w-4 h-4" />
              Create Poll
            </TabsTrigger>
          </TabsList>

          {/* Vote Tab */}
          <TabsContent value="vote" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Your Voter ID</CardTitle>
                <CardDescription>Enter your email or phone number (used for anonymous authentication)</CardDescription>
              </CardHeader>
              <CardContent>
                <Input
                  type="text"
                  placeholder="email@example.com or +212..."
                  value={voterIdentifier}
                  onChange={(e) => setVoterIdentifier(e.target.value)}
                  className="max-w-md"
                />
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {polls.map((poll) => (
                <Card key={poll.poll_id} className="hover:shadow-xl transition-all hover:-translate-y-1">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-xl mb-2">{poll.title}</CardTitle>
                        <CardDescription className="text-base">{poll.question}</CardDescription>
                      </div>
                      <Badge variant="secondary" className="gap-1">
                        <Globe className="w-3 h-3" />
                        {poll.language.toUpperCase()}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {poll.options.map((option, idx) => (
                      <Button
                        key={idx}
                        variant="outline"
                        className="w-full justify-start text-left h-auto py-3 hover:bg-primary hover:text-primary-foreground transition-colors"
                        onClick={() => submitVote(poll.poll_id, option)}
                      >
                        <CheckCircle className="w-4 h-4 mr-2 flex-shrink-0" />
                        <span className="flex-1">{option}</span>
                      </Button>
                    ))}
                  </CardContent>
                  <CardFooter className="flex justify-between text-sm text-muted-foreground">
                    <span>Votes: {poll.vote_count || 0}</span>
                    <span>Closes: {new Date(poll.closes_at * 1000).toLocaleDateString()}</span>
                  </CardFooter>
                </Card>
              ))}
            </div>

            {polls.length === 0 && (
              <Card className="text-center py-12">
                <CardContent>
                  <BarChart3 className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-lg text-muted-foreground">No active polls available</p>
                  <p className="text-sm text-muted-foreground mt-2">Create a new poll to get started!</p>
                </CardContent>
              </Card>
            )}

            {receipt && (
              <Card className="border-green-500 bg-green-50 dark:bg-green-950">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-green-700 dark:text-green-400">
                    <CheckCircle className="w-5 h-5" />
                    Vote Receipt
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm mb-2 text-green-800 dark:text-green-300">Save this receipt to verify your vote on the blockchain:</p>
                  <code className="block p-3 bg-white dark:bg-gray-900 rounded border text-xs break-all">
                    {receipt}
                  </code>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Create Poll Tab */}
          <TabsContent value="create">
            <Card className="max-w-2xl mx-auto">
              <CardHeader>
                <CardTitle>Create New Poll</CardTitle>
                <CardDescription>Create a secure, blockchain-based poll or referendum</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="title">Poll Title</Label>
                  <Input
                    id="title"
                    placeholder="e.g., Constitutional Referendum 2025"
                    value={newPoll.title}
                    onChange={(e) => setNewPoll({ ...newPoll, title: e.target.value })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="question">Question</Label>
                  <Input
                    id="question"
                    placeholder="e.g., Do you approve the proposed amendments?"
                    value={newPoll.question}
                    onChange={(e) => setNewPoll({ ...newPoll, question: e.target.value })}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Options (2-10)</Label>
                  {newPoll.options.map((option, idx) => (
                    <div key={idx} className="flex gap-2">
                      <Input
                        placeholder={`Option ${idx + 1}`}
                        value={option}
                        onChange={(e) => updateOption(idx, e.target.value)}
                      />
                      {newPoll.options.length > 2 && (
                        <Button variant="outline" size="icon" onClick={() => removeOption(idx)}>
                          ×
                        </Button>
                      )}
                    </div>
                  ))}
                  {newPoll.options.length < 10 && (
                    <Button variant="outline" onClick={addOption} className="w-full">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Option
                    </Button>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="duration">Duration (hours)</Label>
                    <Input
                      id="duration"
                      type="number"
                      min="1"
                      max="720"
                      value={newPoll.duration_hours}
                      onChange={(e) => setNewPoll({ ...newPoll, duration_hours: parseInt(e.target.value) })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="language">Language</Label>
                    <select
                      id="language"
                      className="w-full h-10 px-3 rounded-md border border-input bg-background"
                      value={newPoll.language}
                      onChange={(e) => setNewPoll({ ...newPoll, language: e.target.value })}
                    >
                      <option value="ar">العربية (Arabic)</option>
                      <option value="fr">Français (French)</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={createPoll} className="w-full" size="lg">
                  <Plus className="w-4 h-4 mr-2" />
                  Create Poll
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t mt-16 py-8 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <div className="flex items-center justify-center gap-6 mb-4">
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4" />
              <span>RSA + AES Encryption</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4" />
              <span>Anonymous Voting</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4" />
              <span>Blockchain Verified</span>
            </div>
          </div>
          <p>VoteChain Morocco - Free & Secure Blockchain Voting System</p>
          <p className="mt-2 text-xs">Built with cryptographic security for transparent democratic processes</p>
        </div>
      </footer>
    </div>
  )
}

export default App
