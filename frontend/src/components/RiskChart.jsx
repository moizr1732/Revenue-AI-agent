import React from 'react'

const RiskChart = ({ deals }) => {
  const riskRanges = {
    high: deals.filter(d => d.risk_score < 40).length,
    medium: deals.filter(d => d.risk_score >= 40 && d.risk_score < 70).length,
    low: deals.filter(d => d.risk_score >= 70).length
  }

  const total = deals.length
  const percentages = {
    high: total ? (riskRanges.high / total) * 100 : 0,
    medium: total ? (riskRanges.medium / total) * 100 : 0,
    low: total ? (riskRanges.low / total) * 100 : 0
  }

  return (
    <div className="card p-6">
      <div className="space-y-4">
        <div className="h-4 bg-gray-200 rounded-full overflow-hidden flex">
          <div 
            className="h-full bg-red-500" 
            style={{ width: `${percentages.high}%` }}
          />
          <div 
            className="h-full bg-yellow-500" 
            style={{ width: `${percentages.medium}%` }}
          />
          <div 
            className="h-full bg-green-500" 
            style={{ width: `${percentages.low}%` }}
          />
        </div>
        
        <div className="grid grid-cols-3 gap-4 text-xs">
          <div className="text-center">
            <div className="font-semibold text-red-600">High Risk</div>
            <div>{riskRanges.high} deals</div>
            <div className="text-gray-500">{percentages.high.toFixed(1)}%</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-yellow-600">Medium Risk</div>
            <div>{riskRanges.medium} deals</div>
            <div className="text-gray-500">{percentages.medium.toFixed(1)}%</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-green-600">Low Risk</div>
            <div>{riskRanges.low} deals</div>
            <div className="text-gray-500">{percentages.low.toFixed(1)}%</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RiskChart
