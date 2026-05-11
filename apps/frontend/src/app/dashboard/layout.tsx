"use client"

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Home, 
  User, 
  Fingerprint, 
  MapPin, 
  Bell, 
  HelpCircle, 
  LogOut,
  Vote,
  Menu
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { cn } from '@/lib/utils'

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'Profile', href: '/dashboard/profile', icon: User },
  { name: 'Biometrics', href: '/dashboard/biometrics', icon: Fingerprint },
  { name: 'Booth Locator', href: '/dashboard/locator', icon: MapPin },
  { name: 'Notifications', href: '/dashboard/notifications', icon: Bell },
]

export default function VoterLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  return (
    <div className="flex h-screen bg-accent/10 overflow-hidden">
      {/* Sidebar - Mobile Responsive */}
      <aside className="hidden lg:flex w-64 bg-background border-r border-border/50 flex-col">
        <div className="p-6 flex items-center gap-2">
          <div className="p-2 bg-primary rounded-lg">
            <Vote className="w-6 h-6 text-primary-foreground" />
          </div>
          <span className="font-bold text-lg tracking-tight">Voter Portal</span>
        </div>

        <nav className="flex-1 px-4 space-y-1 mt-4">
          {navItems.map((item) => (
            <Link key={item.name} href={item.href}>
              <div 
                className={cn(
                  "flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-medium",
                  pathname === item.href 
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:bg-accent hover:text-foreground"
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </div>
            </Link>
          ))}
        </nav>

        <div className="p-6 mt-auto">
          <Card className="bg-primary/5 border-primary/10 p-4 rounded-2xl">
            <p className="text-xs font-bold text-primary mb-2">Need Help?</p>
            <p className="text-[10px] text-muted-foreground leading-relaxed mb-3">
              Contact support for any voting assistance or registration issues.
            </p>
            <Button size="sm" variant="outline" className="w-full text-[10px] h-8">
              Support Center
            </Button>
          </Card>
          <Button variant="ghost" className="w-full justify-start gap-3 mt-4 text-muted-foreground hover:text-red-500 transition-colors">
            <LogOut className="w-5 h-5" />
            Logout
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-20 bg-background/80 backdrop-blur-md border-b border-border/50 flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="lg:hidden">
              <Menu className="w-6 h-6" />
            </Button>
            <div>
              <h2 className="text-lg font-bold">Voter Dashboard</h2>
              <p className="text-xs text-muted-foreground">ID: VTR-9921-X92-2026</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Badge className="bg-green-500/10 text-green-500 border-green-500/20 px-3 py-1">
              Verified
            </Badge>
            <Avatar className="h-10 w-10 border-2 border-primary/20">
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>JD</AvatarFallback>
            </Avatar>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-8 lg:p-12">
          <div className="max-w-6xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
