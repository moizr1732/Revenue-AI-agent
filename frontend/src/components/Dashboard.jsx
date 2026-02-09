import React, { useState, useEffect } from 'react'
import apiClient from '../api'
import DealCard from './DealCard'
import Metrics from './Metrics'
import AnalysisControls from './AnalysisControls'
import RiskChart from './RiskChart'

const Dashboard = () => {
  const [deals, setDeals] = useState([])
  const [metrics, setMetrics] = useState({
    totalDeals: 0,
    riskyDeals: 0,
    averageScore: 0,
    lastAnalysis: null
  })
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [dealsResponse, statusResponse] = await Promise.all([
        apiClient.get('/api/deals'),
        apiClient.get('/api/status')
      ])
      
      setDeals(dealsResponse.data.deals || [])
      
      // Calculate metrics
      const riskyCount = dealsResponse.data.deals?.filter(d => d.risk_score < 60).length || 0
      const avgScore = dealsResponse.data.deals?.length 
        ? dealsResponse.data.deals.reduce((sum, d) => sum + d.risk_score, 0) / dealsResponse.data.deals.length 
        : 0
      
      setMetrics({
        totalDeals: dealsResponse.data.deals?.length || 0,
        riskyDeals: riskyCount,
        averageScore: Math.round(avgScore),
        lastAnalysis: statusResponse.data.last_analysis
      })
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const triggerAnalysis = async () => {
    try {
      setAnalyzing(true)
      await apiClient.post('/api/analyze')
      
      // Wait a bit for analysis to complete, then refresh
      setTimeout(fetchDashboardData, 5000)
    } catch (error) {
      console.error('Error triggering analysis:', error)
    } finally {
      setAnalyzing(false)
    }
  }

  useEffect(() => {
    fetchDashboardData()
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Deal Risk Dashboard</h1>
          <p className="text-gray-600">AI-powered risk assessment for your sales pipeline</p>
        </div>
        <AnalysisControls 
          onAnalyze={triggerAnalysis} 
          analyzing={analyzing}
          lastRun={metrics.lastAnalysis}
        />
      </div>

      <Metrics data={metrics} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Recent Deal Analysis ({deals.length})
          </h2>
          <div className="space-y-4">
            {deals.map((deal) => (
              <DealCard key={deal.deal_id} deal={deal} />
            ))}
            
            {deals.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No deals analyzed yet. Run your first analysis to see results.
              </div>
            )}
          </div>
        </div>
        
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h2>
          <RiskChart deals={deals} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
