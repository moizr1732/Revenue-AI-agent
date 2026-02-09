import React from 'react'
import { Mail, Calendar, AlertCircle } from 'lucide-react'

const DealCard = ({ deal }) => {
  const getRiskLevel = (score) => {
    if (score < 40) return { level: 'High', class: 'risk-high', icon: AlertCircle }
    if (score < 70) return { level: 'Medium', class: 'risk-medium', icon: AlertCircle }
    return { level: 'Low', class: 'risk-low', icon: Calendar }
  }

  const riskInfo = getRiskLevel(deal.risk_score)
  const RiskIcon = riskInfo.icon

  return (
    <div className={`card p-4 ${riskInfo.class}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <RiskIcon size={16} />
            <h3 className="font-semibold text-gray-900">{deal.deal_name}</h3>
            <span className="px-2 py-1 text-xs font-medium bg-white rounded-full">
              {deal.stage}
            </span>
          </div>
          
          <p className="text-sm text-gray-600 mb-2">{deal.risk_reason}</p>
          
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <div className="flex items-center space-x-1">
              <Mail size={12} />
              <span>Score: {deal.risk_score}/100</span>
            </div>
            <div className="flex items-center space-x-1">
              <Calendar size={12} />
              <span>{new Date(deal.timestamp).toLocaleString()}</span>
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            riskInfo.level === 'High' ? 'bg-red-100 text-red-800' :
            riskInfo.level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
            'bg-green-100 text-green-800'
          }`}>
            {riskInfo.level} Risk
          </div>
        </div>
      </div>
    </div>
  )
}

export default DealCard
