import React from 'react'
import { BarChart3, Zap, Settings, Users } from 'lucide-react'

const Sidebar = () => {
  const menuItems = [
    { icon: BarChart3, label: 'Dashboard', active: true },
    { icon: Users, label: 'Deals', active: false },
    { icon: Users, label: 'Sheets', active: false },
    { icon: Zap, label: 'Automation', active: false },
    { icon: Settings, label: 'Settings', active: false },
  ]

  return (
    <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
      <div className="p-6">
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.label}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  item.active
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            )
          })}
        </nav>
      </div>
    </aside>
  )
}

export default Sidebar
