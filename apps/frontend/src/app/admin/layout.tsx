"use client"

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  LayoutDashboard, 
  Users, 
  Vote, 
  ShieldAlert, 
  FileText, 
  Settings, 
  LogOut,
  Bell,
  Search,
  Menu,
  ChevronLeft
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { cn } from '@/lib/utils'

const navItems = [
  { name: 'Dashboard', href: '/admin/dashboard', icon: LayoutDashboard },
  { name: 'Voter Registry', href: '/admin/voters', icon: Users },
  { name: 'Elections', href: '/admin/elections', icon: Vote },
  { name: 'Fraud Monitoring', href: '/admin/fraud', icon: ShieldAlert },
  { name: 'Reports', href: '/admin/reports', icon: FileText },
  { name: 'System Settings', href: '/admin/settings', icon: Settings },
]

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = React.useState(false)

  return (
    <div className="flex h-screen bg-accent/20 overflow-hidden">
      {/* Sidebar */}
      <aside 
        className={cn(
          "bg-background border-r border-border/50 transition-all duration-300 flex flex-col relative",
          collapsed ? "w-20" : "w-64"
        )}
      >
        <div className="p-6 flex items-center gap-3">
          <div className="p-2 bg-primary rounded-lg shrink-0">
            <Vote className="w-6 h-6 text-primary-foreground" />
          </div>
          {!collapsed && (
            <span className="font-bold text-lg tracking-tight truncate">Election Admin</span>
          )}
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          {navItems.map((item) => (
            <Link key={item.name} href={item.href}>
              <div 
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all group",
                  pathname === item.href 
                    ? "bg-primary text-primary-foreground shadow-lg shadow-primary/20" 
                    : "text-muted-foreground hover:bg-accent hover:text-foreground"
                )}
              >
                <item.icon className="w-5 h-5 shrink-0" />
                {!collapsed && <span className="text-sm font-medium">{item.name}</span>}
              </div>
            </Link>
          ))}
        </nav>

        <div className="p-4 border-t border-border/50">
          <Button variant="ghost" className="w-full justify-start gap-3 rounded-xl text-red-500 hover:text-red-600 hover:bg-red-500/10">
            <LogOut className="w-5 h-5" />
            {!collapsed && <span className="text-sm font-medium">Logout</span>}
          </Button>
        </div>

        <Button 
          variant="secondary" 
          size="icon" 
          className="absolute -right-3 top-20 h-6 w-6 rounded-full border border-border shadow-md"
          onClick={() => setCollapsed(!collapsed)}
        >
          <ChevronLeft className={cn("w-4 h-4 transition-transform", collapsed && "rotate-180")} />
        </Button>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-background border-b border-border/50 flex items-center justify-between px-8 shrink-0">
          <div className="flex items-center gap-4 w-96">
            <div className="relative w-full">
              <Search className="absolute left-3 top-2.5 w-4 h-4 text-muted-foreground" />
              <Input placeholder="Search voters, elections, or logs..." className="pl-10 bg-accent/30 border-none rounded-xl" />
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-background" />
            </Button>
            <div className="flex items-center gap-3 pl-4 border-l border-border/50">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-bold">Admin User</p>
                <p className="text-[10px] text-muted-foreground uppercase font-bold">Super Admin</p>
              </div>
              <Avatar>
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>AD</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </header>

        {/* Scrollable Area */}
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
