import React from 'react';
import ChatBox from '../components/ChatBox';

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#dfe8ff] via-[#eef5ff] to-[#f4ecff] px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto grid min-h-[88vh] max-w-7xl grid-cols-1 items-center gap-10 lg:grid-cols-2">
        <section className="relative">
          <div className="absolute -left-10 top-0 h-56 w-56 rounded-full bg-cyan-200/40 blur-3xl" />
          <div className="absolute left-40 top-40 h-44 w-44 rounded-full bg-blue-300/30 blur-3xl" />

          <h1 className="relative z-10 text-4xl font-bold tracking-tight text-blue-900 sm:text-5xl">
            Memora
          </h1>
          <p className="relative z-10 mt-3 max-w-md text-blue-800/80">
            Planning, building, and monitoring with a context-aware assistant.
          </p>

          <div className="relative z-10 mt-8 flex max-w-sm flex-wrap gap-3">
            {['Planning', 'Building', 'Monitoring'].map((item) => (
              <span
                key={item}
                className="rounded-full border border-blue-200 bg-white/80 px-5 py-2 text-lg font-semibold italic text-blue-700 shadow-sm"
              >
                {item}
              </span>
            ))}
          </div>

          <div className="relative mt-10 flex h-80 w-full max-w-md items-center justify-center">
            <div className="absolute h-64 w-64 rounded-full bg-gradient-to-br from-blue-100 to-cyan-100 blur-md" />
            <div className="relative">
              <div className="mx-auto flex h-36 w-44 items-center justify-center rounded-[38px] bg-gradient-to-b from-white to-blue-100 shadow-xl">
                <div className="relative h-24 w-32 rounded-3xl bg-gradient-to-b from-blue-700 to-blue-500">
                  <div className="absolute left-7 top-8 h-3 w-3 rounded-full bg-white" />
                  <div className="absolute right-7 top-8 h-3 w-3 rounded-full bg-white" />
                  <div className="absolute left-1/2 top-14 h-1.5 w-10 -translate-x-1/2 rounded-full bg-cyan-200" />
                </div>
              </div>
              <div className="mx-auto mt-2 h-36 w-48 rounded-[42px] bg-gradient-to-b from-white to-blue-200 shadow-xl" />
              <div className="absolute -left-8 top-20 h-20 w-8 rounded-full bg-gradient-to-b from-blue-600 to-blue-400" />
              <div className="absolute -right-8 top-20 h-20 w-8 rounded-full bg-gradient-to-b from-blue-600 to-blue-400" />
            </div>
          </div>

          <div className="mt-6 text-sm text-blue-900/70">Live status: Connected</div>
        </section>

        <section className="mx-auto h-[78vh] w-full max-w-md lg:max-w-lg">
          <div className="h-full rounded-[28px] border border-white/80 bg-white/70 p-2 shadow-2xl backdrop-blur">
            <ChatBox />
          </div>
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
