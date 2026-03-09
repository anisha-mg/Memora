import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-400 flex items-center justify-center px-4">
      <div className="max-w-6xl w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* Left Section - Text */}
        <div className="text-white">
          <h1 className="text-5xl lg:text-6xl font-bold mb-6 tracking-tight">
            Memora
          </h1>
          <p className="text-lg lg:text-xl text-blue-50 leading-relaxed mb-8 opacity-90">
            Experience the power of intelligent conversation. Memora uses advanced memory layers and context awareness to deliver personalized, meaningful interactions. Search across your emails, PDFs, calendar events, and more—all powered by cutting-edge natural language processing.
          </p>
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-white text-blue-600 font-semibold px-8 py-3 rounded-lg hover:bg-blue-50 transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            Get started
          </button>
        </div>

        {/* Right Section - Illustration */}
        <div className="flex justify-center items-center">
          <div className="relative w-80 h-96">
            {/* Background Phone Shape */}
            <div className="absolute inset-0 bg-white rounded-3xl shadow-2xl transform perspective"></div>

            {/* Chat Bubbles */}
            <div className="absolute top-16 right-12 bg-blue-200 rounded-2xl px-4 py-2 w-20 h-12 flex items-center justify-center opacity-70">
              <div className="flex gap-1.5">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>

            {/* Another Chat Bubble */}
            <div className="absolute top-40 left-8 bg-blue-200 rounded-2xl px-4 py-2 w-24 h-12 opacity-60"></div>

            {/* Robot/Bot Icon - Center */}
            <div className="absolute inset-0 flex items-center justify-center">
              {/* Simple bot illustration */}
              <div className="relative">
                {/* Head */}
                <div className="w-20 h-20 bg-gradient-to-br from-gray-300 to-gray-400 rounded-lg mx-auto mb-2 relative shadow-lg">
                  {/* Eyes */}
                  <div className="absolute top-6 left-4 flex gap-4">
                    <div className="w-3 h-3 bg-gray-700 rounded-full"></div>
                    <div className="w-3 h-3 bg-gray-700 rounded-full"></div>
                  </div>
                  {/* Mouth */}
                  <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 w-8 h-1 bg-gray-700 rounded-full"></div>
                </div>
                {/* Body */}
                <div className="w-16 h-12 bg-gradient-to-b from-gray-400 to-gray-500 rounded-lg mx-auto shadow-lg"></div>
              </div>
            </div>

            {/* Lightbulb Icon - Top right */}
            <div className="absolute -top-4 -right-4 bg-yellow-300 rounded-full p-3 shadow-lg animate-pulse">
              <svg className="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM15.657 14.243a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM11 17a1 1 0 102 0v-1a1 1 0 10-2 0v1zM4.343 14.243a1 1 0 001.414-1.414l-.707-.707a1 1 0 10-1.414 1.414l.707.707zM2 10a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM4.343 5.757a1 1 0 001.414 1.414l.707-.707a1 1 0 10-1.414-1.414l-.707.707z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
