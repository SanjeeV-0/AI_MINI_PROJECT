import ChatBox from './components/ChatBox';
import DataViewer from './components/DataViewer';

function App() {
  return (
    <div className="min-h-screen bg-[var(--bg-base)] flex flex-col relative overflow-x-hidden">
      {/* Background ambient light effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-[100px] pointer-events-none -translate-y-1/2"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none translate-y-1/2"></div>

      {/* Navigation Bar */}
      <nav className="glass sticky top-0 z-10 border-b border-border/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center shadow-lg shadow-primary/20">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            <h1 className="text-xl font-medium tracking-tight text-text-main">
              Meet<span className="font-light text-primary">Summariser</span>
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Optional upload button for future use */}
            <button className="text-sm font-medium text-text-muted hover:text-text-main transition-colors px-3 py-1.5 rounded-md hover:bg-surface border border-transparent hover:border-border">
              Upload Transcript
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-[calc(100vh-8rem)] min-h-[600px]">
          
          {/* Left Pane - Chat RAG Interface */}
          <div className="lg:col-span-5 h-full">
            <ChatBox />
          </div>

          {/* Right Pane - Data Viewer */}
          <div className="lg:col-span-7 h-full">
            <DataViewer />
          </div>

        </div>
      </main>
    </div>
  );
}

export default App;
