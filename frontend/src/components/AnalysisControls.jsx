import React from 'react'
import { Play, RefreshCw } from 'lucide-react'

const AnalysisControls = ({ onAnalyze, analyzing, lastRun }) => {
  return (
    <div className="flex items-center space-x-4">
      <div className="text-sm text-gray-600">
        Last run: {lastRun ? new Date(lastRun).toLocaleString() : 'Never'}
      </div>
      <button
        onClick={onAnalyze}
        disabled={analyzing}
        className="btn-primary flex items-center space-x-2 disabled:opacity-50"
      >
        {analyzing ? (
          <>
            <RefreshCw size={16} className="animate-spin" />
            <span>Analyzing...</span>
          </>
        ) : (
          <>
            <Play size={16} />
            <span>Run Analysis</span>
          </>
        )}
      </button>
    </div>
  )
}

export default AnalysisControls
