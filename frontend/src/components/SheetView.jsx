import React, { useState } from 'react'
import apiClient from '../api'

const SheetView = () => {
  const [sheetId, setSheetId] = useState('1IradqvjgkrRNkdYa13qUsLgPzNq0YCCUjDV3mwGgvZg')
  const [rows, setRows] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchSheet = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await apiClient.get(`/api/sheets/read?sheet_id=${sheetId}`)
      setRows(res.data.rows)
    } catch (e) {
      setError(e.response?.data?.error || e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <input
          value={sheetId}
          onChange={(e) => setSheetId(e.target.value)}
          className="px-3 py-2 border rounded-lg w-96"
        />
        <button onClick={fetchSheet} className="btn-primary">Fetch Sheet</button>
      </div>

      {loading && <div>Loading...</div>}
      {error && <div className="text-red-600">{error}</div>}

      {rows && (
        <div className="overflow-auto border rounded-lg p-4 bg-white">
          <table className="min-w-full text-sm">
            <tbody>
              {rows.map((r, i) => (
                <tr key={i} className={i===0? 'font-semibold' : ''}>
                  {r.map((c, j) => (
                    <td key={j} className="px-3 py-1 border-b">{c}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default SheetView
