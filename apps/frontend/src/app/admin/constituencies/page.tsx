"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  MapPin, 
  Users, 
  Search, 
  Filter, 
  Download,
  Building2,
  TrendingUp,
  AlertCircle
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts'

const constituencyData = [
  { name: 'Pune Central', voters: 450000, turnout: 68, booths: 420 },
  { name: 'Mumbai South', voters: 820000, turnout: 52, booths: 780 },
  { name: 'Nagpur East', voters: 390000, turnout: 71, booths: 310 },
  { name: 'Nashik West', voters: 280000, turnout: 64, booths: 250 },
  { name: 'Thane North', voters: 610000, turnout: 58, booths: 520 },
]

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#f59e0b'];

const ConstituencyAnalytics = () => {
  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black tracking-tight uppercase">Constituency Analytics</h1>
          <p className="text-muted-foreground italic">Deep-dive into regional voter demographics and turnout trends.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" className="rounded-xl border-2">
             <Download className="w-4 h-4 mr-2" /> Export Dataset
          </Button>
          <Button className="rounded-xl shadow-lg shadow-primary/20 bg-primary font-bold">
             Live Turnout Map
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <Card className="lg:col-span-1 border-border/50 bg-background/50">
          <CardHeader>
             <CardTitle className="text-sm uppercase tracking-widest text-muted-foreground">Search Jurisdiction</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
             <div className="relative">
                <Search className="absolute left-3 top-2.5 w-4 h-4 text-muted-foreground" />
                <Input placeholder="Search LS / VS ID..." className="pl-10 rounded-xl" />
             </div>
             <div className="space-y-2">
                <p className="text-xs font-bold text-muted-foreground uppercase">Popular Searches</p>
                <div className="flex flex-wrap gap-2">
                   <Badge variant="secondary" className="cursor-pointer hover:bg-primary/10">Delhi LS-7</Badge>
                   <Badge variant="secondary" className="cursor-pointer hover:bg-primary/10">Pune VS-21</Badge>
                   <Badge variant="secondary" className="cursor-pointer hover:bg-primary/10">Lucknow LS-2</Badge>
                </div>
             </div>
             <hr className="border-border/50" />
             <div className="p-4 bg-primary/5 rounded-xl border border-primary/10">
                <div className="flex items-center gap-2 text-primary mb-2">
                   <AlertCircle className="w-4 h-4" />
                   <span className="text-xs font-bold uppercase">Delimitation Note</span>
                </div>
                <p className="text-[10px] text-muted-foreground leading-relaxed">
                   Boundary maps are based on the 2026 Delimitation Commission guidelines.
                </p>
             </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-3 border-border/50 bg-background/50">
          <CardHeader className="flex flex-row items-center justify-between">
             <div>
                <CardTitle>Voter Population Distribution</CardTitle>
                <CardDescription>Comparison of electorate size across selected constituencies.</CardDescription>
             </div>
             <BarChart3 className="w-5 h-5 text-primary" />
          </CardHeader>
          <CardContent className="h-[400px]">
             <ResponsiveContainer width="100%" height="100%">
                <BarChart data={constituencyData}>
                   <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                   <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                   <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value/1000}k`} />
                   <Tooltip 
                      contentStyle={{ backgroundColor: 'hsl(var(--background))', borderColor: 'hsl(var(--border))', borderRadius: '12px' }}
                   />
                   <Bar dataKey="voters" radius={[4, 4, 0, 0]}>
                      {constituencyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                   </Bar>
                </BarChart>
             </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
         {constituencyData.map((item, i) => (
            <Card key={i} className="border-border/50 hover:border-primary/30 transition-all group overflow-hidden bg-background/50">
               <div className="h-1 bg-primary opacity-0 group-hover:opacity-100 transition-opacity" />
               <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                     <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-primary" />
                        <CardTitle className="text-lg">{item.name}</CardTitle>
                     </div>
                     <Badge className="bg-primary/10 text-primary border-none">Active</Badge>
                  </div>
                  <CardDescription>LS-Constituency #29</CardDescription>
               </CardHeader>
               <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                     <div className="p-3 bg-accent/30 rounded-xl">
                        <p className="text-[10px] uppercase font-bold text-muted-foreground">Electorate</p>
                        <p className="text-xl font-black">{(item.voters/1000).toFixed(1)}k</p>
                     </div>
                     <div className="p-3 bg-accent/30 rounded-xl">
                        <p className="text-[10px] uppercase font-bold text-muted-foreground">Turnout</p>
                        <p className="text-xl font-black text-green-500">{item.turnout}%</p>
                     </div>
                  </div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border/50 pt-4">
                     <div className="flex items-center gap-1">
                        <Building2 className="w-3 h-3" />
                        <span>{item.booths} Booths</span>
                     </div>
                     <div className="flex items-center gap-1 text-primary font-bold cursor-pointer hover:underline">
                        <span>Details</span>
                        <TrendingUp className="w-3 h-3" />
                     </div>
                  </div>
               </CardContent>
            </Card>
         ))}
      </div>
    </div>
  )
}

export default ConstituencyAnalytics
