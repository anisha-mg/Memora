import React from 'react';

const sourceToApp = (source) => {
  const key = String(source || '').toLowerCase();
  if (key.includes('email')) return 'Email';
  if (key.includes('pdf')) return 'PDF Docs';
  if (key.includes('csv')) return 'CSV Data';
  if (key.includes('calendar')) return 'Calendar';
  return 'Unknown Source';
};

const PuppyLoader = () => {
  return (
    <div className="mt-3 rounded-xl bg-slate-50 p-3">
      <p className="text-xs font-medium text-slate-600">Fetching data...</p>
      <div className="puppy-track mt-2">
        <svg
          viewBox="0 0 120 70"
          className="puppy-runner h-10 w-16"
          role="img"
          aria-label="Running puppy clipart"
        >
          <ellipse cx="58" cy="34" rx="26" ry="15" fill="#7c5a3a" />
          <circle cx="87" cy="27" r="11" fill="#8a6441" />
          <circle cx="91" cy="25" r="2" fill="#1f2937" />
          <ellipse cx="95" cy="31" rx="5" ry="3" fill="#5b3f2a" />
          <ellipse cx="82" cy="18" rx="4" ry="7" fill="#6d4b30" />
          <ellipse cx="37" cy="29" rx="5" ry="3" fill="#6d4b30" />
          <rect x="45" y="44" width="6" height="14" rx="3" fill="#6d4b30" />
          <rect x="65" y="44" width="6" height="14" rx="3" fill="#6d4b30" />
          <rect x="78" y="43" width="6" height="14" rx="3" fill="#6d4b30" />
          <rect x="55" y="43" width="6" height="14" rx="3" fill="#6d4b30" />
        </svg>
      </div>
    </div>
  );
};

const DataSourcePanel = ({ isLoading, fetchHistory }) => {
  return (
    <div className="flex h-full flex-col rounded-3xl border border-white/80 bg-white/80 p-4 shadow-xl backdrop-blur">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-blue-900">Data Fetch Tracker</h3>
        <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs text-blue-700">
          {fetchHistory.length} logs
        </span>
      </div>

      <p className="text-xs text-slate-500">
        Shows which app/source was used to answer your latest prompts.
      </p>

      {isLoading && <PuppyLoader />}

      <div className="mt-3 flex-1 space-y-2 overflow-y-auto pr-1">
        {fetchHistory.length === 0 ? (
          <div className="rounded-xl bg-slate-50 p-3 text-xs text-slate-500">
            No fetch activity yet. Ask a question to see source mapping.
          </div>
        ) : (
          fetchHistory.map((item) => (
            <div key={item.id} className="rounded-xl border border-slate-200 bg-white p-3">
              <p className="text-xs font-semibold text-slate-800">{item.query}</p>
              <p className="mt-1 text-[11px] text-slate-500">{new Date(item.timestamp).toLocaleTimeString()}</p>
              {item.error ? (
                <p className="mt-2 text-xs text-rose-600">Fetch failed</p>
              ) : (
                <div className="mt-2 flex flex-wrap gap-2">
                  {item.sources.length > 0 ? (
                    item.sources.map((src, idx) => (
                      <span
                        key={`${item.id}-${src}-${idx}`}
                        className="rounded-full border border-blue-200 bg-blue-50 px-2 py-1 text-[11px] text-blue-800"
                      >
                        {src} -> {sourceToApp(src)}
                      </span>
                    ))
                  ) : (
                    <span className="rounded-full border border-slate-200 bg-slate-50 px-2 py-1 text-[11px] text-slate-600">
                      No source tags returned
                    </span>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default DataSourcePanel;