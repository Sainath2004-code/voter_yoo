'use client';

import React from 'react';
import { usePathname } from 'next/navigation';

interface DashboardLayoutProps {
  children: React.ReactNode;
  role: string;
  scope?: string;
}

export default function DashboardLayout({ children, role, scope }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-slate-50 dark:bg-slate-900">
      {/* Sidebar - Dynamically rendered based on role */}
      <aside className="w-64 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 p-6">
        <div className="mb-8">
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">ECI Portal</h1>
          <p className="text-xs text-slate-500 uppercase tracking-wider mt-1">{role.replace('_', ' ')}</p>
          {scope && <p className="text-[10px] text-blue-500 font-medium mt-1">Scope: {scope}</p>}
        </div>
        
        <nav className="space-y-1">
          {/* Common Links */}
          <NavLink href="/dashboard" label="Overview" />
          
          {/* Role Specific Links */}
          {role === 'booth_level_officer' && (
            <>
              <NavLink href="/dashboard/voters" label="Voter List" />
              <NavLink href="/dashboard/verifications" label="Field Tasks" />
            </>
          )}
          
          {role === 'chief_election_commissioner' && (
            <>
              <NavLink href="/admin/elections" label="Election Schedule" />
              <NavLink href="/admin/officers" label="Officer Registry" />
              <NavLink href="/admin/analytics" label="National Insights" />
            </>
          )}
          
          <NavLink href="/dashboard/grievances" label="Grievances" />
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-8">
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-semibold text-slate-800 dark:text-slate-100">
            Election Governance Platform
          </h2>
          <div className="flex items-center gap-4">
             {/* User profile dropdown would go here */}
          </div>
        </header>
        
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

function NavLink({ href, label }: { href: string; label: string }) {
  const pathname = usePathname();
  const isActive = pathname === href;
  
  return (
    <a 
      href={href}
      className={`block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
        isActive 
          ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400' 
          : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800'
      }`}
    >
      {label}
    </a>
  );
}
