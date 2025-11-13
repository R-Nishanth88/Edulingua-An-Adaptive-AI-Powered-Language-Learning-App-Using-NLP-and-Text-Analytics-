import { Link } from 'react-router-dom'
import { BookOpen, Brain, MessageSquare, BarChart3 } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden animated-gradient text-white min-h-[600px] flex items-center">
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
          }}
        ></div>
        {/* Floating shapes */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-white/10 rounded-full blur-xl animate-float"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-purple-300/20 rounded-full blur-2xl animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-pink-300/20 rounded-full blur-xl animate-float" style={{ animationDelay: '4s' }}></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32 w-full">
          <div className="text-center">
            <div className="inline-block mb-6 animate-bounce-slow">
              <h1 className="text-6xl sm:text-7xl font-bold mb-4">
                <span className="text-gradient bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-purple-100">
                  🧩 EduLingua Pro
                </span>
              </h1>
            </div>
            <p className="text-2xl sm:text-3xl mb-6 text-white/90 max-w-2xl mx-auto font-semibold">
              Adaptive AI Language Learning Platform
            </p>
            <p className="text-lg sm:text-xl mb-10 text-white/80 max-w-3xl mx-auto">
              Master English writing with intelligent feedback, grammar analysis, vocabulary enhancement, 
              and personalized learning recommendations powered by advanced NLP.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/login"
                className="bg-white text-blue-600 hover:bg-blue-50 font-bold text-lg px-10 py-4 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 transition-all duration-300 hover:-translate-y-1"
              >
                🚀 Start Learning
              </Link>
              <Link
                to="/login"
                className="bg-white/20 hover:bg-white/30 backdrop-blur-lg text-white font-bold text-lg px-10 py-4 rounded-2xl border-2 border-white/30 hover:border-white/50 transition-all duration-300 transform hover:scale-110 hover:-translate-y-1"
              >
                ✨ Sign Up Free
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-b from-white to-gray-50 dark:from-gray-900 dark:to-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl sm:text-5xl font-bold text-center mb-4 text-gray-900 dark:text-white">
            <span className="text-gradient">Powerful Features</span>
          </h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12 text-lg">
            Everything you need to master English writing
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <FeatureCard
              icon={<BookOpen className="w-12 h-12" />}
              title="Grammar Analysis"
              description="Advanced NLP-powered grammar error detection and correction with detailed explanations."
              gradient="from-blue-500 to-cyan-500"
            />
            <FeatureCard
              icon={<Brain className="w-12 h-12" />}
              title="Vocabulary Enhancement"
              description="Lexical diversity analysis, synonym suggestions, and contextual vocabulary recommendations."
              gradient="from-purple-500 to-pink-500"
            />
            <FeatureCard
              icon={<MessageSquare className="w-12 h-12" />}
              title="AI Tutor Chatbot"
              description="Interactive chatbot that explains grammar rules, answers questions, and provides learning tips."
              gradient="from-pink-500 to-red-500"
            />
            <FeatureCard
              icon={<BarChart3 className="w-12 h-12" />}
              title="Progress Analytics"
              description="Visual dashboards tracking your CEFR level, error trends, and learning progress over time."
              gradient="from-green-500 to-emerald-500"
            />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gradient-to-b from-gray-50 to-white dark:from-gray-800 dark:to-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl sm:text-5xl font-bold text-center mb-4 text-gray-900 dark:text-white">
            <span className="text-gradient">How It Works</span>
          </h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12 text-lg">
            Simple steps to improve your English
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StepCard
              number="1"
              title="Write & Submit"
              description="Type or paste your English text into our intelligent analyzer."
              color="from-blue-500 to-cyan-500"
            />
            <StepCard
              number="2"
              title="AI Analysis"
              description="Our NLP engine analyzes grammar, vocabulary, readability, tone, and style."
              color="from-purple-500 to-pink-500"
            />
            <StepCard
              number="3"
              title="Learn & Improve"
              description="Receive detailed feedback, corrections, and personalized recommendations."
              color="from-green-500 to-emerald-500"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 animated-gradient text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl sm:text-5xl font-bold mb-6 animate-pulse-slow">Ready to Improve Your English? 🎯</h2>
          <p className="text-xl sm:text-2xl mb-10 text-white/90 font-medium">
            Join thousands of learners using AI-powered language learning.
          </p>
          <Link
            to="/login"
            className="bg-white text-blue-600 hover:bg-blue-50 font-bold text-xl px-12 py-5 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-110 transition-all duration-300 hover:-translate-y-2 inline-block animate-bounce-slow"
          >
            🚀 Get Started Now
          </Link>
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ icon, title, description, gradient }) {
  return (
    <div className="card hover-lift text-center group cursor-pointer">
      <div className={`flex justify-center mb-4 p-4 rounded-2xl bg-gradient-to-br ${gradient} text-white transform group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-gray-900 dark:text-white group-hover:text-gradient transition-all">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{description}</p>
    </div>
  )
}

function StepCard({ number, title, description, color }) {
  return (
    <div className="text-center hover-lift">
      <div className={`w-20 h-20 bg-gradient-to-br ${color} text-white rounded-2xl flex items-center justify-center text-3xl font-bold mx-auto mb-6 shadow-xl transform hover:rotate-12 transition-transform duration-300`}>
        {number}
      </div>
      <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 leading-relaxed">{description}</p>
    </div>
  )
}
