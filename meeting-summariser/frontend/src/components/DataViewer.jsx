import { useState, useEffect } from 'react';

export default function DataViewer() {
  const [activeTab, setActiveTab] = useState('summary');
  const [data, setData] = useState({
    summary: null,
    actionItems: null,
    decisions: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData(activeTab);
  }, [activeTab]);

  const fetchData = async (tab) => {
    if (data[tab]) return; // Already fetched
    setLoading(true);
    setError(null);
    
    try {
      let endpoint = '';
      if (tab === 'summary') endpoint = '/api/summary';
      if (tab === 'actionItems') endpoint = '/api/action-items';
      if (tab === 'decisions') endpoint = '/api/decisions';

      const response = await fetch(endpoint);
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const result = await response.json();
      
      if (result.error) {
        setError(result.error);
      } else {
        setData(prev => ({
          ...prev,
          [tab]: tab === 'actionItems' ? result.action_items : result[tab === 'actionItems' ? 'action_items' : tab]
        }));
      }
    } catch (err) {
      setError('Could not connect to server or no data available yet.');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'summary', label: 'Summary' },
    { id: 'actionItems', label: 'Action Items' },
    { id: 'decisions', label: 'Decisions' },
  ];

  return (
    <div className="flex flex-col h-full glass rounded-xl overflow-hidden shadow-2xl shadow-black/50 border border-border">
      <div className="flex border-b border-border bg-surface/50 shrink-0">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-3 text-sm font-medium tracking-wide transition-all ${
              activeTab === tab.id
                ? 'text-primary border-b-2 border-primary bg-primary/5'
                : 'text-text-muted hover:text-text-main hover:bg-surface'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      
      <div className="flex-1 overflow-y-auto p-6 min-h-0">
        {loading ? (
          <div className="h-full flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-primary rounded-full animate-ping"></div>
            <div className="w-2 h-2 bg-primary/70 rounded-full animate-ping" style={{animationDelay: '150ms'}}></div>
            <div className="w-2 h-2 bg-primary/40 rounded-full animate-ping" style={{animationDelay: '300ms'}}></div>
          </div>
        ) : error ? (
          <div className="h-full flex flex-col items-center justify-center text-red-400/80 space-y-4">
            <svg className="w-10 h-10 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <p className="text-sm font-mono tracking-tight">{error}</p>
          </div>
        ) : (
          <div className="text-text-main text-sm leading-relaxed prose prose-invert max-w-none">
            {activeTab === 'summary' && data.summary && (
              <div className="whitespace-pre-wrap">{data.summary}</div>
            )}
            
            {activeTab === 'actionItems' && (
              data.actionItems && data.actionItems.length > 0 ? (
                <ul className="space-y-3 list-none p-0 m-0">
                  {data.actionItems.map((item, i) => (
                    <li key={i} className="flex gap-3 items-start bg-surface/40 p-4 rounded-lg border border-border/50 hover:border-primary/30 transition-colors">
                      <div className="mt-0.5 text-primary">
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <span className="flex-1 opacity-90">{item}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-text-muted italic text-center mt-10">No action items extracted.</p>
              )
            )}
            
            {activeTab === 'decisions' && data.decisions && (
              <div className="whitespace-pre-wrap bg-surface/30 p-5 rounded-lg border border-border/30">
                {data.decisions}
              </div>
            )}
            
            {!data[activeTab] && !loading && !error && (
               <p className="text-text-muted italic text-center mt-10">Select a meeting to view its {activeTab}.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
