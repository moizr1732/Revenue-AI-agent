import React from 'react'
import { TrendingUp, AlertTriangle, Clock, Database } from 'lucide-react'

const Metrics = ({ data }) => {
  const cards = [
    {
      icon: Database,
      label: 'Total Deals',
      value: data.totalDeals,
      color: 'blue'
    },
    {
      icon: AlertTriangle,
      label: 'Risky Deals',
      value: data.riskyDeals,
      color: data.riskyDeals > 0 ? 'red' : 'green'
    },
    {
      icon: TrendingUp,
      label: 'Avg Risk Score',
      value: `${data.averageScore}/100`,
      color: data.averageScore > 70 ? 'green' : data.averageScore > 40 ? 'yellow' : 'red'
    },
    {
      icon: Clock,
      label: 'Last Analysis',
      value: data.lastAnalysis ? new Date(data.lastAnalysis).toLocaleTimeString() : 'Never',
      color: 'gray'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card) => {
        const Icon = card.icon
        const colorClasses = {
          blue: 'bg-blue-50 text-blue-600',
          red: 'bg-red-50 text-red-600',
          green: 'bg-green-50 text-green-600',
          yellow: 'bg-yellow-50 text-yellow-600',
          gray: 'bg-gray-50 text-gray-600'
        }

        return (
          <div key={card.label} className="card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{card.value}</p>
              </div>
              <div className={`p-3 rounded-full ${colorClasses[card.color]}`}>
                <Icon size={24} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default Metrics
